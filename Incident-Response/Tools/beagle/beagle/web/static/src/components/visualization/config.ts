export const GRAPH_VIZ_CONFIG = {
    nodes: {
        shape: "circle",
        shapeProperties: {
            borderDashes: [2, 0]
        },
        borderWidth: 2,
        color: {
            border: "#fff"
        },
        font: {
            size: 8
        },
        scaling: {
            label: {
                enabled: true
            }
        }
    },
    layout: {
        improvedLayout: false,
        hierarchical: false
    },
    edges: {
        color: {
            color: "#A9A9A9",
            inherit: false
        },
        font: {
            align: "horizontal"
        },
        smooth: true
    },
    physics: {
        solver: "forceAtlas2Based",
        forceAtlas2Based: {
            gravitationalConstant: -50,
            centralGravity: 0.01,
            springConstant: 0.08,
            springLength: 100,
            damping: 0.5,
            avoidOverlap: 0.5
        },
        adaptiveTimestep: true,
        stabilization: {
            iterations: 200,
            fit: true
        }
    },
    height: window.innerHeight * 0.965 + "px"
};

// Tree Viz Settings
export const TREE_VIZ_CONFIG = JSON.parse(JSON.stringify(GRAPH_VIZ_CONFIG));
TREE_VIZ_CONFIG.physics = false;
TREE_VIZ_CONFIG.layout.hierarchical = {
    enabled: true,
    sortMethod: "directed"
};
