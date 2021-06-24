import { Edge, Node } from 'src/models';

export default interface Mutator {
    name: string;
    category: string;
    mutate: (
        visibleNodes: Node[],
        visibleEdges: Edge[],
        visibleNodeTypes: string[],
        visibleEdgeTypes: string[],
        nodes: Node[],
        edges: Edge[],
        selectedNode?: number,
        selectedEdge?: number
    ) => { visibleNodes: Node[]; visibleEdges: Edge[] };
}
