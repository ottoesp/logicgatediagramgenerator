from copy import deepcopy
from dag import DiagramDag, DiagramNode
from functools import reduce
from .grid import Grid
from .charsets import default_charset, debug_charset
from nodeType import NodeType
from .path import Gutter
from .rendervars import *


def determine_dimensions(layers, x_spacing):
    max_x = (max([layer[-1][1] for layer in layers]) + 1) * x_spacing

    y_vals = [0 for _ in layers]

    y_offset = 0

    for i, layer in enumerate(layers):
        y_vals[i] = y_offset
        y_offset += NODE_SPACING + len(layer) * LINE_SPACING + 2 * EDGE_SPACING
    max_y = y_offset
 
    return max_x, max_y, y_vals

def assign_node_coordinates(dag: DiagramDag, layers, y_vals, x_spacing):
    for i, layer in enumerate(layers):
        for node_id, x in layer:
            node = dag.get_node_by_id(node_id)
            if node is None:
                raise ValueError()
            node.set_coordinates(x * x_spacing, y_vals[i])

def generate_gutters(
        dag: DiagramDag, 
        layers : list[list[str]], 
        layer_y_coordinates : list[int], 
        max_x : int
    ) -> list[Gutter]:
    
    gutters: list[Gutter] = []
    for i, layer in enumerate(layers[:-1]):        
        gutter_y = layer_y_coordinates[i] + NODE_SPACING
        gutter_width = layer_y_coordinates[i + 1] - gutter_y

        gutter = Gutter(gutter_y, gutter_width, max_x, dag, layers[i], layers[i + 1])

        gutters.append(gutter)
    return gutters

def render_dag(dag: DiagramDag, ordered_layers : list[list[tuple[str, int]]], x_spacing : int):
    # Determine grid size and spacing then initialise a grid to it
    max_x, max_y, layer_y_coordinates = determine_dimensions(ordered_layers, x_spacing)
    grid = Grid(max_x, max_y, debug_charset)

    assign_node_coordinates(dag, ordered_layers, layer_y_coordinates, x_spacing)
    
    # Don't need specific x information anymore
    layers = [[node for node, x in ordered_layer] for ordered_layer in ordered_layers]

    for node in dag.get_nodes():
        grid.set_node(node)

    # grid.print_with_axis(5)

    gutters = generate_gutters(dag, layers, layer_y_coordinates, max_x)
    gutters[0].enumerate_configurations()