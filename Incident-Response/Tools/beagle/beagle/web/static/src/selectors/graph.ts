import { createSelector } from 'reselect';

import { State } from '../reducers';

/*
 * Get the graph state from the root state
 */
const getGraphState = (state: State) => state.graph;

/*
 * Getting nodes array from graph State
 */
export const getNodes = createSelector(
    [getGraphState],
    s => s.nodes
);

// Get the edges
export const getEdges = createSelector(
    [getGraphState],
    s => s.edges
);

