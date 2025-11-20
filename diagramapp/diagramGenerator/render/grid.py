from .charsets import MiscVisual

class Grid:
    def __init__(self, max_x, max_y, charset):
        self.lines = []
        for i in range(max_x):
            self.lines.append([charset[MiscVisual.EMPTY] for _ in range(max_y)])

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
                if char != self.charset[MiscVisual.EMPTY]:
                    self.set_cell(x + i, y + j, char, False)