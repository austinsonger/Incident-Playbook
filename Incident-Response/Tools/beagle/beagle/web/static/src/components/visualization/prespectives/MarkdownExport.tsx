import * as _ from 'lodash';
import * as React from 'react';
import { Button, Divider, Segment, Select } from 'semantic-ui-react';
import { Node } from 'src/models';

import { VizProps } from '.';

interface MarkdownExportState {
    h3: string;
}

const styles = {
    Markdown: {
        h3: "###"
    },
    JIRA: {
        h3: "h3. "
    }
};

export default class MarkdownExport extends React.PureComponent<VizProps, MarkdownExportState> {
    constructor(props: any) {
        super(props);

        this.state = {
            ...Object.values(styles)[0]
        };
    }

    public copy = () => {
        const segment = document.getElementById("segment");

        if (segment === null) {
            return;
        } else {
            const textField = document.createElement("textarea");
            textField.innerHTML = segment.innerText;
            document.body.appendChild(textField);
            textField.select();
            document.execCommand("copy");
            textField.remove();
        }
    };

    public nodesMDTable = () => {
        const nodeGroups = _.groupBy(this.props.visibleNodes, "_node_type");

        return _.toPairs(nodeGroups).map(pair => (
            <div key={pair[0]}>
                <div>
                    {this.state.h3} {pair[0]}
                </div>
                <div>|{Object.keys(pair[1][0].properties).join("|")}|</div>
                <div>
                    |
                    {Object.keys(pair[1][0].properties)
                        .map(__ => "--")
                        .join("|")}
                    |
                </div>
                <div>
                    {pair[1].map(node => (
                        <div key={node.id}>
                            |
                            {Object.keys(node.properties)
                                .map(k =>
                                    typeof node.properties[k] === "string"
                                        ? node.properties[k].replace("|", "\\|")
                                        : JSON.stringify(node.properties[k]).replace("|", "\\|")
                                )
                                .join("|")}
                            |
                        </div>
                    ))}
                </div>
                <br />
            </div>
        ));
    };

    public edgesMDTable = () => {
        const idsToNodes = this.props.visibleNodes.reduce((accum: object, node: Node) => {
            accum[node.id] = node;
            return accum;
        }, {});

        let edges = _.flatten(
            this.props.visibleEdges.map(e =>
                e.properties.data.length > 0
                    ? e.properties.data.map(props => {
                          const timeVar = new Date(0);
                          let timestamp = _.get(props, "timestamp", -1);

                          if (timestamp !== -1 && timestamp !== "null") {
                              timeVar.setUTCSeconds(timestamp);
                              timestamp = JSON.stringify(timeVar);
                          } else {
                              timestamp = JSON.stringify("Unknown");
                          }

                          return {
                              from: e.from,
                              to: e.to,
                              type: e.label,
                              data: JSON.stringify(_.omit(props, "timestamp")).replace("|", "\\|"),
                              timestamp: timestamp.slice(1, timestamp.length - 1)
                          };
                      })
                    : [
                          {
                              from: e.from,
                              to: e.to,
                              type: e.label,
                              data: JSON.stringify({}),
                              timestamp: "-1"
                          }
                      ]
            )
        );

        edges = _.sortBy(
            edges.map(e => ({
                ...e,
                to: idsToNodes[e.to]._display,
                from: idsToNodes[e.from]._display
            })),
            "timestamp"
        );

        return (
            <div>
                <div>{this.state.h3} Edges</div>
                <div>|{Object.keys(edges[0]).join("|")}|</div>
                <div>
                    |
                    {Object.keys(edges[0])
                        .map(__ => "--")
                        .join("|")}
                    |
                </div>
                {edges.map((e, idx) => (
                    <div key={idx}>|{Object.values(e).join("|")}|</div>
                ))}
            </div>
        );
    };

    public handleSyntaxChange = (event: React.SyntheticEvent, data: { value: string }) => {
        const nextState = styles[data.value];
        this.setState(nextState);
    };
    public render() {
        return (
            <Segment key="segment" style={{ height: "92vh", overflowY: "auto" }}>
                <Button
                    primary={true}
                    key="btn"
                    icon="copy"
                    onClick={this.copy}
                    content="Copy Table"
                />
                <Select
                    style={{ float: "right" }}
                    onChange={this.handleSyntaxChange}
                    options={Object.keys(styles).map(entry => ({
                        key: entry,
                        text: entry,
                        value: entry
                    }))}
                    placeholder="Choose markdown syntax"
                />
                <Divider />
                <div id="segment">
                    <div>{this.props.visibleNodes.length > 0 && this.nodesMDTable()}</div>
                    <div>{this.props.visibleEdges.length > 0 && this.edgesMDTable()}</div>
                </div>
            </Segment>
        );
    }
}
