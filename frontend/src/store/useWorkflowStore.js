import { create } from 'zustand';

export const useWorkflowStore = create((set) => ({
  nodes: [], // 👈 começa vazio
  edges: [],
  setNodes: (fnOrArray) =>
    set((state) => ({
      nodes:
        typeof fnOrArray === 'function'
          ? fnOrArray(state.nodes)
          : Array.isArray(fnOrArray)
            ? fnOrArray
            : [],
    })),
  setEdges: (fnOrArray) =>
    set((state) => ({
      edges:
        typeof fnOrArray === 'function'
          ? fnOrArray(state.edges)
          : Array.isArray(fnOrArray)
            ? fnOrArray
            : [],
    })),
}));
