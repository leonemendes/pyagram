// src/components/NodeTypes/LogicNode.jsx
import React from 'react';
import { Handle, Position } from 'reactflow';

export default function LogicNode({ data }) {
    return (
        <div className="bg-white border rounded-lg shadow p-2 text-center w-28">
            <div className="font-semibold">{data.label}</div>
            <Handle type="target" position={Position.Left} />
            <Handle type="source" position={Position.Right} />
        </div>
    );
}
