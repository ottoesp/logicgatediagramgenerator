from dag import DiagramDag

def index_of_containing_set(target: str, sets: list[set[str]]):
    for i, s in enumerate(sets):
        if target in s:
            return i
    return  -1

def get_edges_to_layer(dag: DiagramDag, layer : list[str]):
    adj = dag.get_rev_adjacency_list()
    edges: list[tuple[str, str]] = []

    for u in layer:
        # Add all the edges to list
        edges.extend([(u, v) for v in adj[u]])
    
    return edges

def generate_empty_grid(width: int, height: int, fill) -> list[list]:
    grid = []
    for i in range(height):
        grid.append([fill for _ in range(width)])
    return grid