import { Action, ActionTypes } from '../actions/selectedNode';
import { Node } from '../models';

export interface State {
    node: undefined | Node;
}

export const initialState: State = {
    node: undefined
};

export function reducer(state: State = initialState, action: Action) {
    switch (action.type) {
        // Set the initial edges
        case ActionTypes.SET_SELECTED_NODE: {
            return {
                node:
                    action.payload.node === undefined
                        ? undefined
                        : action.nodes.filter(n => n.id === action.payload.node)[0]
            };
        }

        default: {
            return state;
        }
    }
}
