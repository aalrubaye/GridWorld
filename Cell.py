from enum import Enum


class Type(Enum):
    CLEAR = 0
    OBSTACLE = 1
    START = 2
    GOAL = 3
    VISITED = 4


class Color(Enum):
    CLEAR = "floral white"
    OBSTACLE = "black"
    START = "cyan2"
    GOAL = "orange"
    VISITED = "khaki1"

class World(Enum):
    CELL_WIDTH = 80
    X=10
    Y=10

