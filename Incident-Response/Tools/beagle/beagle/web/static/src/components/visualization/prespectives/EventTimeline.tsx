import * as _ from 'lodash';
import * as React from 'react';
import Timeline from 'react-visjs-timeline';
import { Edge, Node } from 'src/models';
import { TimelineGroup, TimelineItem } from 'vis';

interface EventTimelineProps {
    visibleNodes: Node[];
    visibleEdges: Edge[];
}

interface EventTimelineState {
    items: TimelineItem[];
    groups: TimelineGroup[];
}

export default class EventTimeline extends React.Component<EventTimelineProps, EventTimelineState> {
    public static getDerivedStateFromProps(props: EventTimelineProps) {
        let idx = 0;

        function transformEdge(edge: Edge): TimelineItem[] | undefined {
            const targetNode = _.find(props.visibleNodes, { id: edge.to });

            if (
                _.isNil(edge) ||
                _.isUndefined(targetNode) ||
                !("properties" in edge) ||
                edge.properties.data.length === 0 // Edge with no data, for example, a file of edge.
            ) {
                return undefined;
            }

            return edge.properties.data
                .filter(properties => !_.isNil(properties) && "timestamp" in properties)
                .map(edgeInfo => {
                    const date = new Date(0);
                    date.setUTCSeconds(edgeInfo.timestamp);

                    return {
                        id: idx++,
                        content: targetNode._display + " <span>(" + edge.label + ")</span>",
                        start: date,
                        group: edge.label,
                        style: "background-color: " + targetNode.color
                    };
                });
        }

        const items = _.compact(_.flattenDeep(props.visibleEdges.map(transformEdge)));

        return {
            items,
            groups: _.map(_.uniq(_.map(items, "group")), (ele: string) => ({
                id: ele,
                content: ele
            }))
        };
    }

    public el: vis.Timeline;

    constructor(props: EventTimelineProps) {
        super(props);

        this.state = {
            items: [],
            groups: []
        };
    }

    public render() {
        return (
            <div style={{ paddingTop: "5px" }}>
                <Timeline
                    ref={(c: any) => (c === null ? this.el == null : (this.el = c.$el))}
                    items={this.state.items}
                    groups={this.state.groups}
                    options={{
                        width: "100%",
                        maxHeight: "90vh",
                        height: "90vh",
                        verticalScroll: true,
                        type: "box",
                        showCurrentTime: false
                    }}
                />
            </div>
        );
    }
}
