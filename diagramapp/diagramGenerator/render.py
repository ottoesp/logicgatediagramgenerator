from copy import deepcopy
from functools import reduce

default_charset = {
    'empty' : ' ',
    'not' : 'not\nnot',
    'or' : 'or \nor ',
    'and' : 'and\nand',
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
        block_lines = (self.charset[block] if use_charset else block).split('\n')
        for i, b_line in enumerate(block_lines):
            for j, char in enumerate(b_line):
                if char != self.charset['empty']:
                    self.set_cell(x + i, y + j, char, False)

def determine_dimensions(layers, x_spacing):
    max_x = (max([layer[-1][1] for layer in layers]) + 2) * x_spacing

    y_vals = [0 for _ in layers]

    for i, layer in enumerate(layers):
        y_vals[i] += NODE_SPACING + len(layer) * LINE_SPACING + 2 * EDGE_SPACING

    max_y = sum(y_vals)

    return max_x, max_y, y_vals

def place_nodes(grid, layers, y_vals, x_spacing):
    for layer in layers:
        pass

def render_dag(edges, layers, x_spacing):
    max_x, max_y, y_vals = determine_dimensions(layers, x_spacing)

    grid = Grid(max_x, max_y, debug_charset)

    print(grid)