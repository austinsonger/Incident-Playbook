import * as React from 'react';
import { Dimmer, Loader, Segment } from 'semantic-ui-react';

interface LoadingBarProps {
    text: string;
}

const LoadingBar: React.FunctionComponent<LoadingBarProps> = props => {
    return (
        <div>
            <Segment
                padded="very"
                basic={true}
                className="container"
                style={{
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                    height: "100vh"
                }}
            >
                <Dimmer active={true} inverted={true}>
                    <Loader size="huge">{props.text}</Loader>
                </Dimmer>
            </Segment>
        </div>
    );
};

export default LoadingBar;
