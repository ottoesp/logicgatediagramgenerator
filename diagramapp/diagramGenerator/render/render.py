from copy import deepcopy
from dag import DiagramDag, DiagramNode
from functools import reduce
from .grid import Grid
from .charsets import default_charset, debug_charset
from .displayElement import DisplayGate, AndGate, DummyGate, DisplayElement, NotGate, OrGate, Path
from nodeType import NodeType

"""
Currently has issues with lanes being assigned right to left, would like this the other way around
since variables can go to > 2 and only have downstream paths
"""

NODE_SPACING = 3
LINE_SPACING = 1
EDGE_SPACING = 2

def determine_dimensions(layers, x_spacing):
    max_x = (max([layer[-1][1] for layer in layers]) + 2) * x_spacing

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

def initialise_display_elements(dag: DiagramDag):
    display_nodes : list[DisplayGate] = []
    data_nodes : set[DiagramNode] = dag.get_nodes()
    
    for node in data_nodes:
        if node.nodeType == NodeType.AND:
            display_nodes.append(AndGate(node))
        elif node.nodeType == NodeType.OR:
            display_nodes.append(OrGate(node))

def render_dag(dag: DiagramDag, layers, x_spacing):
    max_x, max_y, y_vals = determine_dimensions(layers, x_spacing)

    grid = Grid(max_x, max_y, debug_charset)
    assign_node_coordinates(dag, layers, y_vals, x_spacing)

    print(grid)