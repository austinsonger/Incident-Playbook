import * as _ from 'lodash';
import { Edge, Node } from 'src/models';
import { updateVisibleEdges } from 'src/reducers/visibleGraph';

import Mutator from '..';

export default class ForwardTravel implements Mutator {
    public name = "Forward Fanout";
    public category = "Traversal";

    public mutate = (
        visibleNodes: Node[],
        visibleEdges: Edge[],
        visibleNodeTypes: string[],
        visibleEdgeTypes: string[],
        nodes: Node[],
        edges: Edge[],
        selectedNode: number
    ) => {
        if (selectedNode === undefined) {
            return { visibleNodes, visibleEdges };
        }

        const queue: number[] = [selectedNode];
        const nodesToAdd: number[] = [];

        while (queue.length !== 0) {
            const curr = queue.pop();
            const candidates = edges
                .filter(e => e.from === curr)
                .filter(e => _.includes(visibleEdgeTypes, e.label))
                .map(e => e.to)
                .filter(n => !_.includes(nodesToAdd, n));

            // Add to the list of nodes to add
            candidates.forEach(n => nodesToAdd.push(n));

            // Add elements to the queue
            candidates.filter(n => !_.includes(queue, n)).forEach(n => queue.push(n));
        }

        // Remove null elements
        const newNodes = nodesToAdd.map(n => _.find(nodes, { id: n }));

        // Set the new visibleNodes
        visibleNodes = _.uniqBy([...visibleNodes, ..._.compact(newNodes)], "id");

        // Update the visible edges.
        visibleEdges = _.uniqBy(
            [...visibleEdges, ...updateVisibleEdges(visibleNodes, edges)],
            "id"
        );

        return { visibleNodes, visibleEdges };
    };
}
