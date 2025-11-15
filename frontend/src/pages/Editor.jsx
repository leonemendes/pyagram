import React, { useCallback } from 'react';
import ReactFlow, {
  addEdge,
  Background,
  Controls,
  useNodesState,
  useEdgesState,
  Handle,
  Position
} from 'reactflow';
import 'reactflow/dist/style.css';
import { useWorkflowStore } from '../store/useWorkflowStore.js';
import Toolbar from '../components/Toolbar.jsx';

function LogicNode({ data }) {
  return (
    <div className="bg-white border-2 border-blue-500 rounded p-2 text-sm w-32 text-center shadow-md">
      <div className="font-bold text-blue-700">{data.label}</div>
      <Handle type="target" position={Position.Top} />
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
}

const nodeTypes = { logic: LogicNode };

export default function Editor() {
  const { nodes, edges, setNodes, setEdges } = useWorkflowStore();

  // ReactFlow requires local controlled states
  const [rfNodes, setRfNodes, onNodesChange] = useNodesState(nodes);
  const [rfEdges, setRfEdges, onEdgesChange] = useEdgesState(edges);

  // Sync Zustand store with ReactFlow state
  React.useEffect(() => {
    setNodes(rfNodes);
    setEdges(rfEdges);
  }, [rfNodes, rfEdges, setNodes, setEdges]);

  const onConnect = useCallback(
    (params) => setRfEdges((eds) => addEdge(params, eds)),
    [setRfEdges]
  );

  const handleAddNode = (type) => {
    const id = String(Date.now());
    const newNode = {
      id,
      type: 'logic',
      data: { label: type.toUpperCase() },
      // Position always defined, never undefined
      position: {
        x: 150 + Math.random() * 300,
        y: 80 + Math.random() * 200,
      },
    };
    setRfNodes((nds) => nds.concat(newNode));
  };

  // Safety fallback — avoids undefined nodes
  const safeNodes = Array.isArray(rfNodes)
    ? rfNodes.filter((n) => n && n.position && typeof n.position.x === 'number')
    : [];

  return (
    <div className="w-full h-full flex bg-gray-100">
      <Toolbar onAddNode={handleAddNode} />
      <div className="flex-1 bg-white">
        <ReactFlow
          nodes={safeNodes}
          edges={rfEdges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          nodeTypes={nodeTypes}
          fitView
        >
          <Background />
          <Controls />
        </ReactFlow>
      </div>
    </div>
  );
}
