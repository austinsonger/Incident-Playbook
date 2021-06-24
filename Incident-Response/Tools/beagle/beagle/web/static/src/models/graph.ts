import { Edge, Node } from '.';

export default interface Graph {
    directed: boolean;
    multigraph: boolean;
    graph: object;
    nodes: Node[];
    edges: Edge[];
}
