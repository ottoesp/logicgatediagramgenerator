from enum import Enum

class NodeType(Enum):
    AND = 1
    OR = 2
    NOT = 3
    DUMMY = 4
    VARIABLE = 5
    NONE = 6
    ROOT = 7