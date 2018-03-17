from enum import Enum

___author = "Abdul Rubaye"


# The enum for Cell Type
class Type(Enum):
    CLEAR = 0
    OBSTACLE = 1
    START = 2
    GOAL = 3
    VISITED = 4


# The enum for Cell color
class Color(Enum):
    CLEAR = "floral white"
    OBSTACLE = "black"
    START = "cyan2"
    GOAL = "orange"
    VISITED = "khaki1"


# The grid world properties
class World(Enum):
    CELL_WIDTH = 80
    X=8
    Y=8

