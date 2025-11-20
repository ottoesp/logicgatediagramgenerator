from autoArrange.topo import kahns_topological_sort, lex_cmp, transitive_reduction
from functools import reduce
from dag import DiagramNode, DiagramDag, get_adjacency_list, get_undirected_adjacency_list, DummyNode

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
    unordered_layers: list[set[str]],
    w
) -> list[list[tuple[str, int]]]:

    # Compute maximum layer width
    max_width: int = reduce(lambda max_w, layer: max(max_w, len(layer)), unordered_layers, 0)

    # Build adjacency list
    adj: dict[str, set[str]] = get_undirected_adjacency_list(dag.get_node_ids(), dag.edges)

    # First layer: center it horizontally
    first_layer = [
        (u, i + (max_width - len(unordered_layers[0])) // 2)
        for i, u in enumerate(unordered_layers[0])
    ]
    ordered_layers: list[list[tuple[str, int]]] = [first_layer]

    # Process each subsequent layer
    for i in range(1, len(unordered_layers)):
        lower_layer: list[tuple[str, int]] = ordered_layers[i - 1]

        # Start with placeholder x = -1
        current_layer: list[tuple[str, int]] = [(u, -1) for u in unordered_layers[i]]

        # Compute barycentric x-positions
        updated_layer: list[tuple[str, int]] = []
        for (u, _) in current_layer:
            neighbour_x_sum = 0
            num_neighbours = 0

            for (v, x_v) in lower_layer:
                if v in adj[u]:
                    neighbour_x_sum += x_v
                    num_neighbours += 1

            if num_neighbours > 0:
                x = neighbour_x_sum // num_neighbours
            else:
                x = 0  # Fallback if isolated; replace with a better heuristic if wanted

            updated_layer.append((u, x))

        # Sort by computed x
        updated_layer.sort(key=lambda item: item[1])

        # Convert x values into centered integer positions
        offset = (max_width - len(updated_layer)) // 2
        final_layer = [(u, j + offset) for j, (u, _) in enumerate(updated_layer)]

        ordered_layers.append(final_layer)

    return ordered_layers