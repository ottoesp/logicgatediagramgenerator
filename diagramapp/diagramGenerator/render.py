from copy import deepcopy
from dag import DiagramDag, DiagramNode
from functools import reduce

default_charset = {
    'empty' : ' ',
    'not' : 'not\nnot',
    'or' : 'or \nor ',
    'and' : 'and\nand',
    'dummy': '---'
}

debug_charset = deepcopy(default_charset)
debug_charset['empty'] = '.'

NODE_SPACING = 3
LINE_SPACING = 2
EDGE_SPACING = 2

class Grid:
    def __init__(self, max_x, max_y, charset):
        self.lines = []
        for i in range(max_x):
            self.lines.append([charset['empty'] for _ in range(max_y)])

        self.charset = charset

    def __str__(self):
        return '\n'.join([''.join(line) for line in self.lines])

    def set_cell(self, x, y, character, use_charset=True):
        self.lines[x][y] = self.charset[character] if use_charset else character

    def set_block(self, x, y, block: str, use_charset=True):
        if use_charset:
            if block in self.charset:
                source = self.charset[block]
            else:
                source = block
        else:
            source = block
        block_lines = source.split('\n')

        for i, b_line in enumerate(block_lines):
            for j, char in enumerate(b_line):
                if char != self.charset['empty']:
                    self.set_cell(x + i, y + j, char, False)

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


def place_nodes(nodes: list[DiagramNode], grid):
    for node in nodes:
        grid.set_block(node.x, node.y, node.name)

def render_dag(dag: DiagramDag, layers, x_spacing):
    max_x, max_y, y_vals = determine_dimensions(layers, x_spacing)

    grid = Grid(max_x, max_y, default_charset)
    assign_node_coordinates(dag, layers, y_vals, x_spacing)
    place_nodes(dag.get_nodes(), grid)

    print(grid)