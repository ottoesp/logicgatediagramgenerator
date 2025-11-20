from enum import Enum

class NodeTypes(Enum):
    AND = 1
    OR = 2
    NOT = 3
    DUMMY = 4
    VARIABLE = 5