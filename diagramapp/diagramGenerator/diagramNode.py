from nodeType import NodeType
from render.charsets import default_charset

def reset_id_counter():
    DiagramNode.nextId = 0

class DiagramNode:
    nextId = 0
    def __init__(self, nodeType : NodeType):
        self.nodeType : NodeType = nodeType
        self.id = str(DiagramNode.nextId)
        DiagramNode.nextId += 1
        self.x: int = -1
        self.y: int = -1

    def get_id(self):
        return self.id

    def set_coordinates(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return f'[{self.nodeType.name}, {self.id}]'
    
    def __repr__(self):
        return f'{self.nodeType.name}.{self.id}'
    
    def render(self, charset=default_charset):
        return charset[self.nodeType]

class RootNode(DiagramNode):
    def __init__(self):
        super().__init__(NodeType.ROOT)

class VariableNode(DiagramNode):
    def __init__(self, name):
        super().__init__(NodeType.VARIABLE)
        self.name = name
        self.id = name
    
    def render(self, charset=default_charset):
        return self.id
    
    def __repr__(self):
        return self.id

class DummyNode(DiagramNode):
    def __init__(self):
        super().__init__(NodeType.DUMMY)
