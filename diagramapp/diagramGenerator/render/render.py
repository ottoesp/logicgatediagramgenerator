from copy import deepcopy
from dag import DiagramDag, DiagramNode, get_adjacency_list
from functools import reduce
from .grid import Grid
from .charsets import default_charset, debug_charset
from nodeType import NodeType
from .path import Gutter
from .rendervars import *
from utils import get_edges_to_layer, max_len_of_arrays
from collections.abc import Callable
'''
TODO Maybe just make this reactive to whatever node coordinates are assigned? Makes it more
flexible and it only gets called once even if that's not very efficient
'''
def get_max_dimensions(dag: DiagramDag):
    nodes = dag.get_nodes()
    max_x = 0
    max_y = 0

    for node in nodes:
        if node.x > max_x:
            max_x = node.x
        if node.y > max_y:
            max_y = node.y

    return max_x + NODE_X_MAX_SIZE, max_y + NODE_Y_MAX_SIZE
            
def determine_layer_y_coordinates(layers: list[list[str]]) -> list[int]:
    y_vals = [0 for _ in layers]

    y_offset = 0

    for i, layer in enumerate(layers):
        y_vals[i] = y_offset
        y_offset += NODE_Y_MAX_SIZE + len(layer) * LINE_Y_SPACING + 2 * EDGE_Y_SPACING
 
    return y_vals

def space_between(len_layer: int, x_spacing: int, max_len_layer: int) -> list[int]:
    step = (x_spacing * max_len_layer) // (len_layer - 1)
    positions = []
    for i in range(len_layer):
        positions.append(step * i)
    return positions

def space_around(len_layer: int, x_spacing: int, max_len_layer: int) -> list[int]:
    base = max_len_layer // (len_layer + 1)
    extra = max_len_layer % (len_layer + 1)

    positions = []
    pos = base
    for i in range(len_layer):
        positions.append(pos * x_spacing)
        pos += base + (1 if extra > 0 else 0)
        extra -= 1

    return positions

def assign_node_coordinates(
        dag: DiagramDag, ordered_layers : list[list[str]],
        y_vals: list[int], x_spacing, 
        spacing_method: Callable[[int, int, int], list[int]],
    ):
    adj = dag.get_adjacency_list()
    max_layer_width = max_len_of_arrays(ordered_layers)

    # Loop through each layer and assign coordinates according to layer with spaced x values across layer
    for i, layer in enumerate(ordered_layers):
        if len(layer) > 1:
            positions = spacing_method(len(layer), x_spacing, max_layer_width)
            for j, node_id in enumerate(layer):
                node = dag.get_node_by_id(node_id)
                node.set_coordinates(positions[j], y_vals[i])
        elif i > 0:
            # Only one node and it has children so align with a child
            node = dag.get_node_by_id(layer[0])

            # Get an arbitrary child
            children = adj[node.get_id()]
            avg_x = sum([dag.get_node_by_id(id).x for id in children])//len(children)

            node.set_coordinates(avg_x, y_vals[i])
        else:
            # Only one node and in the first layer so centre
            node = dag.get_node_by_id(layer[0])
            node.set_coordinates((x_spacing * max_layer_width) // 2, y_vals[i])

def generate_gutters(
        dag: DiagramDag, 
        layers : list[list[str]], 
        layer_y_coordinates : list[int], 
        max_x : int
    ) -> list[Gutter]:
    
    gutters: list[Gutter] = []
    for i, layer in enumerate(layers[:-1]):        
        gutter_y = layer_y_coordinates[i] + NODE_Y_MAX_SIZE
        gutter_width = layer_y_coordinates[i + 1] - gutter_y

        gutter = Gutter(gutter_y, gutter_width, max_x, dag, layers[i], layers[i + 1])

        edges = get_edges_to_layer(dag, layer)
        for edge in edges:
            gutter.add_path(edge[0], edge[1])

        gutters.append(gutter)
    return gutters

def render_dag(dag: DiagramDag, ordered_layers : list[list[str]], x_spacing : int):
    layer_y_coordinates = determine_layer_y_coordinates(ordered_layers)

    max_layer_width = max_len_of_arrays(ordered_layers)
    assign_node_coordinates(dag, ordered_layers, layer_y_coordinates, x_spacing, space_around)

    # Determine grid size and spacing then initialise a grid to it
    max_x, max_y = get_max_dimensions(dag)
    grid = Grid(max_x, max_y, default_charset)

    for node in dag.get_nodes():
        grid.set_node(node)

    gutters = generate_gutters(dag, ordered_layers, layer_y_coordinates, max_x)
    for gutter in gutters:
        for path in gutter.paths:
            grid.set_block(0, gutter.y, gutter.render_path(path))
    for gutter in gutters:
        gutter.print_gutter()
        print()

    grid.print_with_axis(5)