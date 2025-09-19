from collections import defaultdict
from copy import deepcopy
from typing import Tuple

class DiagramNode:
    nextId = 0
    variables = []
    def __init__(self, name):
        self.name = name
        self.id = str(DiagramNode.nextId)
        DiagramNode.nextId += 1

    def get_id(self):
        return self.id

    def __str__(self):
        return f'[{self.name}, {self.id}]'

class VariableNode(DiagramNode):
    def __init__(self, name):
        super().__init__(name)
        self.name = name
        self.id = name

class DummyNode(DiagramNode):
    def __init__(self):
        super().__init__("dummy")



class DiagramDag:
    def __init__(self):
        self.nodes: set[DiagramNode] = set()
        self.edges: set[Tuple[str, str]] = set()

    def get_node_ids(self):
        return set(map(lambda node: node.get_id(), self.nodes))

    def insert_node(self, node: DiagramNode, parent_node: DiagramNode = None):
        if node.get_id() not in self.get_node_ids():
            self.nodes.add(node)
        if parent_node is not None:
            self.edges.add((parent_node.get_id(), node.get_id()))
        return node

    def delete_edge(self, u, v):
        self.edges.remove((u, v))

    def insert_edge(self, u, v):
        self.edges.add((u, v))

    def print_nodes(self):
        for node in self.nodes:
            print(f'{node}, ', end='')
        print()

    def print_edges(self):
        print(self.edges)

def get_adjacency_list(nodes: set[str], edges: set[Tuple[str, str]]):
    adj = {u : set() for u in nodes}
    for edge in edges:
        adj[edge[0]].add(edge[1])
    return adj


