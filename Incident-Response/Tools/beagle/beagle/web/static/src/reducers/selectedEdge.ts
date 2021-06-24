import { Action, ActionTypes } from '../actions/selectedEdge';
import { Edge } from '../models';

export interface State {
    edge: undefined | Edge;
}

export const initialState: State = {
    edge: undefined
};

export function reducer(state: State = initialState, action: Action) {
    switch (action.type) {
        // Set the initial edges
        case ActionTypes.SET_SELECTED_EDGE: {
            return {
                edge:
                    action.payload.edge === undefined
                        ? undefined
                        : action.edges.filter(e => e.id === action.payload.edge)[0]
            };
        }

        default: {
            return state;
        }
    }
}
