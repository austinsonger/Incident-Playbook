import * as React from 'react';
import { Header, Table } from 'semantic-ui-react';
import { snakeToSpaced } from 'src/common';
import { Node } from 'src/models';

interface Props {
    node: Node;
}

export default class NodeInfoTable extends React.Component<Props, {}> {
    constructor(props: Props) {
        super(props);
    }

    public render() {
        const node = this.props.node;

        if (node === undefined) {
            return (
                <Header as="h3" className="centered">
                    Click a node to view information
                </Header>
            );
        } else {
            return (
                <Table celled={true} striped={true} columns={2}>
                    <Table.Header>
                        <Table.Row>
                            <Table.HeaderCell
                                colSpan="2"
                                textAlign="center"
                                style={{ backgroundColor: node.color }}
                            >
                                <Header>{node._display}</Header>
                            </Table.HeaderCell>
                        </Table.Row>
                        <Table.Row>
                            <Table.HeaderCell>Key</Table.HeaderCell>
                            <Table.HeaderCell>Value</Table.HeaderCell>
                        </Table.Row>
                        {Object.keys(node.properties).map((key: string, index: number) => (
                            <Table.Row key={index}>
                                <Table.Cell>{snakeToSpaced(key)}</Table.Cell>
                                <Table.Cell style={{ wordBreak: "break-all" }}>
                                    {/* JSON Stringify any null or empty objects */
                                    node.properties[key] === null ||
                                    typeof node.properties[key] === "object"
                                        ? JSON.stringify(node.properties[key])
                                        : node.properties[key]}
                                </Table.Cell>
                            </Table.Row>
                        ))}
                    </Table.Header>
                </Table>
            );
        }
    }
}
