import { createSelector } from 'reselect';

import { State } from '../reducers';

const getGraphState = (state: State) => state.visibleGraph.present;

// Get visible nodes
export const getVisibleNodes = createSelector(
    [getGraphState],
    s => s.visibleNodes
);

export const getVisibleEdges = createSelector(
    [getGraphState],
    s => s.visibleEdges
);

export const getVisibleEdgeTypes = createSelector(
    [getGraphState],
    s => s.visibleEdgeTypes
);

export const getVisibleNodeTypes = createSelector(
    [getGraphState],
    s => s.visibleNodeTypes
);
