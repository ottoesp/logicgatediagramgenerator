from copy import copy, deepcopy

from dag import DiagramNode, DiagramDag, get_adjacency_list, DummyNode
from parseWff import  parse_wff
from topo import kahns_topological_sort, lex_cmp, transitive_reduction
from functools import reduce
from utils import *


def get_layers(dag: DiagramDag, w:int):
    _, edges_reduced = transitive_reduction(dag)
    topo = kahns_topological_sort(dag.get_node_ids(), edges_reduced)

    layers = [set()]
    adj = get_adjacency_list(dag.get_node_ids(), dag.edges)
    for node in reversed(topo):
        i = 0
        neighbours = adj[node]
        while True:

            neighbours_in_higher_layers = reduce(
                lambda sum_len, layer: sum_len + len(neighbours & layer), layers[i:], 0)

            if len(layers[i]) < w and neighbours_in_higher_layers == 0:
            # if len(layers[i]) < w and len(neighbours & layers[i]) == 0:
                # If the intersection has no elements, i.e. no neighbour is in the layer
                # Then add this node to the layer
                layers[i].add(node)
                break
            if len(layers) == i + 1:
                layers.append(set())
            i += 1

    return layers

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
                layers[layer_v + i + 1].add(dummy.get_id())

                dag.insert_edge(prev, dummy.get_id())
                prev = dummy.get_id()
            else:
                dag.insert_edge(dummy.get_id(), v)

def order_layers(dag: DiagramDag, unordered_layers: list[set[str]], w):

    def space_evenly(n, i, d):
        return (i * d)/(n - 1)

    adj = get_adjacency_list(dag.get_node_ids(), dag.edges)
    ordered_layers = [(u, space_evenly(len(unordered_layers[0]), i, w)) for i, u in enumerate(unordered_layers[0])]

    for layer in unordered_layers[1:]:
        pass
    # We're trying to order based on the average of the previous layer,
    # everybody should only have neighbours one layer away so we should be able to just take average of their x
    # which creates an ordering that we can space evenly on for the next (so that it stays chill for the next ones)
    # make sure to actually add it into layers in that order


def generate_diagram(wff, w):
    """
    Then use Kahn's algorithm https://en.wikipedia.org/wiki/Topological_sorting
    for topological sorting into Coffman-Grahams Algorithm https://en.wikipedia.org/wiki/Coffman%E2%80%93Graham_algorithm
    for optimal levels
    Then https://en.wikipedia.org/wiki/Layered_graph_drawing
    """

    dag = DiagramDag()
    root = DiagramNode("init")
    dag.insert_node(root)

    parse_wff(wff, dag, root)
    layers = get_layers(dag, w)

    insert_dummy_edges(dag, layers)

    order_layers(dag, layers, w)



generate_diagram("(A and B) or (A and C) or (B and C)", 5)

# generate_diagram("A and (B or (C and ((not B or C) or A)))", 5)
# generate_diagram("A")
#
# generate_diagram("((A and B) or (A and C)) or (A and not C)")
# generate_diagram("( (A or not (A and B)) or (C and not B))")