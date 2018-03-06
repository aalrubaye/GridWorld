import math

import Cell

___author = "Abdul Rubaye"


# Returns a cell's color of a (S,a) based to the gained reward
def poly_color(val):
    if val <= 0:
        return "gray72"
    if -1 < val <= 25:
        return "blanched almond"
    if 25 < val <=50:
        return "bisque"
    if 50 < val <=75:
        return "navajo white"
    else:
        return "sandy brown"


# Returns cells color based on the total gain reward
def ql_color(q_vals):
    sum = 0
    for i in range(4):
        sum += q_vals[i]

    if sum <= 30:
        return "#fff8eb"
    if 30 < sum <= 60:
        return "#fff1de"
    if 60 < sum <=90:
        return "#ffe6c7"
    if 90 < sum <=120:
        return "#ffe6c7"
    if 120 <sum<=150:
        return "#ffd19a"
    if 150<sum<=180:
        return "#ffc887"
    if 180<sum<=210:
        return "#ffbe72"
    if 210<sum<=240:
        return "#ffb660"
    if 240<sum<=270:
        return "#ffae52"
    else:
        return "#ffa53d"


# Returns the q values of a cell
def q_values(cell_q_values):
    q_vals = []
    for i in range (4):
        q_vals.append(round(cell_q_values[i],1))
    return q_vals


# Find the states on the path for QL Algorithm
def next_state_on_path(state, index):
    (x, y) = state
    switcher = {
        0: (x-1, y),
        1: (x+1, y),
        2: (x, y+1),
        3: (x, y-1)
    }
    return switcher.get(index, (x, y))


# Returns a cell color based on the value from the map matrix
def cell_color(value):
    switcher = {
        0: Cell.Color.CLEAR,
        1: Cell.Color.OBSTACLE,
        2: Cell.Color.START,
        3: Cell.Color.GOAL
    }
    return switcher.get(value, Cell.Color.CLEAR)


# Finds the direct neighbors of a cell
def direct_neighbors(node):
    (grid_x, grid_y) = (Cell.World.X, Cell.World.Y)
    (x,y) = node
    top = (x-1, y) if (x-1) > -1 else None
    bottom = (x+1, y) if (x+1) < grid_x else None
    left = (x, y-1) if (y-1) > -1 else None
    right = (x, y+1) if (y+1) < grid_y else None

    return [top,bottom,left,right]


# Calculates the distance between two nodes
def linear_distance(node1, node2):
    if node1 == node2:
        return 0
    (x1,y1) = node1
    (x2,y2) = node2

    dx = abs(x1-x2)
    dy = abs(y1-y2)

    neighbor_cells = True if (dx == 1) or (dy == 1) else False

    if ((y1 == y2) or (x1 == x2)) and neighbor_cells:
        return 1
    else:
        return 2


# Calculates h(n) based on the Euclidean formula
def heuristic(current, goal):
    (x1, y1) = current
    (x2, y2) = goal

    return math.sqrt(math.pow(abs(x2-x1), 2) + math.pow(abs(y2-y1), 2))
