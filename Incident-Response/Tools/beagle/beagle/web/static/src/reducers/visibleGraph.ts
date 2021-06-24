import * as _ from 'lodash';
import Mutator from 'src/mutators';

import { Action, ActionTypes } from '../actions/visibleGraph';
import { Edge, Node } from '../models';

export interface State {
    visibleNodes: Node[]; // Set of the currently visible nodes
    visibleEdges: Edge[]; // Set of the currently visible nodes
    visibleNodeTypes: string[];
    visibleEdgeTypes: string[];
    earliestEvent: Date;
    latestEvent: Date;
}

export const initialState: State = {
    visibleNodes: [],
    visibleEdges: [],
    visibleNodeTypes: [],
    visibleEdgeTypes: [],
    earliestEvent: new Date(0),
    latestEvent: new Date()
};

// We only pull in 25 at a time.
export const PULL_IN_LIMIT = 25;

export function updateVisibleEdges(nodes: Node[], edges: Edge[]) {
    const nodeIds = _.map(nodes, "id");

    return edges.filter(e => _.includes(nodeIds, e.from) && _.includes(nodeIds, e.to));
}

function pullInNeighbors(state: State, node: number, nodes: Node[], edges: Edge[]) {
    // Get all incoming or outgoing neighbors of this node.
    const candidates: number[] = Array.from(
        // Transform into a set to prevent duplicate IDs
        new Set(
            edges
                .filter(
                    (edge: Edge) =>
                        (edge.from === node || edge.to === node) &&
                        _.includes(state.visibleEdgeTypes, edge.label)
                )
                .reduce(
                    (accumulator: number[], edge: Edge) => accumulator.concat([edge.from, edge.to]),
                    []
                )
        )
    );

    // Map to node objects.
    const nodesToAdd: Node[] = candidates.map(
        (nodeId: number): Node => nodes.filter(n => n.id === nodeId)[0]
    );

    // Get only **new** nodes, don't add in ones we already have present.
    const newNodes: Node[] = nodesToAdd
        .reduce(
            (accumulator: Node[], newNode: Node): Node[] =>
                // Make sure this node is not already visible.
                state.visibleNodes.find((presentNode: Node) => newNode.id === presentNode.id) ===
                undefined
                    ? accumulator.concat([newNode])
                    : accumulator,
            []
        )
        .slice(0, PULL_IN_LIMIT);

    return state.visibleNodes.concat(newNodes);
}

function addSingleNode(state: State, node: number, nodes: Node[]) {
    const nodeObj = nodes.filter(n => n.id === node)[0];

    const currentNodes: number[] = state.visibleNodes.map((n: Node) => n.id);

    return currentNodes.indexOf(node) > -1 ? state.visibleNodes : [nodeObj, ...state.visibleNodes];
}

function filterForVisibleNodes(state: State) {
    state.visibleNodes = state.visibleNodes.filter(n =>
        _.includes(state.visibleNodeTypes, n._node_type)
    );

    const idsToNodes = state.visibleNodes.reduce((accum: object, node: Node) => {
        accum[node.id] = node;
        return accum;
    }, {});

    state.visibleEdges = state.visibleEdges.filter(
        e =>
            _.includes(state.visibleEdgeTypes, e.label) &&
            _.has(idsToNodes, e.from) &&
            _.has(idsToNodes, e.to)
    );

    return state;
}

export function reducer(state: State = initialState, action: Action) {
    let nextState: State = state;

    switch (action.type) {
        case ActionTypes.SET_VISIBLE_NODES: {
            nextState = {
                ...state,
                visibleNodes: action.payload.nodes
            };
            break;
        }

        case ActionTypes.SET_VISIBLE_EDGES: {
            nextState = {
                ...state,
                visibleEdges: action.payload.edges
            };
            break;
        }

        case ActionTypes.PULL_IN_NEIGHBORS: {
            const nextVisibleNodes = pullInNeighbors(
                state,
                action.payload.node,
                action.nodes,
                action.edges
            );

            const nextVisibleEdges = updateVisibleEdges(nextVisibleNodes, action.edges);

            const [min, max] = findMinMax(
                _.flatMap(nextVisibleEdges, e => _.map(e.properties.data, "timestamp"))
            );

            nextState = {
                ...state,
                // Pull in neighbors changes the set of visible nodes.
                visibleNodes: nextVisibleNodes,
                visibleEdges: nextVisibleEdges,
                latestEvent: stringToEpoch(max),
                earliestEvent: stringToEpoch(min)
            };
            break;
        }

        case ActionTypes.HIDE_NODE: {
            const nextVisibleNodes = state.visibleNodes.filter(
                (visibleNode: Node) => visibleNode.id !== action.payload.node
            );

            const nextVisibleEdges = updateVisibleEdges(nextVisibleNodes, state.visibleEdges);
            const [min, max] = findMinMax(
                _.flatMap(nextVisibleEdges, e => _.map(e.properties.data, "timestamp"))
            );

            nextState = {
                ...state,
                // Pull in neighbors changes the set of visible nodes.
                visibleNodes: nextVisibleNodes,
                visibleEdges: nextVisibleEdges,
                latestEvent: stringToEpoch(max),
                earliestEvent: stringToEpoch(min)
            };
            break;
        }

        case ActionTypes.ADD_NODE: {
            const nextVisibleNodes = addSingleNode(state, action.payload.node, action.nodes);

            const nextVisibleEdges = updateVisibleEdges(nextVisibleNodes, action.edges);

            const [min, max] = findMinMax(
                _.flatMap(nextVisibleEdges, e => _.map(e.properties.data, "timestamp"))
            );

            nextState = {
                ...state,
                // Pull in neighbors changes the set of visible nodes.
                visibleNodes: nextVisibleNodes,
                visibleEdges: nextVisibleEdges,
                latestEvent: stringToEpoch(max),
                earliestEvent: stringToEpoch(min)
            };
            break;
        }

        case ActionTypes.SET_VISIBLE_NODE_TYPES: {
            nextState = {
                ...state,
                visibleNodeTypes: action.payload.nodeTypes
            };
            break;
        }

        case ActionTypes.SET_VISIBLE_EDGE_TYPES: {
            nextState = {
                ...state,
                visibleEdgeTypes: action.payload.edgeTypes
            };
            break;
        }

        case ActionTypes.RUN_MUTATOR_FROM_NODE: {
            const mutator: Mutator = action.mutator;

            const { visibleNodes, visibleEdges } = mutator.mutate(
                action.visibleNodes,
                action.visibleEdges,
                action.visibleNodeTypes,
                action.visibleEdgeTypes,
                action.nodes,
                action.edges,
                action.selectedNode
            );

            const [min, max] = findMinMax(
                _.flatMap(visibleEdges, e => _.map(e.properties.data, "timestamp"))
            );

            nextState = {
                ...state,
                visibleEdges,
                visibleNodes,
                latestEvent: stringToEpoch(max),
                earliestEvent: stringToEpoch(min)
            };
            break;
        }

        default: {
            nextState = state;
            break;
        }
    }

    return filterForVisibleNodes(nextState);
}

function findMinMax(arr: any) {
    let min = arr[0];
    let max = arr[0];

    for (let i = 1, len = arr.length; i < len; i++) {
        const v = arr[i];
        min = v < min ? v : min;
        max = v > max ? v : max;
    }

    return [min, max];
}

function stringToEpoch(timeStr: string) {
    const d = new Date(0);
    d.setUTCSeconds(Number(timeStr));
    return d;
}
