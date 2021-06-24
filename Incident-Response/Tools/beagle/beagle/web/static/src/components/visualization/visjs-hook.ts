import { Network } from 'vis';

let network: Network;

export const initVisjsControl = (visJSNetwork: Network): void => {
    network = visJSNetwork;
};

export const getNodeAt = (event: vis.Position) => {
    return network.getNodeAt(event);
};

export const freezeGraph = () => {
    network.stopSimulation();
};

export const highlightNode = (node: number) => {
    network.selectNodes([node]);
};
