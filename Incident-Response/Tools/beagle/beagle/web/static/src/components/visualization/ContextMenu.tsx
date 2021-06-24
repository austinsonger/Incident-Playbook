import * as React from 'react';
import { ContextMenu as RContextMenu, ContextMenuTrigger, MenuItem } from 'react-contextmenu';
import { runMutatorFromNode } from 'src/actions/visibleGraph';
import { store } from 'src/App';
import BackwardTravel from 'src/mutators/traversals/backwardTravel';
import ForwardTravel from 'src/mutators/traversals/forwardTravel';

import { getNodeAt } from './visjs-hook';

export interface ContextMenuProps {
    position: vis.Position;
}

export default class ContextMenu extends React.Component<ContextMenuProps, any> {
    public constructor(props: ContextMenuProps) {
        super(props);
    }

    public runBackWardsTravel = () => {
        const nodeId = Number(getNodeAt(this.props.position));

        store.dispatch(runMutatorFromNode(nodeId, new BackwardTravel()));
    };

    public runForwardsTravel = () => {
        const nodeId = Number(getNodeAt(this.props.position));

        store.dispatch(runMutatorFromNode(nodeId, new ForwardTravel()));
    };

    public render() {
        return (
            <ContextMenuTrigger id="graph_context_menu">
                {this.props.children}
                <RContextMenu id="graph_context_menu">
                    <MenuItem onClick={this.runBackWardsTravel}>Backtrack Node</MenuItem>
                    <MenuItem onClick={this.runForwardsTravel}>Show all descendents</MenuItem>
                </RContextMenu>
            </ContextMenuTrigger>
        );
    }
}
