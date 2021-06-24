import { createSelector } from 'reselect';

import { State } from '../reducers';

const getSelectedNodeState = (state: State) => state.selectedNode;

// Get the select node
export const getSelectedNode = createSelector(
    [getSelectedNodeState],
    s => s.node
);
