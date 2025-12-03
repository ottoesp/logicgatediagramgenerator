from ..dag import DiagramDag
from ..utils import max_len_of_arrays
from ..nodeType import VERTICAL_SIZE, PREFERS_OFFSET
from ..render.rendervars import *
import sys

INT_INF = sys.maxsize
N_ADJUST_PASSES = 3

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

def offset_if_inline_with_non_neighbour(dag: DiagramDag, left_layer: list[str], right_layer: list[str], positions: list[int]):
    adj = dag.get_rev_adjacency_list()

    # For each node, if node is in-line with non-neighbour, offset
    for i, left_id in enumerate(left_layer):
        # Non neighbours is the set difference of neighbours and all ids
        non_neighbour_ids = (dag.get_node_ids() & set(right_layer)) - adj[left_id]
        
        non_neighbours = [dag.get_node_by_id(right_id) for right_id in non_neighbour_ids]
        for node in non_neighbours:
            if positions[i] in range(node.x, node.x + VERTICAL_SIZE[node.nodeType] - 1):
                # Offset this and all further nodes in the layer
                for j in range(i, len(positions)):
                    positions[j] += VERTICAL_SIZE[node.nodeType]

                break


def align_inline_with_neighbour(dag: DiagramDag, left_layer: list[str], positions: list[int]):
    forward_adj = dag.get_adjacency_list()
    reversed_adj = dag.get_rev_adjacency_list()

    # For each node, if node can be in-line with neighbour without intersection, make inline
    for i, left_id in enumerate(left_layer):
        neighbours = [dag.get_node_by_id(right_id) for right_id in reversed_adj[left_id]]
        left_node = dag.get_node_by_id(left_id)
        
        # Calculate the range of positions the node may take without overlapping
        bounded_above = 0 if i == 0 else positions[i - 1] + VERTICAL_SIZE[dag.get_node_by_id(left_layer[i - 1]).nodeType] + NODE_X_BETWEEN
        bounded_below = INT_INF if i == len(left_layer) - 1 else positions[i + 1] - (VERTICAL_SIZE[left_node.nodeType] + NODE_X_BETWEEN)

        # Find a neighbour with an x value within that range and set it as the new position
        for neighbour in neighbours:

            # Determine whether it is better to place it in-line with the top or bottom of the neighbour
            siblings = forward_adj[neighbour.id]
            if len(siblings) <= 1:
                # It has no siblings so put in-line
                try_x = neighbour.x
            else:
                first_sibling = list(siblings - {left_id})[0]
                sibling_x = positions[left_layer.index(first_sibling)] 
                
                if sibling_x < positions[i]:
                    # Sibling is above so better to offset
                    try_x = neighbour.x + 1
                else:
                    try_x = neighbour.x

            if try_x <= bounded_below and try_x >= bounded_above:
                positions[i] = try_x
                break
          
def determine_layer_y_coordinates(layers: list[list[str]]) -> list[int]:
    y_vals = [0 for _ in layers]

    y_offset = 0

    for i, layer in enumerate(layers):
        y_vals[i] = y_offset
        y_offset += NODE_Y_MAX_SIZE + len(layer) * LINE_Y_SPACING + 2 * EDGE_Y_SPACING
 
    return y_vals
  

def assign_coordinates(dag: DiagramDag, layers: list[list[str]], x_spacing: int):
    max_len_layer = max_len_of_arrays(layers)

    layer_y_coordinates = determine_layer_y_coordinates(layers)
    
    # Set the end node to be centred
    root = dag.get_node_by_id(layers[-1][0])
    root.set_coordinates(max_len_layer*x_spacing // 2, layer_y_coordinates[-1])

    # Loop through the layers backwards from the second last    
    for layer_idx in range(len(layers) - 2, -1, -1):
        left_layer = layers[layer_idx]
        right_layer = layers[layer_idx + 1]

        # Calculate intitial positioning
        positions = [pos * x_spacing for pos in space_around(len(left_layer), max_len_layer)]
        
        offset_if_inline_with_non_neighbour(dag, left_layer, right_layer, positions)
        for _ in range(N_ADJUST_PASSES):
            align_inline_with_neighbour(dag, left_layer, positions)

        # Set the coordinates of each node
        for i, left_id in enumerate(left_layer):
            dag.get_node_by_id(left_id).set_coordinates(positions[i], layer_y_coordinates[layer_idx])

    return layer_y_coordinates

    