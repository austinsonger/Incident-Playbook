import { Action, ActionTypes } from '../actions/graph';
import { Edge, Node } from '../models';

export interface State {
    edges: Edge[]; // ALL Edges in the graph
    nodes: Node[]; // ALL Nodes in the graph
}

export const initialState: State = {
    edges: [],
    nodes: []
};

export function reducer(state: State = initialState, action: Action) {
    switch (action.type) {
        // Set the initial edges
        case ActionTypes.SET_EDGES: {
            return {
                ...state,
                edges: action.payload.edges
            };
        }

        // Set the initial nodes
        case ActionTypes.SET_NODES: {
            return {
                ...state,
                nodes: action.payload.nodes
            };
        }

        case ActionTypes.SET_NODES_AND_EDGES: {
            return {
                ...state,
                nodes: action.payload.nodes,
                edges: action.payload.edges
            };
        }

        default: {
            return state;
        }
    }
}
