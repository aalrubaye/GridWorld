from Tkinter import *

class World:
    master = None
    rightFrame = None
    leftFrame = None
    grid = None
    (grid_x, grid_y) = (800,800)

    def __init__(self,root):
        self.master = root
        self.rightFrame = Frame(root)
        self.rightFrame.pack(side=RIGHT, fill=Y)
        self.leftFrame = Frame(root)
        set.leftFrame.pack(side=LEFT, fill=Y)
        self.grid = Canvas(self.leftFrame, width=800, heigh=800)
        self.create_button("Print hello", 2, doexpensive)


    def create_grid(self):
        for i in range(self.grid_x):
            for j in range(self.grid_y):
                self.grid.create_rectangle(i*80, j*80, (i+1)*80, (j+1)*80, fill='red', width=1)
        self.grid.pack(side=LEFT)

    def create_button(self, text, row_val, command):
        return Button(self.rightFrame, text=text, width=20, command=command).grid(row=row_val, column=1, sticky=W)
