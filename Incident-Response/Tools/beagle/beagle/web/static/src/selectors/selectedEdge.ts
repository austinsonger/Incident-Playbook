import { createSelector } from 'reselect';

import { State } from '../reducers';

const getSelectedEdgeState = (state: State) => state.selectedEdge;

// Get the select node
export const getSelecteEdge = createSelector(
    [getSelectedEdgeState],
    s => s.edge
);
