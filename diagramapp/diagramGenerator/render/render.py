from copy import deepcopy
from dag import DiagramDag, DiagramNode
from functools import reduce
from .grid import Grid


"""
Currently has issues with lanes being assigned right to left, would like this the other way around
since variables can go to > 2 and only have downstream paths
"""

default_charset = {
    'empty' : ' ',
    'not' : 'not\nnot',
    'or' : 'or \nor ',
    'and' : 'and\nand',
    'dummy': '+-+',
    'VertLine': '│',
    'HorzLine': '─'
}

debug_charset = deepcopy(default_charset)
debug_charset['empty'] = '.'

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
            node.set_coordinates(x * x_spacing, y_vals[i])

def draw_edges_from_node(dag:DiagramDag, grid, edges, upstream: DiagramNode, lane_y):
    needsLane = False

    for downstream_id in edges:
        downstream = dag.get_node_by_id(downstream_id)

        x_diff = abs(downstream.x - upstream.x)
        y_diff = upstream.y - downstream.y

        # WIP: Currently a very rudimentary way of doing this, need to make actually readable
        if x_diff > 0:
            lineAB = vert_line(x_diff)
            grid.set_block(min(upstream.x, downstream.x), lane_y, lineAB)

            needsLane = True
        else:
            lineAB = horz_line(y_diff - NODE_SPACING)
            grid.set_block(downstream.x, downstream.y + NODE_SPACING, lineAB)

    return needsLane

def draw_edges(dag: DiagramDag, grid, layers):
    adj = dag.get_adjacency_list()
    for layer in reversed(layers):
        layer_y = dag.get_node_by_id(layer[0][0]).y

        lane = 0

        for upstream_id, _ in layer:
            lane_y = layer_y - (EDGE_SPACING + lane)
            usedLane = draw_edges_from_node(dag, grid, adj[upstream_id], dag.get_node_by_id(upstream_id), lane_y)
            if usedLane: # This was sort of an attempt to make it smaller but we'd need to determine this earlier
                lane += 1

def vert_line(height, charset=default_charset):
    return (charset['VertLine'] + '\n') * height

def horz_line(width, charset=default_charset):
    return charset['HorzLine'] * width + '\n'

def place_nodes(nodes: list[DiagramNode], grid):
    for node in nodes:
        grid.set_block(node.x, node.y, node.name)

def render_dag(dag: DiagramDag, layers, x_spacing):
    max_x, max_y, y_vals = determine_dimensions(layers, x_spacing)

    grid = Grid(max_x, max_y, default_charset)
    assign_node_coordinates(dag, layers, y_vals, x_spacing)
    place_nodes(dag.get_nodes(), grid)

    draw_edges(dag, grid, layers)

    print(grid)