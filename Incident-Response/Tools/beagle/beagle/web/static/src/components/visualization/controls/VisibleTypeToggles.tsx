import * as _ from 'lodash';
import * as React from 'react';
import { Checkbox, CheckboxProps, Grid, Header, List } from 'semantic-ui-react';
import { setVisibleEdgeTypes, setVisibleNodeTypes } from 'src/actions/visibleGraph';
import { store } from 'src/App';
import { Edge, Node } from 'src/models';

export interface VisibleTypeTogglesProps {
    nodes: Node[];
    edges: Edge[];
    visibleNodeTypes: string[];
    visibleEdgeTypes: string[];
}

export interface VisibleTypeTogglesState {
    allNodeTypes: Array<{ type: string; color: string }>;
    allEdgeTypes: string[];
}

export default class VisibleTypeToggles extends React.Component<
    VisibleTypeTogglesProps,
    VisibleTypeTogglesState
> {
    public static getDerivedStateFromProps(props: VisibleTypeTogglesProps) {
        return {
            allEdgeTypes: _.uniq(_.map(props.edges, "label")),
            allNodeTypes: _.uniqBy(
                _.map(props.nodes, n => ({ color: n.color, type: n._node_type })),
                "type"
            )
        };
    }

    constructor(props: VisibleTypeTogglesProps) {
        super(props);

        this.state = {
            allNodeTypes: [],
            allEdgeTypes: []
        };
    }

    public toggleNodeVisiblity = (e: React.SyntheticEvent, props: CheckboxProps) => {
        // Cast to string
        const nodeType = String(props.value);

        let nextNodeTypes = this.props.visibleNodeTypes;

        // Check if we are removing or adding.
        if (props.checked) {
            nextNodeTypes = _.uniq([...nextNodeTypes, nodeType]);
        } else {
            nextNodeTypes = nextNodeTypes.filter(n => n !== nodeType);
        }

        // Dispatch
        store.dispatch(setVisibleNodeTypes(nextNodeTypes));
    };

    public toggleEdgeVisibility = (e: React.SyntheticEvent, props: CheckboxProps) => {
        // Cast to string
        const nodeType = String(props.value);

        let nextEdgeTypes = this.props.visibleEdgeTypes;

        // Check if we are removing or adding.
        if (props.checked) {
            nextEdgeTypes = _.uniq([...nextEdgeTypes, nodeType]);
        } else {
            nextEdgeTypes = nextEdgeTypes.filter(n => n !== nodeType);
        }

        // Dispatch
        store.dispatch(setVisibleEdgeTypes(nextEdgeTypes));
    };

    public render() {
        return (
            <Grid columns="equal" textAlign="left" divided={true}>
                <Grid.Column>
                    <Header as="h5">Node Types</Header>
                    <List floated="left">
                        {this.state.allNodeTypes.map(nodeType => (
                            <List.Item key={nodeType.type}>
                                {/* <Segment style={{ backgroundColor: nodeType.color }} basic={true}> */}
                                <Checkbox
                                    checked={_.includes(this.props.visibleNodeTypes, nodeType.type)}
                                    value={nodeType.type}
                                    onChange={this.toggleNodeVisiblity}
                                    label={nodeType.type}
                                />
                                {/* </Segment> */}
                            </List.Item>
                        ))}
                    </List>
                </Grid.Column>
                <Grid.Column>
                    <Header as="h5">Edge Types</Header>
                    <List floated="left">
                        {this.state.allEdgeTypes.map(edgeType => (
                            <List.Item key={edgeType}>
                                <Checkbox
                                    checked={_.includes(this.props.visibleEdgeTypes, edgeType)}
                                    value={edgeType}
                                    onChange={this.toggleEdgeVisibility}
                                    label={edgeType}
                                />
                            </List.Item>
                        ))}
                    </List>
                </Grid.Column>
            </Grid>
        );
    }
}
