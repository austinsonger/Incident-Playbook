import * as _ from 'lodash';
import * as React from 'react';
import { Header, Table } from 'semantic-ui-react';
import { Edge } from 'src/models';

export interface EdgeInfoTableProps {
    edge: Edge;
}

export default class EdgeInfoTable extends React.Component<EdgeInfoTableProps, any> {
    public render() {
        if (this.props.edge === undefined) {
            return (
                <Header as="h3" className="centered">
                    Click an Edge to view information
                </Header>
            );
        } else if (this.props.edge.properties.data.every(e => _.isNull(e))) {
            // If all the events are `null`, that means this edge has no underyling events.
            return (
                <Header as="h5" className="centered">
                    Edge contains no underlying events.
                </Header>
            );
        } else {
            // Clone since we modify the edge later
            const edge = _.cloneDeep(this.props.edge);

            const allKeys = new Set<string>();
            const tableData = edge.properties.data.map(entry => {
                if (_.isNull(entry)) {
                    return {};
                }
                Object.keys(entry).forEach(key => allKeys.add(_.capitalize(key)));

                if ("timestamp" in entry) {
                    const tmp = new Date(0);
                    tmp.setUTCSeconds(Number(entry.timestamp));
                    entry.timestamp = _.toString(tmp); // Display as string.
                }
                // Captialize the object keys
                return _.fromPairs(_.toPairs(entry).map(([k, v]) => [_.capitalize(k), v]));
            });

            const foundKeys = Array.from(allKeys);

            const renderBodyRow = (item: object, i: number) => {
                global.console.log(item, i);
                const r = {
                    key: `row-${i}`,
                    cells: [
                        ...Object.values(item).map(v => {
                            if (_.isNull(v)) {
                                return "";
                            } else if (_.isNumber(v)) {
                                return v;
                            }
                            const stringified = JSON.stringify(v);
                            return stringified.slice(1, stringified.length - 1);
                        })
                    ],
                    style: {
                        wordBreak: "break-all"
                    }
                };
                return r;
            };

            return (
                <Table
                    celled={true}
                    striped={true}
                    headerRow={foundKeys}
                    fixed={true}
                    tableData={tableData}
                    renderBodyRow={renderBodyRow}
                />
            );
        }
    }
}

// <Table.Header>
// <Table.Row>
//     <Table.HeaderCell colSpan="2" textAlign="center">
//         <Header>{this.props.edge.label}</Header>
//     </Table.HeaderCell>
// </Table.Row>
// <Table.Row>
//     <Table.HeaderCell>Key</Table.HeaderCell>
//     <Table.HeaderCell>Value</Table.HeaderCell>
// </Table.Row>
// {Object.keys(this.props.edge.properties).map(
//     (key: string, index: number) => (
//         <Table.Row key={index}>
//             <Table.Cell>{key}</Table.Cell>
//             <Table.Cell style={{ wordBreak: "break-all" }}>
//                 {/* JSON Stringify any null or empty objects */
//                 this.props.edge.properties[key] === null ||
//                 typeof this.props.edge.properties[key] === "object"
//                     ? JSON.stringify(this.props.edge.properties[key])
//                     : this.props.edge.properties[key]}
//             </Table.Cell>
//         </Table.Row>
//     )
// )}
// </Table.Header>
