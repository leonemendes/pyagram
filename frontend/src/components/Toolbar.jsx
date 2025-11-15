import React from 'react';

export default function Toolbar({ onAddNode }) {
    const nodes = ['AND', 'OR', 'NOT', 'IF'];

    return (
        <div className="w-36 bg-white border-r p-3 shadow">
            <div className="font-semibold mb-3 text-gray-800 text-center">Blocks</div>
            {nodes.map((type) => (
                <button
                    key={type}
                    onClick={() => onAddNode(type)}
                    className="w-full mb-2 bg-blue-600 text-white p-2 rounded hover:bg-blue-700 transition"
                >
                    + {type}
                </button>
            ))}
        </div>
    );
}
