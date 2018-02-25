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
    GOAL = "sandy brown"
    VISITED = "antique white"


class Size(Enum):
    Width = 80
