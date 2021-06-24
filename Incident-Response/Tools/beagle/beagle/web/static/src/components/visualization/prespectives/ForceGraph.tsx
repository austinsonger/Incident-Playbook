import * as React from 'react';
import { hideMenu } from 'react-contextmenu/modules/actions';
import Graph from 'react-graph-vis';
import { SetSelectedEdge } from 'src/actions/selectedEdge';
import { setSelectedNode } from 'src/actions/selectedNode';
import { hideNode, pullInNeighbors } from 'src/actions/visibleGraph';
import { store } from 'src/App';

import { GraphEvent, VizProps } from '.';
import { GRAPH_VIZ_CONFIG } from '../config';
import ContextMenu from '../ContextMenu';
import { freezeGraph, initVisjsControl } from '../visjs-hook';

export default class ForceGraph extends React.Component<VizProps> {
    public state: vis.Position;

    constructor(props: VizProps) {
        super(props);
    }

    public onClick = (event: GraphEvent) => {
        const { nodes, edges } = event;

        // Hide the child context menu.
        hideMenu();

        if (nodes.length !== 0) {
            store.dispatch(setSelectedNode(nodes[0]));
        } else if (edges.length !== 0) {
            store.dispatch(SetSelectedEdge(edges[0]));
        }
    };

    public onDoubleClick = (event: GraphEvent) => {
        const nodes = event.nodes;

        if (nodes.length === 0) {
            return;
        }

        store.dispatch(pullInNeighbors(nodes[0]));
    };

    public onHold = (event: GraphEvent) => {
        const nodes = event.nodes;

        if (nodes.length === 0) {
            return;
        }

        store.dispatch(hideNode(nodes[0]));
    };

    public onRightClick = (clickEvent: { pointer: { DOM: { x: number; y: number } } }) => {
        this.setState(clickEvent.pointer.DOM);
        freezeGraph();
        return true;
    };

    public render() {
        return (
            <ContextMenu position={this.state}>
                <Graph
                    key="graph"
                    // Make graph work on parents nodes.
                    graph={{
                        edges: this.props.visibleEdges,
                        nodes: this.props.visibleNodes
                    }}
                    getNetwork={initVisjsControl}
                    options={GRAPH_VIZ_CONFIG}
                    events={{
                        click: this.onClick,
                        doubleClick: this.onDoubleClick,
                        hold: this.onHold,
                        oncontext: this.onRightClick
                    }}
                />
            </ContextMenu>
        );
    }
}
