import { Edge, Node } from '../models';

export enum ActionTypes {
    SET_NODES = "[graph] SET_NODES",
    SET_EDGES = "[graph] SET_EDGES",
    SET_NODES_AND_EDGES = "[graph] SET_NODES_AND_EDGES"
}

export interface SetNodes {
    type: ActionTypes.SET_NODES;
    payload: { nodes: Node[] };
}

export interface SetEdges {
    type: ActionTypes.SET_EDGES;
    payload: { edges: Edge[] };
}

export interface SetNodesAndEdges {
    type: ActionTypes.SET_NODES_AND_EDGES;
    payload: { nodes: Node[]; edges: Edge[] };
}

/* tslint:disable:object-literal-sort-keys */
export function setNodes(nodes: Node[]): SetNodes {
    return {
        type: ActionTypes.SET_NODES,
        payload: {
            nodes
        }
    };
}
/* tslint:disable:object-literal-sort-keys */
export function setEdges(edges: Edge[]): SetEdges {
    return {
        type: ActionTypes.SET_EDGES,
        payload: {
            edges
        }
    };
}

export function setNodesAndEdges(nodes: Node[], edges: Edge[]): SetNodesAndEdges {
    return {
        type: ActionTypes.SET_NODES_AND_EDGES,
        payload: {
            nodes,
            edges
        }
    };
}

export type Action = SetEdges | SetNodes | SetNodesAndEdges;
