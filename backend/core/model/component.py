# core/model/component.py
from typing import List, Dict
from enum import Enum

class Direction(Enum):
    IN = 0
    OUT = 1

class Port:
    def __init__(self, name: str, direction: Direction, datatype: str = "bool"):
        self.name = name
        self.direction = direction
        self.datatype = datatype

class Component:
    def __init__(self, name: str):
        self.name = name
        self.ports: List[Port] = []
        self.subcomponents: List["Component"] = []
        self.connections: List[Dict] = []

    def add_port(self, port: Port):
        self.ports.append(port)

    def connect(self, src: str, dst: str):
        self.connections.append({"from": src, "to": dst})
