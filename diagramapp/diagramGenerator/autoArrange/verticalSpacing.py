from ..dag import DiagramDag
from ..utils import max_len_of_arrays

def space_around(len_layer: int, max_len_layer: int) -> list[int]:
    base = max_len_layer // (len_layer + 1)
    extra = max_len_layer % (len_layer + 1)

    positions = []
    pos = base
    for i in range(len_layer):
        positions.append(pos)
        pos += base + (1 if extra > 0 else 0)
        extra -= 1

    return positions

def assign_coordinates(dag: DiagramDag, layers: list[list[str]], layer_y_coordinates: list[int], x_spacing: int):
    max_len_layer = max_len_of_arrays(layers)

    root = dag.get_node_by_id(layers[-1][0])
    root.set_coordinates(max_len_layer*x_spacing//2, layer_y_coordinates[-1])
    
    for i in range(len(layers) - 2, -1, -1):
        left_layer = layers[i]
        right_layer = layers[i + 1]


    