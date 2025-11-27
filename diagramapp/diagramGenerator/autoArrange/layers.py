from ..autoArrange.topo import kahns_topological_sort, lex_cmp, transitive_reduction
from functools import reduce
from ..dag import DiagramNode, DiagramDag, get_adjacency_list, get_undirected_adjacency_list, DummyNode, get_rev_adjacency_list

def get_layers(dag: DiagramDag, w:int):
    _, edges_reduced = transitive_reduction(dag)
    topo = kahns_topological_sort(dag.get_node_ids(), edges_reduced)

    layers: list[set[str]] = [set()]
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

def order_layers(
    dag: "DiagramDag",
    unordered_layers: list[set[str]]
) -> list[list[str]]:

    # Build adjacency list
    adj = dag.get_rev_adjacency_list()

    # We build ordered layers in reverse, first we add the target node
    ordered_layers: list[list[str]] = [[] for layer in unordered_layers]
    ordered_layers[-1] = list(unordered_layers[-1])

    # Process each layer in reverse order from the second last layer
    for i in range(len(unordered_layers) - 2, -1, -1):
        left_layer = unordered_layers[i]
        right_layer = ordered_layers[i + 1]

        # Create a dict of average child positions to act as a sorting key
        avg_parent_positions: dict[str, float] = {}
        for node_id in left_layer:
            parents = adj[node_id]

            # Calculate average position of children in previous layer 
            sum_parent_pos: float = 0

            for parent_id in parents:
                sum_parent_pos += right_layer.index(parent_id)
            # Insert into dictionary
            avg_parent_positions[node_id] = sum_parent_pos/len(parents)

        sorted_layer = sorted(left_layer, key=lambda u_id : avg_parent_positions[u_id])
        ordered_layers[i] = sorted_layer

    return ordered_layers