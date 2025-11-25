from autoArrange.topo import kahns_topological_sort, lex_cmp, transitive_reduction
from functools import reduce
from dag import DiagramNode, DiagramDag, get_adjacency_list, get_undirected_adjacency_list, DummyNode, get_rev_adjacency_list

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
    adj: dict[str, set[str]] = get_adjacency_list(dag.get_node_ids(), dag.edges)

    # First layer is ordered lexicographically by ID (could be a better approach)
    ordered_layers: list[list[str]] = [sorted(list(unordered_layers[0]))]

    # Process each subsequent layer
    for i in range(1, len(unordered_layers)):
        current_layer = unordered_layers[i]
        ordered_child_layer = ordered_layers[i-1]

        # Create a dict of average child positions to act as a sorting key
        avg_child_positions: dict[str, float] = {}
        for node_id in current_layer:
            children = adj[node_id]

            # Calculate average position of children in previous layer 
            sum_child_pos: float = 0

            for child_id in children:
                sum_child_pos += ordered_child_layer.index(child_id)
            # Insert into dictionary
            avg_child_positions[node_id] = sum_child_pos/len(children)

        sorted_layer = sorted(current_layer, key=lambda u_id : avg_child_positions[u_id])
        ordered_layers.append(sorted_layer)

    return ordered_layers