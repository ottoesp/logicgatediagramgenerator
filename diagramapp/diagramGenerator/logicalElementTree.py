from collections import defaultdict
from typing import Tuple

from connectives import LogicalElement

class LogElNode:
    def __init__(self):
        self.data = LogicalElement()
        self.left = None
        self.right = None


    def is_empty(self):
        return self.data.is_empty()

    def set_data(self, data):
        self.data = data

class DiagramNode:
    nextId = 0
    variables = []
    def __init__(self, name):
        self.name = name
        self.id = DiagramNode.nextId
        DiagramNode.nextId += 1

    def get_id(self):
        return self.id


class VariableNode(DiagramNode):
    def __init__(self, name):
        super().__init__(name)
        self.name = name

    def get_id(self):
        return self.name


class DiagramDag:
    def __init__(self):
        self.nodes: set[DiagramNode] = set()
        self.edges: set[Tuple[DiagramNode, DiagramNode]] = set()

        self.adj = defaultdict(list)

    def insert_node(self, node: DiagramNode, parent_node: DiagramNode = None):
        self.nodes.add(node)
        if parent_node is not None:
            self.edges.add((parent_node, node))
            self.adj[parent_node.get_id()].append(node)

