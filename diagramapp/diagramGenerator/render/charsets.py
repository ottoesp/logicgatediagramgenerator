from .marchingLines import LineCase
from enum import Enum
from nodeType import NodeType
import copy

class MiscVisual(Enum):
    EMPTY = 1

default_charset: dict[LineCase | NodeType | MiscVisual, str] = {
    NodeType.AND : "and\nand",
    NodeType.OR : "or \nor ",
    NodeType.NOT : "not",

    LineCase.HORZ_VERT : "┼",
    LineCase.HORZ_DOWN : "┬",
    LineCase.HORZ_UP : "┴",
    LineCase.VERT_RIGHT : "├",
    LineCase.VERT_LEFT : "┤",
    LineCase.UP_RIGHT : "└",
    LineCase.VERT : "│",
    LineCase.UP_RIGHT_CROSSED : "└",
    LineCase.VERT_CROSSED : "╫",
    LineCase.UP_LEFT : "┘",
    LineCase.DOWN_RIGHT : "┌",
    LineCase.UP_LEFT_CROSSED : "┘",
    LineCase.DOWN_RIGHT_CROSSED : "┌",
    LineCase.HORZ : "─",
    LineCase.DOWN_LEFT : "┐",
    LineCase.HORZ_CROSSED : "╪",
    LineCase.DOWN_LEFT_CROSSED : "┐",

    MiscVisual.EMPTY : " ",
    NodeType.DUMMY : '───',
    NodeType.ROOT : "$"
}

debug_charset = copy.deepcopy(default_charset)
debug_charset[MiscVisual.EMPTY] = "🞘"
