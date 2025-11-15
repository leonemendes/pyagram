export function runWorkflow(nodes, edges, inputValues = {}) {
    const nodeMap = Object.fromEntries(nodes.map((n) => [n.id, n]));
    const connections = {};

    // Build connections between nodes
    edges.forEach((e) => {
        if (!connections[e.target]) connections[e.target] = [];
        connections[e.target].push(e.source);
    });

    function evaluate(nodeId) {
        const node = nodeMap[nodeId];
        if (!node) throw new Error(`Nde ${nodeId} not found`);
        const type = node.data.label;

        if (inputValues[nodeId] !== undefined) return inputValues[nodeId];

        const inputs = (connections[nodeId] || []).map(evaluate);

        switch (type) {
            case 'AND':
                return inputs.every(Boolean);
            case 'OR':
                return inputs.some(Boolean);
            case 'NOT':
                return !inputs[0];
            case 'IF':
                return inputs[0] ? inputs[1] : inputs[2];
            default:
                return false;
        }
    }

    // Choose the last node (no outputs) as the final output
    const targets = new Set(edges.map((e) => e.target));
    const lastNode = nodes.find((n) => !targets.has(n.id)) || nodes[nodes.length - 1];

    if (!lastNode) throw new Error('No terminal node found');
    return evaluate(lastNode.id);
}
