import { store } from 'src/App';

import { Node } from '../models';

export enum ActionTypes {
    SET_SELECTED_NODE = "[selected_node] SET_SELECTED_NODE"
}

export interface SetSelectedNode {
    type: ActionTypes.SET_SELECTED_NODE;
    nodes: Node[];
    payload: { node: number | undefined };
}

/* tslint:disable:object-literal-sort-keys */
export function setSelectedNode(node: number | undefined): SetSelectedNode {
    return {
        type: ActionTypes.SET_SELECTED_NODE,
        nodes: store.getState().graph.nodes,
        payload: {
            node
        }
    };
}

export type Action = SetSelectedNode;
