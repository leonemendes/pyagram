"""
Workflow execution engine.

This module evaluates workflow graphs built in the frontend (ReactFlow)
and sent to the backend through the /run endpoint.

Each node represents a logical or computational operation (AND, OR, NOT, IF, etc.).
Connections define data flow between nodes.
Inputs are given by name and can be provided as constants.
"""

from typing import Dict, Any, List, Callable
from core.model.workflow import Workflow


# ----------------------------------------------------------------------
# Supported logical operators
# ----------------------------------------------------------------------
OPS: Dict[str, Callable[..., Any]] = {
    "AND": lambda *args: all(args),
    "OR": lambda *args: any(args),
    "NOT": lambda x: not x,
    "IF": lambda cond, a, b: a if cond else b,
}


class WorkflowExecutor:
    """Interprets and executes a Workflow graph."""

    def __init__(self, workflow: Workflow):
        self.workflow = workflow

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _build_connection_map(self) -> Dict[str, List[str]]:
        """
        Build a mapping of target -> [source_ids] from workflow connections.
        Example:
            A -> N1, B -> N1   =>  { "N1": ["A", "B"] }
        """
        connection_map: Dict[str, List[str]] = {}
        for c in self.workflow.connections:
            connection_map.setdefault(c.target, []).append(c.source)
        return connection_map

    # ------------------------------------------------------------------
    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the workflow graph using the provided input values.

        Parameters
        ----------
        inputs : dict
            External input values, e.g. {"A": True, "B": False}

        Returns
        -------
        dict
            The final context containing all computed values and a trace.
        """
        context: Dict[str, Any] = dict(inputs)
        connection_map = self._build_connection_map()
        nodes = {n.id: n for n in self.workflow.nodes}
        trace: List[Dict[str, Any]] = []

        def evaluate(node_id: str) -> Any:
            # Use cached value if already evaluated
            if node_id in context:
                return context[node_id]

            node = nodes.get(node_id)
            if not node:
                # If it's not a node, assume it is an input constant
                return context.get(node_id, False)

            fn = OPS.get(node.type.upper())
            if not fn:
                raise ValueError(f"Unknown node type: {node.type}")

            # Recursively evaluate all upstream sources
            sources = connection_map.get(node_id, [])
            args = [evaluate(src) for src in sources]

            # Execute operator
            try:
                result = fn(*args)
            except Exception as exc:
                raise RuntimeError(
                    f"Failed to execute node {node.id} ({node.type}): {exc}"
                ) from exc

            # Save in context
            context[node.id] = result

            # Append to trace for debugging or visualization
            trace.append(
                {
                    "node": node.id,
                    "type": node.type,
                    "inputs": args,
                    "result": result,
                }
            )

            return result

        # Determine terminal nodes (no outgoing edges)
        all_targets = {c.target for c in self.workflow.connections}
        all_sources = {c.source for c in self.workflow.connections}
        terminal_nodes = [nid for nid in all_sources if nid not in all_targets]

        # Evaluate all terminal nodes
        for node_id in terminal_nodes:
            evaluate(node_id)

        return {"context": context, "trace": trace}
