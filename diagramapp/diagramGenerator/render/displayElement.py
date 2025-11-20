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
    gateType = NodeType.NONE
    def __init__(self, node: DiagramNode):
        self.dataNode = node
        super().__init__(node.x, node.y)
    
    def get_gate_type(self):
        return self.gateType
    
    def render(self, charset=default_charset):
        super().render(charset)
        if self.gateType is None:
            raise Exception("Gate not of specified type")
        return charset[self.gateType]

class DummyGate(DisplayGate):
    gateType = NodeType.DUMMY
    def __init__(self, node):
        super().__init__(node)

class AndGate(DisplayGate):
    gateType = NodeType.AND
    def __init__(self, node):
        super().__init__(node)

class OrGate(DisplayGate):
    gateType = NodeType.OR
    def __init__(self, node):
        super().__init__(node)

class NotGate(DisplayGate):
    gateType = NodeType.NOT
    def __init__(self, node):
        super().__init__(node)