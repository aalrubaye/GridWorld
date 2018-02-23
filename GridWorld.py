from Tkinter import *
from tkFileDialog import askopenfilename
import tkMessageBox

root = Tk()
root.title("GridWorld HomeWork")
root.resizable(width=FALSE, height=FALSE)
cellWidth = 80

rightFrame = Frame(root)
rightFrame.pack(side=RIGHT, fill=Y)

leftFrame = Frame(root)
leftFrame.pack(side=LEFT, fill=Y)

var = IntVar()
var.set(1)

Label(rightFrame, text="    ", fg='white').grid(row=0, column=2, sticky=W)
Label(rightFrame, text="    ", fg='white').grid(row=0, column=0, sticky=E)

grid = Canvas(leftFrame, width=800, heigh=800)


# grid size
(x, y) = (10, 10)

gridMatrix = [[0 for row in range(x)] for col in range(y)]

# The world grid matrix initializer
def initialize_grid_matrix():
    for i in range(x):
        for j in range(y):
            gridMatrix[i][j] = 0


# Returns a cell color based on the value from the map matrix
def cell_color(value):
    switcher = {
        0: "floral white",
        1: "black",
        2: "cyan2",
        3: "sandy brown"
    }
    return switcher.get(value, "floral white")


# Adds the text for QL path planning
def insert_text_ql(x, y):
    grid.create_text(((x+0.5)*cellWidth, (y+0.25)*cellWidth), text="2", fill='black')
    grid.create_text(((x+0.25)*cellWidth, (y+0.5)*cellWidth), text="2", fill='black')
    grid.create_text(((x+0.75)*cellWidth, (y+0.5)*cellWidth), text="2", fill='black')
    grid.create_text(((x+0.5)*cellWidth, (y+0.75)*cellWidth), text="2", fill='black')


# Adds the text for A_star path planning
def insert_text_a_star(x, y):
    grid.create_text(((x+0.5)*cellWidth, (y+0.25)*cellWidth), text="text-top", fill='black')
    grid.create_text(((x+0.5)*cellWidth, (y+0.5)*cellWidth), text="text-mid", fill='black')
    grid.create_text(((x+0.5)*cellWidth, (y+0.75)*cellWidth), text="text-below", fill='black')


# Adds the exploration notes for each cell
def add_exploration_texts():
    insert_text_a_star(2,2)
    insert_text_ql(1,1)
    grid.pack(side=LEFT)


# Creates and renders the world grid
def create_grid():
    for i in range(x):
        for j in range(y):
            color = cell_color(gridMatrix[j][i])
            grid.create_rectangle(i*cellWidth, j*cellWidth, (i+1)*cellWidth, (j+1)*cellWidth, fill=color, width=1)
    grid.pack(side=LEFT)
    # add_exploration_texts()


# opens a map matrix from a file and renders it to the grid
def open_file():
    map_file = askopenfilename(title = "Select map file")
    if len(map_file) == 0:
        tkMessageBox.showwarning('No Selection', 'No map file was selected!')
    convert_file_to_matrix(map_file)
    create_grid()


# converts a map file content to a grid matrix
def convert_file_to_matrix(file):
    content = open(file, "r")
    index_i = 0
    for line in content:
        index_j = 0
        number_strings = line.split()
        for val in number_strings:
            gridMatrix[index_i][index_j] = int(val)
            index_j += 1
        index_i += 1


def do_nothing():
    print("doNothing")


# Adds the start cell or goal cell via click event
def add_start_goal_cell(coordination):
    (i, j) = (coordination.x/80, coordination.y/80)
    if (i < 10) & (j < 10):
        if gridMatrix[j][i] == 0:
            if var.get() == 2:
                grid.create_rectangle(i*cellWidth, j*cellWidth, (i+1)*cellWidth, (j+1)*cellWidth, fill='yellow', width=1)
                gridMatrix[j][i] = 2
            elif var.get() == 3:
                grid.create_rectangle(i*cellWidth, j*cellWidth, (i+1)*cellWidth, (j+1)*cellWidth, fill='red', width=1)
                gridMatrix[j][i] = 3


def separator(row_val):
    Label(rightFrame, text=" "*33).grid(row=row_val, column=1)


def horizontal_line(row_val):
    Label(rightFrame, text="_"*33, fg='gray').grid(row=row_val, column=1)


# Creates the buttons
def create_button(text, row_val, command):
    Button(rightFrame, text=text, width=20, command=command).grid(row=row_val, column=1, sticky=W)


# Create the radio button for start/goal
def create_radio_buttons(row_val):
    separator(row_val)
    horizontal_line(row_val+1)
    Label(rightFrame, text="Select Cell Type").grid(row=row_val+2, column=1, sticky=W)
    Radiobutton(rightFrame, text="Start", variable=var, value=2).grid(row=row_val+3, column=1, sticky=W)
    Radiobutton(rightFrame, text="Goal", variable=var, value=3).grid(row=row_val+4, column=1, sticky=W)
    horizontal_line(14)


# Creates and Displays the buttons on the right side of the screen
def create_side_elements():
    row_val = 4
    create_button("Upload Map", row_val, open_file)
    separator(row_val+1)
    create_button("A* Path finder", row_val+2, do_nothing)
    create_button("Q Learning", row_val+3, do_nothing)
    create_radio_buttons(row_val+4)


initialize_grid_matrix()
create_grid()
create_side_elements()





grid.bind('<Button-1>', add_start_goal_cell)

root.mainloop()
