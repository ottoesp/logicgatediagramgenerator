
from dag import DiagramNode, DiagramDag, get_adjacency_list, get_undirected_adjacency_list, DummyNode
from parseWff import parse_wff
from layers import get_layers, order_layers
from utils import *


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
                layers[layer_u - (i + 1)].add(dummy.get_id())

                dag.insert_edge(prev, dummy.get_id())
                prev = dummy.get_id()
            else:
                dag.insert_edge(prev, v)


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

    ordered_layers = order_layers(dag, layers, w)
    for layer in ordered_layers:
        print(layer)
    # dag.print_graph()

generate_diagram("(A and B) or (A and C) or (B and C)", 2)

generate_diagram("A and (B or (C and ((not B or C) or A)))", 5)
# generate_diagram("A")
#
# generate_diagram("((A and B) or (A and C)) or (A and not C)")
# generate_diagram("( (A or not (A and B)) or (C and not B))")