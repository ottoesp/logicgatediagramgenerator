from .marchingLines import LineCase
from enum import Enum

class Gate(Enum):
    AND = 1
    OR = 2
    NOT = 3

default_charset: dict[LineCase | Gate  : str] = {
    Gate.AND : "and\nand",
    Gate.OR : "or \n\or ",
    Gate.NOT : "not",

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
    LineCase.DOWN_LEFT_CROSSED : "┐"
}