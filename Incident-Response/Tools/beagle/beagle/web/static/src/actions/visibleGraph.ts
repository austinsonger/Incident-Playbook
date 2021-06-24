import { store } from 'src/App';
import Mutator from 'src/mutators';

import { Edge, Node } from '../models';

export enum ActionTypes {
    SET_VISIBLE_NODES = "[visible_graph] SET_VISIBLE_NODES",
    SET_VISIBLE_EDGES = "[visible_graph] SET_VISIBLE_EDGES",
    PULL_IN_NEIGHBORS = "[visible_graph] PULL_IN_NEIGHBORS",
    HIDE_NODE = "[visible_graph] HIDE_NODE",
    ADD_NODE = "[visible_graph] ADD_NODE",
    SET_VISIBLE_NODE_TYPES = "[visible_graph] SET_VISIBLE_NODE_TYPES",
    SET_VISIBLE_EDGE_TYPES = "[visible_graph] SET_VISIBLE_EDGE_TYPES",
    RUN_MUTATOR_FROM_NODE = "[mutator] RUN_MUTATOR_FROM_NODE"
}

export interface SetVisibleNodes {
    type: ActionTypes.SET_VISIBLE_NODES;
    payload: { nodes: Node[] };
}

export interface SetVisibleEdges {
    type: ActionTypes.SET_VISIBLE_EDGES;
    payload: { edges: Edge[] };
}

export interface PullInNeighbors {
    type: ActionTypes.PULL_IN_NEIGHBORS;
    payload: { node: number };
    nodes: Node[];
    edges: Edge[];
}

export interface HideNode {
    type: ActionTypes.HIDE_NODE;
    payload: { node: number };
}

export interface AddNode {
    type: ActionTypes.ADD_NODE;
    payload: { node: number };
    nodes: Node[];
    edges: Edge[];
}

export interface SetVisibleNodeTypes {
    type: ActionTypes.SET_VISIBLE_NODE_TYPES;
    payload: { nodeTypes: string[] };
}

export interface SetVisibleEdgeTypes {
    type: ActionTypes.SET_VISIBLE_EDGE_TYPES;
    payload: { edgeTypes: string[] };
}

export interface RunMutatorFromNode {
    type: ActionTypes.RUN_MUTATOR_FROM_NODE;
    selectedNode: number;
    mutator: Mutator;
    nodes: Node[];
    edges: Edge[];
    visibleNodes: Node[];
    visibleEdges: Edge[];
    visibleNodeTypes: string[];
    visibleEdgeTypes: string[];
}

/* tslint:disable:object-literal-sort-keys */
export function setVisibleNodes(nodes: Node[]): SetVisibleNodes {
    return {
        type: ActionTypes.SET_VISIBLE_NODES,
        payload: {
            nodes
        }
    };
}

/* tslint:disable:object-literal-sort-keys */
export function setVisibleEdges(edges: Edge[]): SetVisibleEdges {
    return {
        type: ActionTypes.SET_VISIBLE_EDGES,
        payload: {
            edges
        }
    };
}

export function pullInNeighbors(node: number): PullInNeighbors {
    return {
        type: ActionTypes.PULL_IN_NEIGHBORS,
        payload: {
            node
        },
        nodes: store.getState().graph.nodes,
        edges: store.getState().graph.edges
    };
}

export function hideNode(node: number): HideNode {
    return {
        type: ActionTypes.HIDE_NODE,
        payload: {
            node
        }
    };
}

export function addNode(node: number): AddNode {
    return {
        type: ActionTypes.ADD_NODE,
        payload: {
            node
        },
        nodes: store.getState().graph.nodes,
        edges: store.getState().graph.edges
    };
}

export function setVisibleNodeTypes(nodeTypes: string[]): SetVisibleNodeTypes {
    return {
        type: ActionTypes.SET_VISIBLE_NODE_TYPES,
        payload: {
            nodeTypes
        }
    };
}

/* tslint:disable:object-literal-sort-keys */
export function setVisibleEdgeTypes(edgeTypes: string[]): SetVisibleEdgeTypes {
    return {
        type: ActionTypes.SET_VISIBLE_EDGE_TYPES,
        payload: {
            edgeTypes
        }
    };
}

/* tslint:disable:object-literal-sort-keys */
export function runMutatorFromNode(node: number, mutator: Mutator): RunMutatorFromNode {
    return {
        type: ActionTypes.RUN_MUTATOR_FROM_NODE,
        selectedNode: node,
        mutator,
        nodes: store.getState().graph.nodes,
        edges: store.getState().graph.edges,
        visibleNodes: store.getState().visibleGraph.present.visibleNodes,
        visibleEdges: store.getState().visibleGraph.present.visibleEdges,
        visibleNodeTypes: store.getState().visibleGraph.present.visibleNodeTypes,
        visibleEdgeTypes: store.getState().visibleGraph.present.visibleEdgeTypes
    };
}

export type Action =
    | SetVisibleNodes
    | SetVisibleEdges
    | PullInNeighbors
    | HideNode
    | AddNode
    | RunMutatorFromNode
    | SetVisibleNodeTypes
    | SetVisibleEdgeTypes;
