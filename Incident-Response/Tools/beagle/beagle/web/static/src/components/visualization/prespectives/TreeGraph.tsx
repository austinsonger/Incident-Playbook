import * as React from 'react';
import Graph from 'react-graph-vis';

import { VizProps } from '.';
import { TREE_VIZ_CONFIG } from '../config';

export default class TreeGraph extends React.Component<VizProps, any> {
    public render() {
        return (
            <Graph
                graph={{
                    edges: this.props.visibleEdges,
                    nodes: this.props.visibleNodes
                }}
                options={TREE_VIZ_CONFIG}
            />
        );
    }
}
