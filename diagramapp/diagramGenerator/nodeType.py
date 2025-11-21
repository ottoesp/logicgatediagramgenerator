from enum import Enum

class NodeType(Enum):
    AND = 1
    OR = 2
    NOT = 3
    DUMMY = 4
    VARIABLE = 5
    NONE = 6
    ROOT = 7

NUMBER_OF_INPUTS = {
    NodeType.AND : 2,
    NodeType.OR : 2,
    NodeType.NOT : 1,
    NodeType.DUMMY : 1,
}