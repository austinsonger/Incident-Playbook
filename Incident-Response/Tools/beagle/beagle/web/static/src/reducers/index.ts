import { reducer as toastrReducer } from 'react-redux-toastr';
import { combineReducers } from 'redux';
import undoable, { StateWithHistory } from 'redux-undo';

import * as fromGraph from './graph';
import * as fromSelectedEdge from './selectedEdge';
import * as fromSelectedNode from './selectedNode';
import * as fromVisibleGraph from './visibleGraph';

/*
 * This is the root state of the app
 * It contains every substate of the app
 */
export interface State {
    graph: fromGraph.State;
    visibleGraph: StateWithHistory<fromVisibleGraph.State>;
    selectedNode: fromSelectedNode.State;
    selectedEdge: fromSelectedEdge.State;
}

/*
 * Root reducer of the app
 * Returned reducer will be of type Reducer<State>
 */
export const reducer = combineReducers({
    visibleGraph: undoable(fromVisibleGraph.reducer, {
        ignoreInitialState: true
    }),
    toastr: toastrReducer,
    graph: fromGraph.reducer,
    selectedNode: fromSelectedNode.reducer,
    selectedEdge: fromSelectedEdge.reducer
});
