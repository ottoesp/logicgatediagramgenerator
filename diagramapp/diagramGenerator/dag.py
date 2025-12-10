from typing import Tuple
from .nodeType import NodeType, SINGLE_INPUT_GATES, DOUBLE_INPUT_GATES
from .diagramNode import *

def index_of_containing_set(target: str, sets: list[set[str]]):
    for i, s in enumerate(sets):
        if target in s:
            return i
    return  -1

class DiagramDag:
    def __init__(self) -> None:
        self.nodes: set[DiagramNode] = set()
        self.edges: set[Tuple[str, str]] = set()

        self.adj: dict[str, set[str]] | None = None
        self.rev_adj: dict[str, set[str]] | None = None

        self.node_lookup: dict[str, DiagramNode] = {}
        reset_id_counter()

    def get_node_ids(self):
        return set(map(lambda node: node.id, self.nodes))

    def get_nodes(self):
        return self.nodes

    def insert_node(self, node: DiagramNode, parent_node: DiagramNode | None = None):
        if node.id not in self.get_node_ids():
            self.nodes.add(node)
            self.node_lookup[node.id] = node
        if parent_node is not None:
            self.edges.add((parent_node.id, node.id))
        return node

    def delete_edge(self, u, v):
        self.edges.remove((u, v))

    def insert_edge(self, u, v):
        self.edges.add((u, v))

    def get_node_by_id(self, node_id) -> DiagramNode:
        return self.node_lookup[node_id]

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

    def get_adjacency_list(self) -> dict[str, set[str]]:
        if self.adj is None:
            self.adj = get_adjacency_list(self.get_node_ids(), self.edges)
        return self.adj

    def get_rev_adjacency_list(self) -> dict[str, set[str]]:
        if self.rev_adj is None:
            self.rev_adj = get_rev_adjacency_list(self.get_node_ids(), self.edges)
        return self.rev_adj

def get_adjacency_list(nodes: set[str], edges: set[Tuple[str, str]]):
    adj: dict[str, set[str]] = {u : set() for u in nodes}
    for edge in edges:
        adj[edge[0]].add(edge[1])
    return adj

def get_rev_adjacency_list(nodes: set[str], edges: set[Tuple[str, str]]) -> dict[str, set[str]]:
    adj: dict[str, set[str]] = {u: set() for u in nodes}
    for edge in edges:
        adj[edge[1]].add(edge[0])
    return adj

def get_undirected_adjacency_list(nodes: set[str], edges: set[Tuple[str, str]]) -> dict[str, set[str]]:
    adj: dict[str, set[str]] = {u: set() for u in nodes}
    for edge in edges:
        adj[edge[0]].add(edge[1])
        adj[edge[1]].add(edge[0])
    return adj

def insert_dummy_edges(dag, layers):
    for edge in set(dag.edges):
        u, v = edge
        layer_u = index_of_containing_set(u, layers)
        layer_v = index_of_containing_set(v, layers)

        distance = layer_u-layer_v

        if distance > 1:
            dag.delete_edge(u, v)
            prev = u
            for i in range(distance - 1):
                dummy = DummyNode()

                dag.insert_node(dummy)
                layers[layer_u - (i + 1)].add(dummy.id)

                dag.insert_edge(prev, dummy.id)
                prev = dummy.id
            else:
                dag.insert_edge(prev, v)

type ParseTree = tuple[NodeType, ParseTree, ParseTree] | tuple[NodeType, ParseTree] | tuple[NodeType, str]

def build_dag_recur(dag: DiagramDag, parent: DiagramNode, parse_tree: ParseTree) -> None:
    if parse_tree[0] == NodeType.VARIABLE:
        # Variables are treated differently since they are grouped by name
        dag.insert_node(VariableNode(parse_tree[1]), parent)
    elif parse_tree[0] in SINGLE_INPUT_GATES:
        new_node = DiagramNode(parse_tree[0])
        dag.insert_node(new_node, parent)
        build_dag_recur(dag, new_node, parse_tree[1]) # type: ignore
    else:
        new_node = DiagramNode(parse_tree[0])
        dag.insert_node(new_node, parent)
        build_dag_recur(dag, new_node, parse_tree[1]) # type: ignore
        build_dag_recur(dag, new_node, parse_tree[2]) # type: ignore

def build_dag_from_parse_tree(parse_tree: ParseTree) -> DiagramDag:
    dag = DiagramDag()

    root = RootNode()
    dag.insert_node(root)

    build_dag_recur(dag, root, parse_tree)

    return dag