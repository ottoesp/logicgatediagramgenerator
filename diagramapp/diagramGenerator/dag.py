from typing import Tuple
from nodeType import NodeType

def reset_id_counter():
    DiagramNode.nextId = 0


class DiagramNode:
    nextId = 0
    def __init__(self, nodeType : NodeType):
        self.nodeType : NodeType = nodeType
        self.id = str(DiagramNode.nextId)
        DiagramNode.nextId += 1
        self.x = None
        self.y = None

    def get_id(self):
        return self.id

    def set_coordinates(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'[{self.nodeType.name}, {self.id}]'


class VariableNode(DiagramNode):
    def __init__(self, name):
        super().__init__(NodeType.VARIABLE)
        self.name = name
        self.id = name


class DummyNode(DiagramNode):
    def __init__(self):
        super().__init__(NodeType.DUMMY)

class DiagramDag:
    def __init__(self):
        self.nodes: set[DiagramNode] = set()
        self.edges: set[Tuple[str, str]] = set()
        reset_id_counter()

    def get_node_ids(self):
        return set(map(lambda node: node.get_id(), self.nodes))

    def get_nodes(self):
        return self.nodes

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
    adj = {u : set() for u in nodes}
    for edge in edges:
        adj[edge[0]].add(edge[1])
    return adj

def get_rev_adjacency_list(nodes: set[str], edges: set[Tuple[str, str]]):
    adj = {u: set() for u in nodes}
    for edge in edges:
        adj[edge[1]].add(edge[0])
    return adj

def get_undirected_adjacency_list(nodes: set[str], edges: set[Tuple[str, str]]):
    adj = {u: set() for u in nodes}
    for edge in edges:
        adj[edge[0]].add(edge[1])
        adj[edge[1]].add(edge[0])
    return adj
