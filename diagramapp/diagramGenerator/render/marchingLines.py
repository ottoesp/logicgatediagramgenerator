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
    ERROR = 18
    
"""
Marching Lines Lookup table for all the different configurations of paths surrounding a cell
Follows order of cardinal directions and the current cell CNESW (certainly never eat soggy weetbix).
Since we want a different character depending on whether a neighbour is the same or different path. 
We denote the cells as 
    'M' : me  (same path)
    'Y' : you (different path)
    '0' : empty cell
The centre cell is marked 'Y' if another path already occupies it. Otherwise it is marked 0.
"""
ml_lookup : dict[str, LineCase] = {
    "0MMMM" : LineCase.HORZ_VERT,
    "00MMM" : LineCase.HORZ_DOWN,
    "0MM0M" : LineCase.HORZ_UP,
    "0MMM0" : LineCase.VERT_RIGHT,
    "0M0MM" : LineCase.VERT_LEFT,
    "0MM00" : LineCase.UP_RIGHT,
    "0M0M0" : LineCase.VERT,
    "YMMYY" : LineCase.UP_RIGHT_CROSSED,
    "YMYMY" : LineCase.VERT_CROSSED,
    "0M00M" : LineCase.UP_LEFT,
    "00M0M" : LineCase.UP_RIGHT,
    "YMYYM" : LineCase.UP_LEFT_CROSSED,
    "YYMYM" : LineCase.DOWN_RIGHT_CROSSED,
    "00M0M" : LineCase.HORZ,
    "000MM" : LineCase.DOWN_LEFT,
    "00MM0" : LineCase.DOWN_RIGHT,
    "YYMYM" : LineCase.HORZ_CROSSED,
    "YYYMM" : LineCase.DOWN_LEFT_CROSSED
}