import { store } from 'src/App';

import { Edge } from '../models';

export enum ActionTypes {
    SET_SELECTED_EDGE = "[selected_edge] SET_SELECTED_EDGE"
}

export interface SetSelectedEdge {
    type: ActionTypes.SET_SELECTED_EDGE;
    edges: Edge[];
    payload: { edge: number | undefined };
}

export function SetSelectedEdge(edge: number | undefined): SetSelectedEdge {
    return {
        type: ActionTypes.SET_SELECTED_EDGE,
        edges: store.getState().graph.edges,
        payload: {
            edge
        }
    };
}

export type Action = SetSelectedEdge;
