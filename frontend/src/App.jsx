import { useWorkflowStore } from './store/useWorkflowStore.js';
import Editor from './pages/Editor.jsx';
import { useState } from 'react';
import { runWorkflow } from './utils/workflowRunner.js';

function App() {
  const { nodes, edges } = useWorkflowStore();
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleRun = async () => {
    try {
      // Simple example: fixed boolean inputs (later you can create A/B input blocks)
      const inputs = { A: true, B: false, C: true };

      const output = runWorkflow(nodes, edges, inputs);
      console.log('✅ Workflow result:', output);

      setResult(output);
      setError(null);
    } catch (err) {
      console.error('❌ Workflow error:', err);
      setError(err.message);
    }
  };

  return (
    <div className="flex flex-col h-screen">
      {/* Top Bar */}
      <div className="p-4 border-b bg-gray-100 flex items-center gap-2">
        <button
          onClick={handleRun}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          ▶ Run Workflow
        </button>

        {result !== null && (
          <span className="ml-4 text-green-700 font-semibold">
            Result: {String(result)}
          </span>
        )}

        {error && (
          <span className="ml-4 text-red-600 font-semibold">❌ {error}</span>
        )}
      </div>

      {/* Canvas */}
      <div className="flex-1">
        <Editor />
      </div>
    </div>
  );
}

export default App;
