import * as _ from 'lodash';
import * as React from 'react';
import { HorizontalGridLines, makeWidthFlexible, MarkSeries, VerticalGridLines, XAxis, XYPlot, YAxis } from 'react-vis';
import { Edge } from 'src/models';

export interface EdgeTimeChartProps {
    edge: Edge;
    earliestEvent: Date;
    latestEvent: Date;
}

export default class EdgeTimeChart extends React.Component<EdgeTimeChartProps, any> {
    public constructor(props: EdgeTimeChartProps) {
        super(props);
        this.state = {
            valuke: null
        };
    }

    public setHintValue = (value: any) => {
        this.setState({ value: "foo" });
    };

    public resetHintValue = () => {
        this.setState({ value: null });
    };

    public render() {
        if (this.props.edge === undefined) {
            return "";
        } else {
            const counts = _.countBy(this.props.edge.properties.data, "timestamp");

            const data = _.toPairs(counts).map(m => {
                const date = new Date(0);
                date.setUTCSeconds(Number(m[0]));
                return {
                    x: date,
                    y: m[1]
                };
            });

            const XYPlotFlex = makeWidthFlexible(XYPlot);
            return (
                <XYPlotFlex
                    xType="time"
                    xDomain={[this.props.earliestEvent, this.props.latestEvent]}
                    height={300}
                    margin={{ bottom: 70 }}
                >
                    <HorizontalGridLines />
                    <VerticalGridLines />
                    <XAxis title="Time" tickLabelAngle={-45} />
                    <YAxis />
                    <MarkSeries data={_.sortBy([...data], "x")} />
                </XYPlotFlex>
            );
        }
    }
}

// // Returns an array of dates between the two dates
// const getDatesBetween = (startDate: Date, endDate: Date) => {
//     const dates = [];

//     // Strip hours minutes seconds etc.

//     let currentDate = new Date(startDate.getFullYear(), startDate.getMonth(), startDate.getDate());

//     while (currentDate <= endDate) {
//         dates.push(currentDate);

//         currentDate = new Date(
//             currentDate.getFullYear(),
//             currentDate.getMonth(),
//             currentDate.getDate() + 1 // Will increase month if over range
//         );
//     }

//     return dates;
// };
