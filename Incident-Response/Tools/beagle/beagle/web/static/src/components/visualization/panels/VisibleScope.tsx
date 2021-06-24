import * as React from 'react';
import { Grid } from 'semantic-ui-react';

export interface VisibleScopeProps {
    visibleNodes: number;
    visibleEdges: number;
    nodes: number;
    edges: number;
    earliestEvent: Date;
    latestEvent: Date;
}

export default class VisibleScope extends React.Component<VisibleScopeProps, any> {
    public render() {
        let earliestTime = JSON.stringify(this.props.earliestEvent);
        let latestTime = JSON.stringify(this.props.latestEvent);
        if (
            this.props.earliestEvent.toString() === "Invalid Date" &&
            this.props.latestEvent.toString() === "Invalid Date"
        ) {
            earliestTime = " No Timestamps ";
            latestTime = " No Timestamps ";
        }

        return (
            <Grid columns={"equal"}>
                <Grid.Row centered={true}>
                    <Grid.Column>
                        {`Visible Nodes: ${this.props.visibleNodes}`}
                        <br />
                        {`Visible Edges: ${this.props.visibleEdges}`}
                    </Grid.Column>
                    <Grid.Column>
                        {`Total Nodes: ${this.props.nodes}`}
                        <br />
                        {`Total Edges: ${this.props.edges}`}
                    </Grid.Column>
                </Grid.Row>
                <Grid.Row>
                    <Grid.Column width={16}>
                        {`Earliest Event: ${earliestTime.slice(1, earliestTime.length - 1)}`}
                        <br />
                        {`Latest Event: ${latestTime.slice(1, latestTime.length - 1)}`}
                    </Grid.Column>
                </Grid.Row>
            </Grid>
        );
    }
}
