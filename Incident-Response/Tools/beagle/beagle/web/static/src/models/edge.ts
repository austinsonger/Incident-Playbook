interface EdgeProps {
    data: any[];
}
export default interface Edge {
    id: number;
    from: number;
    to: number;
    label: string;
    properties: EdgeProps;
}
