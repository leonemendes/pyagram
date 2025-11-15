# core/model/workflow.py
from typing import List, Dict, Callable

class Node:
    def __init__(self, node_id: str, type_: str, inputs: List[str], outputs: List[str]):
        self.id = node_id
        self.type = type_
        self.inputs = inputs
        self.outputs = outputs

class Connection:
    def __init__(self, source: str, target: str):
        self.source = source
        self.target = target

class Workflow:
    def __init__(self):
        self.nodes: List[Node] = []
        self.connections: List[Connection] = []

    def to_dict(self):
        return {
            "nodes": [n.__dict__ for n in self.nodes],
            "connections": [c.__dict__ for c in self.connections]
        }

    @staticmethod
    def from_dict(data: Dict):
        wf = Workflow()
        for n in data["nodes"]:
            wf.nodes.append(Node(n["id"], n["type"], n["inputs"], n["outputs"]))
        for c in data["connections"]:
            wf.connections.append(Connection(c["source"], c["target"]))
        return wf
