from enum import Enum

class LineCase(Enum):
    HORZ_VERT = 1
    HORZ_DOWN = 2
    HORZ_UP = 3
    VERT_RIGHT = 4
    VERT_LEFT = 5
    UP_RIGHT = 6
    VERT = 7
    UP_RIGHT_CROSSED = 8
    VERT_CROSSED = 9
    UP_LEFT = 10
    DOWN_RIGHT = 11
    UP_LEFT_CROSSED = 12
    DOWN_RIGHT_CROSSED = 13
    HORZ = 14
    DOWN_LEFT = 15
    HORZ_CROSSED = 16
    DOWN_LEFT_CROSSED = 17
    
ml_lookup : dict[str, LineCase] = {
"""
Marching Lines Lookup table for all the different configurations of paths surrounding a cell
Follows order of cardinal directions and the current cell NESWC (never eat soggy weetbix cold).
Since we want a different character depending on whether a neighbour is the same or different path. 
We denote the cells as 
    'M' : me  (same path)
    'Y' : you (different path)
    '0' : empty cell
The centre cell is marked 'Y' if another path already occupies it. Otherwise it is marked 0.
"""
    "MMMM0" : LineCase.HORZ_VERT,
    "0MMM0" : LineCase.HORZ_DOWN,
    "MM0M0" : LineCase.HORZ_UP,
    "MMM00" : LineCase.VERT_RIGHT,
    "M0MM0" : LineCase.VERT_LEFT,
    "MM000" : LineCase.UP_RIGHT,
    "M0M00" : LineCase.VERT,
    "MMYYY" : LineCase.UP_RIGHT_CROSSED,
    "MYMYY" : LineCase.VERT_CROSSED,
    "M00M0" : LineCase.UP_LEFT,
    "0M0M0" : LineCase.UP_RIGHT,
    "MYYMY" : LineCase.UP_LEFT_CROSSED,
    "YMYMY" : LineCase.DOWN_RIGHT_CROSSED,
    "0M0M0" : LineCase.HORZ,
    "00MM0" : LineCase.DOWN_LEFT,
    "YMYMY" : LineCase.HORZ_CROSSED,
    "YYMMY" : LineCase.DOWN_LEFT_CROSSED
}