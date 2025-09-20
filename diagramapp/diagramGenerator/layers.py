from topo import kahns_topological_sort, lex_cmp, transitive_reduction
from functools import reduce
from dag import DiagramNode, DiagramDag, get_adjacency_list, get_undirected_adjacency_list, DummyNode
import numpy as np


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

def order_layers(dag: DiagramDag, unordered_layers: list[set[str]], w):

    def space_evenly(n, i, d):
        if n == 1:
            return 0
        else:
            return (i * d)//(n - 1)

    max_width = reduce(lambda max_w, layer: max(max_w, len(layer)), unordered_layers, 0)
    max_width = int(np.lcm.reduce([len(layer) for layer in unordered_layers]))

    adj = get_undirected_adjacency_list(dag.get_node_ids(), dag.edges)
    ordered_layers = [
        [[u, space_evenly(len(unordered_layers[0]), i, max_width)] for i, u in enumerate(unordered_layers[0])]]

    for i in range(1, len(unordered_layers)):
        lower_layer = ordered_layers[i - 1]

        ordered_layers.append([[u, -1] for i, u in enumerate(unordered_layers[i])])
        current_layer = ordered_layers[i]

        # Check directions of edges and layers that dummys are entering
        for u in current_layer:
            neighbour_x_sum = 0
            num_neighbours = 0
            for v in lower_layer:
                # If the node is adjacent
                if v[0] in adj[u[0]]:
                    # Then add its x value to the sum
                    neighbour_x_sum += v[1]
                    num_neighbours += 1
            u[1] = neighbour_x_sum/num_neighbours

        current_layer.sort(key=lambda u: u[1])

        for j, u in enumerate(current_layer):
            u[1] = space_evenly(len(current_layer), j, max_width)

    return ordered_layers