import time

___author = "Abdul Rubaye"

from Tkinter import *
from tkFileDialog import askopenfilename
import tkMessageBox
import Cell
import Astar
import Qlearning
import threading

ql_button = None

root = Tk()
root.title("GridWorld HomeWork")
root.resizable(width=FALSE, height=FALSE)

cellWidth = Cell.Size.Width

rightFrame = Frame(root)
rightFrame.pack(side=RIGHT, fill=Y)

leftFrame = Frame(root)
leftFrame.pack(side=LEFT, fill=Y)

radio_button_value = IntVar()
radio_button_value.set(1)

is_start_created = False
is_goal_created = False

start = ()
goal = ()


Label(rightFrame, text="    ", fg='white').grid(row=0, column=2, sticky=W)
Label(rightFrame, text="    ", fg='white').grid(row=0, column=0, sticky=E)

grid = Canvas(leftFrame, width=800, heigh=800)

# grid size
(grid_x, grid_y) = (10, 10)

gridMatrix = [[0 for row in range(grid_y)] for col in range(grid_x)]
qMatrix = [[0 for row in range(grid_y)] for col in range(grid_x)]

qlearner = Qlearning.Algorithm(gridMatrix)
qMatrix_calculated = False
# The world grid matrix initializer
def initialize_grid_matrix():
    global  gridMatrix
    for i in range(grid_x):
        for j in range(grid_y):
            gridMatrix[i][j] = 0


def set_new_grid():
    global is_start_created, is_goal_created, goal, start
    initialize_grid_matrix()
    create_grid()
    goal = ()
    start = ()
    is_start_created = False
    is_goal_created = False


# Returns a cell color based on the value from the map matrix
def cell_color(value):
    switcher = {
        0: Cell.Color.CLEAR,
        1: Cell.Color.OBSTACLE,
        2: Cell.Color.START,
        3: Cell.Color.GOAL
    }
    return switcher.get(value, Cell.Color.CLEAR)

def ql_color(top,bottom,right,left):
    sum = top+bottom+right+left
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

# Adds the text for QL path planning
def insert_text_ql(x, y, q_matrix):

    top = round(q_matrix[0],1)
    bottom = round(q_matrix[1],1)
    right = round(q_matrix[2],1)
    left = round(q_matrix[3],1)

    qlc = ql_color(top,bottom,right,left)
    grid.create_rectangle(x*cellWidth, y*cellWidth, (x+1)*cellWidth, (y+1)*cellWidth, fill=qlc, width=1)

    grid.create_text(((x+0.5)*cellWidth, (y+0.25)*cellWidth), text=top, fill='black')
    grid.create_text(((x+0.5)*cellWidth, (y+0.75)*cellWidth), text=bottom, fill='black')
    grid.create_text(((x+0.75)*cellWidth, (y+0.5)*cellWidth), text=right, fill='black')
    grid.create_text(((x+0.25)*cellWidth, (y+0.5)*cellWidth), text=left, fill='black')


# Adds the text for A_star path planning
def insert_text_a_star(x, y, routeNode):
    cost = "d="+ str(routeNode.distance)
    fscore = "f="+str(round(routeNode.f_score,1))
    heuristic = "h="+str(round(routeNode.heuristic,1))
    grid.create_text(((x+0.5)*cellWidth, (y+0.25)*cellWidth), text=fscore, fill='black')
    grid.create_text(((x+0.5)*cellWidth, (y+0.5)*cellWidth), text=cost, fill='black')
    grid.create_text(((x+0.5)*cellWidth, (y+0.75)*cellWidth), text=heuristic, fill='black')


# Creates and renders the world grid
def create_grid():
    for i in range(grid_x):
        for j in range(grid_y):
            color = cell_color(gridMatrix[j][i])
            grid.create_rectangle(i*cellWidth, j*cellWidth, (i+1)*cellWidth, (j+1)*cellWidth, fill=color, width=1)
    grid.pack(side=LEFT)


# opens a map matrix from a file and renders it to the grid
def open_file():
    global is_start_created, is_goal_created
    map_file = askopenfilename(title="Select map file")
    if len(map_file) == 0:
        tkMessageBox.showwarning('No Selection', 'No map file was selected!')
    convert_file_to_matrix(map_file)
    create_grid()
    is_start_created = False
    is_goal_created = False


# converts a map file content to a grid matrix
def convert_file_to_matrix(map_file):
    content = open(map_file, "r")
    index_i = 0
    for line in content:
        index_j = 0
        number_strings = line.split()
        for val in number_strings:
            gridMatrix[index_i][index_j] = int(val)
            index_j += 1
        index_i += 1

# Adds the start cell or goal cell via click event
def add_start_goal_cell(coordination):
    global is_start_created, is_goal_created, start, goal
    (i, j) = (coordination.x/cellWidth, coordination.y/cellWidth)
    if (i < grid_x) & (j < grid_y):
        if gridMatrix[j][i] == Cell.Type.CLEAR:
            if (radio_button_value.get() == 2) & (is_start_created is False):
                grid.create_rectangle(i*cellWidth, j*cellWidth, (i+1)*cellWidth, (j+1)*cellWidth,
                                      fill=Cell.Color.START, width=1)
                grid.create_text(((i+0.5)*cellWidth, (j+0.5)*cellWidth), text="Start", fill='black')
                gridMatrix[j][i] = Cell.Type.START
                start = (j,i)
                is_start_created = True
            elif (radio_button_value.get() == 3) & (is_goal_created is False):
                grid.create_rectangle(i*cellWidth, j*cellWidth, (i+1)*cellWidth, (j+1)*cellWidth,
                                      fill=Cell.Color.GOAL, width=1)
                grid.create_text(((i+0.5)*cellWidth, (j+0.5)*cellWidth), text="Goal", fill='black')
                gridMatrix[j][i] = Cell.Type.GOAL
                goal = (j,i)
                is_goal_created = True


# Resets the start cell or goal cell via click event
def reset_start_goal_cell(coordination):
    global is_start_created, is_goal_created, start, goal
    (i, j) = (coordination.x/cellWidth, coordination.y/cellWidth)
    if (i < grid_x) & (j < grid_y):
        if gridMatrix[j][i] == Cell.Type.START:
            if radio_button_value.get() == 2:
                grid.create_rectangle(i*cellWidth, j*cellWidth, (i+1)*cellWidth, (j+1)*cellWidth,
                                      fill=Cell.Color.CLEAR, width=1)
                gridMatrix[j][i] = Cell.Type.CLEAR
                start = ()
                is_start_created = False
        elif gridMatrix[j][i] == Cell.Type.GOAL:
            if radio_button_value.get() == 3:
                grid.create_rectangle(i*cellWidth, j*cellWidth, (i+1)*cellWidth, (j+1)*cellWidth,
                                      fill=Cell.Color.CLEAR, width=1)
                gridMatrix[j][i] = Cell.Type.CLEAR
                goal = ()
                is_goal_created = False


def a_star():
    if (start != ()) and (goal != ()):
        astar = Astar.Algorithm(gridMatrix, start, goal)
        (x,y) = goal
        (x_start, y_start) = start
        (evaluated_nodes, path) = astar.search()

        if evaluated_nodes:
            for i in range (grid_x):
                for j in range (grid_y):
                    if evaluated_nodes[i][j] != 0:
                        if (i,j) == (x,y):
                            grid.create_rectangle(j*cellWidth, i*cellWidth, (j+1)*cellWidth, (i+1)*cellWidth,fill=Cell.Color.GOAL, width=1)
                        elif (i,j) in path:
                            grid.create_rectangle(j*cellWidth, i*cellWidth, (j+1)*cellWidth, (i+1)*cellWidth,fill='green', width=1)
                        else:
                            grid.create_rectangle(j*cellWidth, i*cellWidth, (j+1)*cellWidth, (i+1)*cellWidth,fill=Cell.Color.VISITED, width=1)
                        insert_text_a_star(j,i,evaluated_nodes[i][j])
            grid.create_text(((y_start+0.5)*cellWidth, (x_start+0.5)*cellWidth), text='Start', fill='black')
        else:
            tkMessageBox.showwarning('No Route Found', 'There is no possible route to the goal! You still can re select either one of the start or goal cell.')
    else:
        tkMessageBox.showwarning('Required Values', 'Make sure you select the start and goal cells!')


# def q_learning():
#     global qlearner
#     qlearner = Qlearning.Algorithm(gridMatrix, goal)
#     rep_learning()

def rep_learning():
    global qlearner, qMatrix, qMatrix_calculated

    create_grid()
    qMatrix = qlearner.learn(goal)
    qMatrix_calculated = True
    for i in range (grid_x):
        for j in range (grid_y):
            if gridMatrix[i][j] == Cell.Type.CLEAR:
                insert_text_ql(j,i,qMatrix[i][j])
            if gridMatrix[i][j] == Cell.Type.GOAL:
                grid.create_text(((j+0.5)*cellWidth, (i+0.5)*cellWidth), text="Goal", fill='black')


def find_path_ql():
    global qMatrix
    if start == ():
        tkMessageBox.showwarning('No Start', 'Please select the start state!')
        return
    if qMatrix_calculated is False:
        tkMessageBox.showwarning('QLearning Error', 'Please run the Q Learning Algorithm')
        return


    current = start
    (x,y) = current

    goal_found = False

    while goal_found is False:
        max = qlearner.max_q(qMatrix[x][y])




def separator(row_val):
    Label(rightFrame, text=" "*33).grid(row=row_val, column=1)


def horizontal_line(row_val):
    Label(rightFrame, text="_"*33, fg='gray').grid(row=row_val, column=1)


# Creates the buttons
def create_button(text, row_val, command):
    return Button(rightFrame, text=text, width=20, command=command).grid(row=row_val, column=1, sticky=W)

# Creates and Displays the buttons on the right side of the screen
def create_left_side_elements():
    global ql_button
    row_val = 4
    create_button("Upload Map", row_val, open_file)
    separator(row_val+1)
    create_button("A* Path finder", row_val+2, a_star)
    ql_button = create_button("Q Learning", row_val+3, rep_learning)
    separator(row_val+4)
    create_button("Reset", row_val+5, set_new_grid)
    create_radio_buttons(row_val+6)
    create_button("Find Path", row_val+7, find_path_ql)


# Creates the radio button for start/goal
def create_radio_buttons(row_val):
    separator(row_val)
    horizontal_line(row_val+1)
    Label(rightFrame, text="Cell to add/remove?").grid(row=row_val+2, column=1, sticky=W)
    Radiobutton(rightFrame, text="Start", variable=radio_button_value, value=2).grid(row=row_val+3, column=1, sticky=W)
    Radiobutton(rightFrame, text="Goal", variable=radio_button_value, value=3).grid(row=row_val+4, column=1, sticky=W)
    horizontal_line(row_val+5)


set_new_grid()
create_left_side_elements()

grid.bind('<Button-2>', reset_start_goal_cell)
grid.bind('<Button-1>', add_start_goal_cell)


root.mainloop()






