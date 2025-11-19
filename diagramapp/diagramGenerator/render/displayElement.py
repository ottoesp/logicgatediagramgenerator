class DisplayElement:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def render(self):
        pass

class Path(DisplayElement):
    pass

class Node(DisplayElement):
    def __init__(self, x, y):
        super().__init__(x, y)

class AndGate(Node):
    def __init__(self, x, y):
        super().__init__(x, y)