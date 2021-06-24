import { Edge, Node } from '../../../models';

export interface VizProps {
    visibleEdges: Edge[];
    visibleNodes: Node[];
}

export interface GraphEvent {
    nodes: number[];
    edges: number[];
}
