from Tkinter import *


def doNothing():
    print("I wont do anything")

root = Tk()

# Creating Menu

menu = Menu(root)
root.config(menu=menu)

fileMenu = Menu(menu)
menu.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="New Project...", command=doNothing)
fileMenu.add_command(label="New", command=doNothing)
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=quit)


editMenu=Menu(menu)
menu.add_cascade(label="Edit", menu=editMenu)
editMenu.add_command(label="Redo", command= doNothing)

# Creating Toolbar

toolbar = Frame (root, bg="blue")

insertButton = Button(toolbar, text="Insert Image", command=doNothing)
insertButton.pack(side=LEFT, padx=2, pady=2)

printButton = Button(toolbar, text="Print something", command=doNothing)
printButton.pack(side=LEFT, padx=2, pady=2)

toolbar.pack(side=TOP, fill=X)


# Creating status bar

status = Label(root, text="Preparing...", bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)




root.mainloop()
