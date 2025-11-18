from enum import Enum

class LineCases(Enum):
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
    DOWN_LEFT = 17
    DOWN_LEFT_CROSSED = 18
    
ml_lookup = {
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
    "MMMM0" : LineCases.HORZ_VERT,
    "0MMM0" : LineCases.HORZ_DOWN,
    "MM0M0" : LineCases.HORZ_UP,
    "MMM00" : LineCases.VERT_RIGHT,
    "M0MM0" : LineCases.VERT_LEFT,
    "MM000" : LineCases.UP_RIGHT,
    "M0M00" : LineCases.VERT,
    "MMYYY" : LineCases.UP_RIGHT_CROSSED,
    "MYMYY" : LineCases.VERT_CROSSED,
    "M00M0" : LineCases.UP_LEFT,
    "0M0M0" : LineCases.UP_RIGHT,
    "MYYMY" : LineCases.UP_LEFT_CROSSED,
    "YMYMY" : LineCases.DOWN_RIGHT_CROSSED,
    "0M0M0" : LineCases.HORZ,
    "00MM0" : LineCases.DOWN_LEFT,
    "YMYMY" : LineCases.HORZ_CROSSED,
    "YYMMY" : LineCases.DOWN_LEFT_CROSSED
}