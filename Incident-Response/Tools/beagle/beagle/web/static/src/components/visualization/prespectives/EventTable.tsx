import * as _ from 'lodash';
import * as React from 'react';
import { Accordion, Divider, Header, Icon, Segment, Table } from 'semantic-ui-react';
import { SetSelectedEdge } from 'src/actions/selectedEdge';
import { setSelectedNode } from 'src/actions/selectedNode';
import { store } from 'src/App';
import { snakeToSpaced } from 'src/common';
import { Node } from 'src/models';

import { VizProps } from '.';

export default class EventTable extends React.PureComponent<VizProps, any> {
    public fieldsToTable = (properties: object) => {
        return (
            <Table className="centered" compact={true}>
                {_.toPairs(properties).map(pair => (
                    <Table.Row>
                        <Table.Cell>{snakeToSpaced(pair[0])}</Table.Cell>
                        <Table.Cell>
                            {typeof pair[1] === "string"
                                ? snakeToSpaced(pair[1])
                                : JSON.stringify(pair[1])}
                        </Table.Cell>
                    </Table.Row>
                ))}
            </Table>
        );
    };

    public handleNodeClick = (id: number) => {
        return (e: any) => {
            store.dispatch(setSelectedNode(id));
        };
    };

    public handleEgeClick = (id: number) => {
        return (e: any) => {
            store.dispatch(SetSelectedEdge(id));
        };
    };

    public makeNodesTable = () => {
        return (
            <Table selectable={true} celled={true} sortable={true}>
                <Table.Header>
                    <Table.HeaderCell>Node Type</Table.HeaderCell>
                    <Table.HeaderCell>Display</Table.HeaderCell>
                </Table.Header>
                <Table.Body>
                    {this.props.visibleNodes.map(n => (
                        <Table.Row onClick={this.handleNodeClick(n.id)} key={n.id}>
                            <Table.Cell>{n._node_type}</Table.Cell>
                            <Table.Cell>{n._display}</Table.Cell>
                        </Table.Row>
                    ))}
                </Table.Body>
            </Table>
        );
    };

    public makeEdgesTable = (idsToNodes: object) => {
        return (
            <Table selectable={true} celled={true} sortable={true}>
                <Table.Header>
                    <Table.HeaderCell>From</Table.HeaderCell>
                    <Table.HeaderCell>To</Table.HeaderCell>
                    <Table.HeaderCell>Type</Table.HeaderCell>
                </Table.Header>
                <Table.Body>
                    {this.props.visibleEdges.map(e => (
                        <Table.Row onClick={this.handleEgeClick(e.id)} key={e.id}>
                            <Table.Cell>{idsToNodes[e.to]._display}</Table.Cell>
                            <Table.Cell>{idsToNodes[e.from]._display}</Table.Cell>
                            <Table.Cell>{e.label}</Table.Cell>
                        </Table.Row>
                    ))}
                </Table.Body>
            </Table>
        );
    };

    public render() {
        const idsToNodes = this.props.visibleNodes.reduce((accum: object, node: Node) => {
            accum[node.id] = node;
            return accum;
        }, {});

        return (
            <Segment style={{ height: "92vh", overflowY: "auto" }}>
                <Accordion
                    defaultActiveIndex={[0, 1, 2, 3, 4, 5, 6]}
                    exclusive={false}
                    panels={[
                        {
                            key: "nodes_table",
                            title: {
                                children: (
                                    <Divider horizontal={true}>
                                        <Header as="h3">
                                            <Icon name="linode" /> Nodes
                                        </Header>
                                    </Divider>
                                )
                            },
                            content: { children: this.makeNodesTable() }
                        },
                        {
                            key: "nodes_table",
                            title: {
                                children: (
                                    <Divider horizontal={true}>
                                        <Header as="h3">
                                            <Icon name="arrows alternate horizontal" /> Edges
                                        </Header>
                                    </Divider>
                                )
                            },
                            content: { children: this.makeEdgesTable(idsToNodes) }
                        }
                    ]}
                />
            </Segment>
        );
    }
}
