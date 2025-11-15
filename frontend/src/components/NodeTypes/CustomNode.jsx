import React from 'react';
import { Handle, Position } from 'reactflow';

export default function CustomNode({ data }) {
    return (
        <div className="p-2 bg-white border rounded shadow-sm text-sm text-gray-800">
            <div className="font-semibold">{data.label || 'Custom Node'}</div>
            <Handle type="target" position={Position.Top} />
            <Handle type="source" position={Position.Bottom} />
        </div>
    );
}
