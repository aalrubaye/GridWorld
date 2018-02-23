from Tkinter import *
from tkFileDialog import askopenfilename
import tkMessageBox

root = Tk()
root.title("GridWorld HomeWork")
root.resizable(width=FALSE, height=FALSE)
Width = 80

rightFrame = Frame(root)
rightFrame.pack(side=RIGHT, fill=Y)

var = IntVar()
var.set(1)

rightMargin = Label(rightFrame, text="    ", fg='white')
rightMargin.grid(row=0, column=1, sticky=W)

grid = Canvas(root, width=800, heigh=800, bg='red')

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


def insert_text_ql(x,y):
    grid.create_text(((x+0.5)*Width, (y+0.25)*Width), text="2", fill='black')
    grid.create_text(((x+0.25)*Width, (y+0.5)*Width), text="2", fill='black')
    grid.create_text(((x+0.75)*Width, (y+0.5)*Width), text="2", fill='black')
    grid.create_text(((x+0.5)*Width, (y+0.75)*Width), text="2", fill='black')


def insert_text_a_star(x,y):
    grid.create_text(((x+0.5)*Width, (y+0.25)*Width), text="text-top", fill='black')
    grid.create_text(((x+0.5)*Width, (y+0.5)*Width), text="text-mid", fill='black')
    grid.create_text(((x+0.5)*Width, (y+0.75)*Width), text="text-below", fill='black')


# Creates and renders the world grid
def create_grid():
    for i in range(x):
        for j in range(y):
            color = cell_color(gridMatrix[j][i])
            grid.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill=color, width=1)
    grid.pack(side=LEFT)
    # add_exploration_texts()

def add_exploration_texts():
    insert_text_a_star(2,2)
    insert_text_ql(1,1)
    grid.pack(side=LEFT)


# opens a map matrix from a file and renders it to the grid
def openFile():
    mapFile = askopenfilename(title = "Select map file")
    if len(mapFile) == 0:
        tkMessageBox.showwarning('No Selection', 'No map file was selected!')
    convert_file_to_matrix(mapFile)
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


def create_button(text,row,command) :
    button = Button(rightFrame, text=text, width=20, command=command)
    button.grid(row=row, column=0, sticky=W)

def create_radio_buttons():
    Label(rightFrame, text = "Select Cell Type").grid(row=9, sticky=W)
    Radiobutton(rightFrame, text = "Start", variable=var, value = 2).grid(row=10, sticky=W)
    Radiobutton(rightFrame, text = "Goal", variable=var, value = 3).grid(row=11, sticky=W)

def add_cell(e):
    (x, y) = (e.x/80, e.y/80)
    if (x < 10) & (y < 10):
        if gridMatrix[y][x] == 0:
            if var.get() == 2:
                grid.create_rectangle(x*Width, y*Width, (x+1)*Width, (y+1)*Width, fill='yellow', width=1)
                gridMatrix[y][x] = 2
            elif var.get() == 3:
                grid.create_rectangle(x*Width, y*Width, (x+1)*Width, (y+1)*Width, fill='red', width=1)
                gridMatrix[y][x] = 3

initialize_grid_matrix()
create_grid()
add_exploration_texts()

create_button("Upload Map", 6, openFile)
create_button("A* Path finder", 7, add_cell)
create_button("Q Learning", 8, do_nothing)


create_radio_buttons()

grid.bind('<Button-1>', add_cell)

root.mainloop()
