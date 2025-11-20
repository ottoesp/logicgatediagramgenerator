from .charsets import MiscVisual
from diagramNode import DiagramNode

class Grid:
    def __init__(self, max_x, max_y, charset):
        self.lines = []
        for i in range(max_x):
            self.lines.append([charset[MiscVisual.EMPTY] for _ in range(max_y)])

        self.charset = charset

    def __str__(self):
        return '\n'.join([''.join(line) for line in self.lines])
        
    def print_with_axis(self, tick_spacing: int) -> None:
        output : str = " " * 4
        for i in range(len(self.lines[0])):
            if (i % tick_spacing == 0):
                output += "{tick}".format(tick=i).ljust(tick_spacing)
        output += ("\n")

        for i, line in enumerate(self.lines):
            if (i % tick_spacing == 0):
                output += "{tick:3d}".format(tick=i) + " "
            else:
                output += " " * 4
            output += "".join(line) + "\n"
        print(output)

    def set_cell(self, x, y, character, use_charset=True):
        self.lines[x][y] = self.charset[character] if use_charset else character

    def set_block(self, x, y, block: str):
        block_lines = block.split('\n')

        for i, b_line in enumerate(block_lines):
            for j, char in enumerate(b_line):
                if char != self.charset[MiscVisual.EMPTY]:
                    self.set_cell(x + i, y + j, char, False)

    def set_node(self, node : DiagramNode):
        self.set_block(node.x, node.y, node.render())