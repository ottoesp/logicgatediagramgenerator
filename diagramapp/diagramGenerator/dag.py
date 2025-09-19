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

class VariableNode(DiagramNode):
    def __init__(self, name):
        super().__init__(name)
        self.name = name
        self.id = name

class DiagramDag:
    def __init__(self):
        self.nodes: set[DiagramNode] = set()
        self.edges: set[Tuple[str, str]] = set()

        self.adj = defaultdict(list)

    def get_node_ids(self):
        return map(lambda node: node.get_id(), self.nodes)

    def insert_node(self, node: DiagramNode, parent_node: DiagramNode = None):
        if node.get_id() not in self.get_node_ids():
            self.nodes.add(node)
        if parent_node is not None:
            self.edges.add((parent_node.get_id(), node.get_id()))
            self.adj[parent_node.get_id()].append(node.get_id())
        return node

    def print_graph(self):
        for node in self.nodes:
            print(f'{node.get_id()} {node.name}')
            for child in self.adj[node.get_id()]:
                print(f'   -> {child}')
            print('\n--------------')

    def print_nodes(self):
        for node in self.nodes:
            print(f'{node.name}, ', end='')
        print()

    def print_edges(self):
        print(self.edges)

    def get_nodes_without_incoming_edge(self, edges, nodes):
        return set(self.get_node_ids()).difference(set(map(lambda edge: edge[1], self.edges)))

    def get_topological_ordering(self):
        l = list()
        visited = set()

        def visit(n):
            if n in visited:
                return

            for m in self.adj[n]:
                visit(m)

            visited.add(n)
            l.append(n)

        for node in self.get_node_ids():
            if node not in visited:
                visit(node)

        return l







