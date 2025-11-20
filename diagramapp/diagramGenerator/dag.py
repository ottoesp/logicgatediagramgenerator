from typing import Tuple
from nodeType import NodeType
from diagramNode import *

class DiagramDag:
    def __init__(self) -> None:
        self.nodes: set[DiagramNode] = set()
        self.edges: set[Tuple[str, str]] = set()
        reset_id_counter()

    def get_node_ids(self):
        return set(map(lambda node: node.get_id(), self.nodes))

    def get_nodes(self):
        return self.nodes

    def insert_node(self, node: DiagramNode, parent_node: DiagramNode | None = None):
        if node.get_id() not in self.get_node_ids():
            self.nodes.add(node)
        if parent_node is not None:
            self.edges.add((parent_node.get_id(), node.get_id()))
        return node

    def delete_edge(self, u, v):
        self.edges.remove((u, v))

    def insert_edge(self, u, v):
        self.edges.add((u, v))

    def get_node_by_id(self, node_id) -> DiagramNode|None:
        for node in self.nodes:
            if node.get_id() == node_id:
                return node
        return None

    def print_nodes(self):
        for node in sorted(self.nodes, key=lambda n: n.id):
            print(f'{node}, ', end='')
        print()

    def print_edges(self):
        print(self.edges)

    def print_graph(self):
        adj = get_adjacency_list(self.get_node_ids(), self.edges)
        for node in sorted(self.nodes, key=lambda n: n.id):
            print(node)
            print(f'   {adj[node.id]}')

    def get_adjacency_list(self):
        return get_adjacency_list(self.get_node_ids(), self.edges)

    def get_rev_adjacency_list(self):
        return get_rev_adjacency_list(self.get_node_ids(), self.edges)

def get_adjacency_list(nodes: set[str], edges: set[Tuple[str, str]]):
    adj: dict[str, set[str]] = {u : set() for u in nodes}
    for edge in edges:
        adj[edge[0]].add(edge[1])
    return adj

def get_rev_adjacency_list(nodes: set[str], edges: set[Tuple[str, str]]):
    adj: dict[str, set[str]] = {u: set() for u in nodes}
    for edge in edges:
        adj[edge[1]].add(edge[0])
    return adj

def get_undirected_adjacency_list(nodes: set[str], edges: set[Tuple[str, str]]):
    adj: dict[str, set[str]] = {u: set() for u in nodes}
    for edge in edges:
        adj[edge[0]].add(edge[1])
        adj[edge[1]].add(edge[0])
    return adj
