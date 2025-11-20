from .charsets import NodeType, default_charset
from dag import DiagramNode

class DisplayElement:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def render(self, charset=default_charset):
        pass

class Path(DisplayElement):
    pass

class DisplayGate(DisplayElement):
    def __init__(self, node: DiagramNode):
        super().__init__(node.x, node.y)
        self.dataNode = node
        self.gateType = node.nodeType
    
    def get_gate_type(self):
        return self.gateType
    
    def render(self, charset=default_charset):
        return charset[self.gateType]

class DisplayVariable(DisplayElement):
    def __init__(self, node: DiagramNode):
        super().__init__(node.x, node.y)
        self.dataNode = node
    
    def render(self, charset=default_charset):
        return self.dataNode.id