from enum import Enum

class NodeType(Enum):
    AND = 1
    OR = 2
    NOT = 3
    DUMMY = 4
    VARIABLE = 5
    NONE = 6
    ROOT = 7

STRING_REPRESENTATION = {
    NodeType.AND : 'and',
    NodeType.OR : 'or',
    NodeType.NOT : 'not',
}

TYPE_FROM_STRING_REPRESENTATION = {v: k for k, v in STRING_REPRESENTATION.items()}

NUMBER_OF_INPUTS = {
    NodeType.AND : 2,
    NodeType.OR : 2,
    NodeType.NOT : 1,
    NodeType.DUMMY : 1,
    NodeType.ROOT : 1
}

BINDING_STRENGTH = {
    NodeType.AND : 1,
    NodeType.OR : 1,
    NodeType.NOT : 2,
    NodeType.VARIABLE : 3
}

VERTICAL_SIZE = {
    NodeType.AND : 2,
    NodeType.OR : 2,
    NodeType.NOT : 1,
    NodeType.DUMMY : 1,
    NodeType.ROOT : 1,
    NodeType.VARIABLE : 1
}

PREFERS_OFFSET = {
    NodeType.AND : True,
    NodeType.OR : True,
    NodeType.NOT : False,
    NodeType.DUMMY : False,
    NodeType.ROOT : False,
    NodeType.VARIABLE : False
}

DOUBLE_INPUT_GATES = {NodeType.AND, NodeType.OR}
SINGLE_INPUT_GATES = {NodeType.NOT}