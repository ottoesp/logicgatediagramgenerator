from ..dag import DiagramDag, DiagramNode
from .grid import Grid
from .charsets import default_charset, debug_charset
from ..nodeType import NodeType, VERTICAL_SIZE
from .path import Gutter
from .rendervars import *
from ..utils import get_edges_to_layer, max_len_of_arrays

def get_max_dimensions(dag: DiagramDag):
    nodes = dag.get_nodes()

    # Initialise max nodes as an arbitrary node
    max_x_node: DiagramNode = list(nodes)[0]
    max_y_node: DiagramNode = max_x_node

    for node in nodes:
        if node.x > max_x_node.x:
            max_x_node = node
        if node.y > max_y_node.y:
            max_y_node = node

    return max_x_node.x + NODE_X_MAX_SIZE, max_y_node.y + NODE_Y_MAX_SIZE

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

def render_dag(dag: DiagramDag, ordered_layers : list[list[str]], layer_y_coordinates: list[int]):

    # Determine grid size and spacing then initialise a grid to it
    max_x, max_y = get_max_dimensions(dag)
    grid = Grid(max_x, max_y, default_charset)

    for node in dag.get_nodes():
        grid.set_node(node)

    gutters = generate_gutters(dag, ordered_layers, layer_y_coordinates, max_x)
    for gutter in gutters:
        for path in gutter.paths:
            grid.set_block(0, gutter.y, gutter.render_path(path))

    return str(grid)