import * as _ from 'lodash';
import * as React from 'react';
import {
    Label,
    List,
    Search,
    SearchCategoryProps,
    SearchProps,
    SearchResultData,
    SearchResultProps,
} from 'semantic-ui-react';
import { setSelectedNode } from 'src/actions/selectedNode';
import { addNode } from 'src/actions/visibleGraph';
import { store } from 'src/App';
import { snakeToSpaced } from 'src/common';
import { Node } from 'src/models';

export interface NodeSearchProps {
    nodes: Node[];
}

export interface NodeSearchState {
    nodeTypes: string[];
    nodeColors: object;
    groupedNodes: object;
    isLoading: boolean;
    results: {};
    value: string;
}

export default class NodeSearch extends React.Component<NodeSearchProps, NodeSearchState> {
    public static getDerivedStateFromProps(props: NodeSearchProps, prevState: NodeSearchState) {
        const groupedNodes = _.groupBy(props.nodes, "_node_type");
        const nodeTypes = Object.keys(groupedNodes);

        const nodeColors = {};
        _.toPairs(groupedNodes).map(([key, value]) => (nodeColors[key] = value[0].color));

        return { ...prevState, groupedNodes, nodeTypes, nodeColors };
    }

    public readonly state: NodeSearchState = {
        nodeTypes: [],
        groupedNodes: {},
        nodeColors: {},
        isLoading: false,
        results: {},
        value: ""
    };

    public resetComponent = () => this.setState({ isLoading: false, results: {}, value: "" });

    public handleResultSelect = (e: any, data: SearchResultData) => {
        this.setState({ value: data.result._display });
        store.dispatch(addNode(data.result.id));
        store.dispatch(setSelectedNode(data.result.id));
    };

    public handleSearchChange = (e: any, data: SearchProps) => {
        this.setState({ isLoading: true, value: data.value === undefined ? "" : data.value });

        setTimeout(() => {
            if (this.state.value.length < 1) {
                return this.resetComponent();
            }

            // Convert search value into Regex
            const re = new RegExp(_.escapeRegExp(this.state.value), "i");

            // Make a match against node objects, match against properties.
            const isMatch = (node: Node) => re.test(JSON.stringify(node.properties));

            // Search for hits across nodes.
            const filteredResults = _.reduce(
                this.state.groupedNodes,
                (accum: object, nodes: Node[], nodeType: string) => {
                    const results = _.filter(nodes, isMatch);

                    if (results.length) {
                        accum[nodeType] = { name: nodeType, results };
                    }
                    return accum;
                },
                {}
            );

            this.setState({
                isLoading: false,
                results: filteredResults
            });
        }, 300);
    };

    public resultsRender = (results: SearchResultProps) => {
        return (
            <div key={results.properties._key} style={{ wordBreak: "break-all" }}>
                <Label
                    content={results._display}
                    color="blue"
                    style={{ display: "flex", justifyContent: "center" }}
                    size="large"
                />
                {_.toPairs(results.properties).map(([key, value]: [string, string]) => {
                    return (
                        <List.Item key={key}>
                            <List.Content>
                                <b>{snakeToSpaced(key)}</b>:{" "}
                                {highlightText(value, this.state.value)}
                            </List.Content>
                        </List.Item>
                    );
                })}
            </div>
        );
    };

    public categoryRender = (results: SearchCategoryProps) => {
        const category = results.name;
        return (
            <Label tag={true} style={{ backgroundColor: this.state.nodeColors[category || ""] }}>
                {category}
            </Label>
        );
    };

    public render() {
        return (
            <Search
                input={{
                    fluid: true,
                    placeholder: "Search for a node across all properties (min 3 characters)."
                }}
                category={true}
                loading={this.state.isLoading}
                onResultSelect={this.handleResultSelect}
                onSearchChange={_.debounce(this.handleSearchChange, 500, { leading: true })}
                results={this.state.results}
                value={this.state.value}
                resultRenderer={this.resultsRender}
                categoryRenderer={this.categoryRender}
                fluid={true}
                minCharacters={3}
            />
        );
    }
}
// https://stackoverflow.com/a/47803998/3052228
const highlightText = (text = "", highlight = "") => {
    if (text === null) {
        return text;
    }

    if (!highlight.trim()) {
        return text.toString();
    }
    const regex = new RegExp(`(${_.escapeRegExp(highlight)})`, "gi");
    const parts = text.toString().split(regex);
    return parts
        .filter(part => part)
        .map((part, i) => (regex.test(part) ? <mark key={i}>{part}</mark> : part));
};
