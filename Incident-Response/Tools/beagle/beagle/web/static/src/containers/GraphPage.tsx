import * as _ from 'lodash';
import * as React from 'react';
import { connect } from 'react-redux';
import { toastr } from 'react-redux-toastr';
import { ActionCreators as UndoActionCreators } from 'redux-undo';
import { Accordion, Divider, Grid, Header, Icon, SemanticICONS, Tab } from 'semantic-ui-react';
import { setNodesAndEdges } from 'src/actions/graph';
import { SetSelectedEdge } from 'src/actions/selectedEdge';
import { setSelectedNode } from 'src/actions/selectedNode';
import { store } from 'src/App';
import LoadingBar from 'src/components/misc/LoadingBar';
import NodeSearch from 'src/components/visualization/controls/NodeSearch';
import EdgeInfoTable from 'src/components/visualization/panels/EdgeInfoTable';
import EdgeTimeChart from 'src/components/visualization/panels/EdgeTimechart';
import NodeInfoTable from 'src/components/visualization/panels/NodeInfoTable';
import VisibleScope from 'src/components/visualization/panels/VisibleScope';
import EventTable from 'src/components/visualization/prespectives/EventTable';
import EventTimeline from 'src/components/visualization/prespectives/EventTimeline';
import ForceGraph from 'src/components/visualization/prespectives/ForceGraph';
import MarkdownExport from 'src/components/visualization/prespectives/MarkdownExport';
import TreeGraph from 'src/components/visualization/prespectives/TreeGraph';
import { Graph } from 'src/models/index.js';
import { State } from 'src/reducers';
import { PULL_IN_LIMIT } from 'src/reducers/visibleGraph';
import Upload from 'src/views/Upload';

import {
    pullInNeighbors,
    setVisibleEdges,
    setVisibleEdgeTypes,
    setVisibleNodes,
    setVisibleNodeTypes,
} from '../actions/visibleGraph';
import VisibleTypeToggles from '../components/visualization/controls/VisibleTypeToggles';
import GraphRedoUndo from './GraphRedoUndo';

const EXLUDED_BY_DEFAULT = ["Loaded", "File Of"];

interface GraphPageState {
    ready: boolean;
}

class GraphPage extends React.Component<any, GraphPageState> {
    private tab: any; // sematnic-ui uses old refs, easier to type hint as any.

    constructor(props: any) {
        super(props);

        this.state = {
            ready: false
        };
    }

    public componentDidUpdate(prevProps: any) {
        // Check if we pulled in the limit. If so, notify user.
        if (this.props.visibleNodes.length - prevProps.visibleNodes.length === PULL_IN_LIMIT) {
            toastr.warning(
                `Pull in limit (${PULL_IN_LIMIT}) reached`,
                "Double click the node again to pull in more neighbours."
            );
        }
    }

    public loadGraph() {
        fetch(
            `${process.env.NODE_ENV === "production" ? "" : "http://localhost:8000"}/api/graph/${
                this.props.match.params.id
            }`
        )
            .then(response => response.json())
            .then(graphJson => {
                const graph: Graph = {
                    directed: graphJson.directed,
                    edges: graphJson.links.map((link: any) => {
                        return {
                            from: link.source,
                            id: link.id,
                            label: link.type,
                            properties: link.properties,
                            to: link.target
                        };
                    }),
                    graph: graphJson.graph,
                    multigraph: graphJson.multigraph,
                    nodes: graphJson.nodes.map((node: any) => {
                        const newNode = Object.assign(node);

                        // 15 = len("255.255.255.255") ;
                        newNode.label = (node._display || "").substring(0, 15);
                        if (newNode.label.length === 15) {
                            newNode.label += "...";
                        }

                        newNode.color = node._color;
                        return newNode;
                    })
                };

                // Set the visible edge types
                store.dispatch(setVisibleNodeTypes(_.uniq(_.map(graph.nodes, "_node_type"))));

                // Set the visible edge types, excluding what is off by default.
                store.dispatch(
                    setVisibleEdgeTypes(
                        _.uniq(_.map(graph.edges, "label")).filter(
                            edgeType => !_.includes(EXLUDED_BY_DEFAULT, edgeType)
                        )
                    )
                );
                store.dispatch(setNodesAndEdges(graph.nodes, graph.edges));

                const alertNodes = graph.nodes.filter(n => n._node_type === "Alert");

                if (alertNodes.length > 0) {
                    store.dispatch(setVisibleNodes([...alertNodes]));
                    alertNodes.map(node => store.dispatch(pullInNeighbors(node.id)));
                    store.dispatch(UndoActionCreators.clearHistory()); // Wipe state here
                } else {
                    // Set base state here

                    const sample = _.sampleSize(graph.nodes, 10);
                    store.dispatch(setVisibleNodes(sample));
                    store.dispatch(pullInNeighbors(sample[0].id));

                    store.dispatch(UndoActionCreators.clearHistory());
                }

                this.setState({ ready: true });
            });
    }

    public loadAndResetView() {
        this.tab.state.activeIndex = 0;

        this.loadGraph();

        toastr.info("Evidence added to graph", `Uploaded artifact merged into graph.`, {
            timeOut: 10000
        });
    }

    public componentWillMount() {
        this.loadGraph();
    }

    public componentWillUnmount = () => {
        // Reset the graph on unmount.
        store.dispatch(setVisibleNodeTypes([]));
        store.dispatch(setVisibleEdgeTypes([]));
        store.dispatch(setNodesAndEdges([], []));
        store.dispatch(setVisibleNodes([]));
        store.dispatch(setVisibleEdges([]));
        store.dispatch(setSelectedNode(undefined));
        store.dispatch(SetSelectedEdge(undefined));
        store.dispatch(UndoActionCreators.clearHistory());
    };

    public makeDivider(text: string, icon: SemanticICONS) {
        return (
            <Divider horizontal={true}>
                <Header as="h4">
                    <Icon name={icon} />
                    {text}
                </Header>
            </Divider>
        );
    }

    public render() {
        if (this.state.ready === false) {
            return <LoadingBar text="Fetching Graph Data" />;
        }

        return (
            <Grid columns={2} celled="internally" padded={false}>
                <Grid.Column width={10}>
                    <Tab
                        ref={ref => (this.tab = ref)}
                        menu={{ color: "black", secondary: true, pointing: true, attached: "top" }}
                        panes={[
                            {
                                menuItem: "Graph",
                                render: () => (
                                    <ForceGraph
                                        visibleEdges={this.props.visibleEdges}
                                        visibleNodes={this.props.visibleNodes}
                                    />
                                )
                            },
                            {
                                menuItem: "Tree",
                                render: () => (
                                    <TreeGraph
                                        visibleEdges={this.props.visibleEdges}
                                        visibleNodes={this.props.visibleNodes}
                                    />
                                )
                            },
                            {
                                menuItem: "Timeline",
                                render: () => (
                                    <EventTimeline
                                        visibleEdges={this.props.visibleEdges}
                                        visibleNodes={this.props.visibleNodes}
                                    />
                                )
                            },
                            {
                                menuItem: "Table",
                                render: () => (
                                    <EventTable
                                        visibleEdges={this.props.visibleEdges}
                                        visibleNodes={this.props.visibleNodes}
                                    />
                                )
                            },
                            {
                                menuItem: "Markdown",
                                render: () => (
                                    <MarkdownExport
                                        visibleEdges={this.props.visibleEdges}
                                        visibleNodes={this.props.visibleNodes}
                                    />
                                )
                            },
                            {
                                menuItem: "Add Evidence",
                                render: () => (
                                    // Add evidence
                                    <Upload
                                        postRoute={`/add/${this.props.match.params.id}`}
                                        postUploadHandler={this.loadAndResetView.bind(this)}
                                    />
                                )
                            }
                        ]}
                    />
                </Grid.Column>

                <Grid.Column
                    width={6}
                    stretched={false}
                    style={{ overflowY: "auto", maxHeight: "100vh" }}
                >
                    <Grid.Row centered={true}>
                        <VisibleScope
                            nodes={this.props.nodes.length}
                            edges={this.props.edges.length}
                            visibleNodes={this.props.visibleNodes.length}
                            visibleEdges={this.props.visibleEdges.length}
                            latestEvent={this.props.latestEvent}
                            earliestEvent={this.props.earliestEvent}
                        />
                    </Grid.Row>
                    {<br /> /* Empty row to force a newline? */}
                    <Grid.Row>
                        <Accordion
                            defaultActiveIndex={[0, 1, 2, 3, 4, 5, 6]}
                            exclusive={false}
                            panels={[
                                {
                                    key: "node_search",
                                    title: {
                                        children: this.makeDivider("Node Search", "search")
                                    },
                                    content: { children: <NodeSearch nodes={this.props.nodes} /> }
                                },
                                {
                                    key: "graph_controls",
                                    title: {
                                        children: this.makeDivider("Graph Controls", "configure")
                                    },
                                    content: { children: <GraphRedoUndo /> }
                                },
                                {
                                    key: "node_visibility_controls",
                                    title: {
                                        children: this.makeDivider("Node/Edge Visibility", "eye")
                                    },
                                    content: {
                                        children: (
                                            <VisibleTypeToggles
                                                nodes={this.props.nodes}
                                                edges={this.props.edges}
                                                visibleEdgeTypes={this.props.visibleEdgeTypes}
                                                visibleNodeTypes={this.props.visibleNodeTypes}
                                            />
                                        )
                                    }
                                },
                                {
                                    key: "node_info",
                                    title: {
                                        children: this.makeDivider("Node Info", "info circle")
                                    },
                                    content: {
                                        children: <NodeInfoTable node={this.props.selectedNode} />
                                    }
                                },
                                {
                                    key: "edge_info",
                                    title: {
                                        children: this.makeDivider("Edge Info", "info circle")
                                    },
                                    content: {
                                        children: [
                                            <EdgeInfoTable
                                                key="table"
                                                edge={this.props.selectedEdge}
                                            />,
                                            false && (
                                                <EdgeTimeChart
                                                    key="timechart"
                                                    edge={this.props.selectedEdge}
                                                    latestEvent={this.props.latestEvent}
                                                    earliestEvent={this.props.earliestEvent}
                                                />
                                            )
                                        ]
                                    }
                                }
                            ]}
                        />
                    </Grid.Row>
                </Grid.Column>
            </Grid>
        );
    }
}

const mapStateToProps = (state: State) => ({
    visibleNodes: state.visibleGraph.present.visibleNodes,
    visibleEdges: state.visibleGraph.present.visibleEdges,
    selectedNode: state.selectedNode.node,
    selectedEdge: state.selectedEdge.edge,
    nodes: state.graph.nodes,
    edges: state.graph.edges,
    visibleNodeTypes: state.visibleGraph.present.visibleNodeTypes,
    visibleEdgeTypes: state.visibleGraph.present.visibleEdgeTypes,
    latestEvent: state.visibleGraph.present.latestEvent,
    earliestEvent: state.visibleGraph.present.earliestEvent
});

export default connect<any, any, any>(mapStateToProps)(GraphPage);
