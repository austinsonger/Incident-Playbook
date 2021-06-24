import * as React from 'react';
import { connect } from 'react-redux';
import { Dispatch } from 'redux';
import { ActionCreators as UndoActionCreators } from 'redux-undo';
import { Button } from 'semantic-ui-react';
import { State } from 'src/reducers';

export interface GraphRedoUndoProps {
    onUndo: () => void;
    onRedo: () => void;
    onReset: () => void;
    canUndo: boolean;
    canRedo: boolean;
}

class GraphRedoUndo extends React.Component<GraphRedoUndoProps, any> {
    public render() {
        return (
            <div>
                <Button
                    key="undo"
                    icon="undo"
                    content="Undo"
                    style={{ marginLeft: "auto" }}
                    attached="left"
                    labelPosition="left"
                    onClick={this.props.onUndo}
                    disabled={!this.props.canUndo}
                />
                <Button
                    key="redo"
                    icon="redo"
                    content="Redo"
                    attached="right"
                    style={{ marginLeft: "auto" }}
                    labelPosition="right"
                    onClick={this.props.onRedo}
                    disabled={!this.props.canRedo}
                />
                <Button
                    key="reset"
                    icon="eraser"
                    content="Reset"
                    style={{ float: "right" }}
                    negative={true}
                    labelPosition="right"
                    onClick={this.props.onReset}
                    disabled={!this.props.canUndo}
                />
            </div>
        );
    }
}

const mapStateToProps = (state: State) => {
    return {
        // Makes it so that the graph is initialized
        canUndo: state.visibleGraph.past.length > 0,
        canRedo: state.visibleGraph.future.length > 0
    };
};

const mapDispatchToProps = (dispatch: Dispatch) => {
    return {
        onUndo: () => dispatch(UndoActionCreators.undo()),
        onRedo: () => dispatch(UndoActionCreators.redo()),
        // Reset by jumping to 0 and clearing the history.
        onReset: () => {
            dispatch(UndoActionCreators.jumpToPast(0));
        }
    };
};
export default connect<any, any, any>(
    mapStateToProps,
    mapDispatchToProps
)(GraphRedoUndo);
