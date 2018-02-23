from Tkinter import *

# creating a blank window
root = Tk()


# ----------- 2
# topFrame = Frame(root)
# topFrame.pack()
#
# bottomFrame = Frame(root)
# bottomFrame.pack(side=BOTTOM)
#
# button1 = Button(topFrame, text="A* Algorithm")
# button1.pack(side=LEFT)

# ----------- 3
# label1 = Label(root, text="A* Algorithm", fg="blue", bg="yellow")
# label2 = Label(root, text="D* Algorithm", fg="red", bg="pink")
# label3 = Label(root, text="QL Algorithm", fg="green", bg="gray")
#
# label1.pack()
# label2.pack(fill=X)
# label3.pack(side=LEFT, fill=Y)


# ----------- 4 & 5
# label1 = Label(root, text="A*")
# label2 = Label(root, text="D* Algorithm")
# entry1 = Entry(root)
# entry2 = Entry(root)
#
# #E,W,S,N
# label1.grid(row=0, column=0, sticky=E)
# label2.grid(row=1, column=0, sticky=W)
#
# entry1.grid(row=0, column=1)
# entry2.grid(row=1, column=1)
#
# check = Checkbutton(root, text="remember me")
# check.grid(columnspan=2)
#
# button1 = Button(root, text="submit")
# button1.grid(columnspan=2)



# ----------- 6
# def printmyname(event):
#     print("my name is Abdul")
#
# button1 = Button(root, text="Print my Name")
# button1.bind("<Button-1>",printmyname)
# button1.pack()


# ----------- 7
# frame = Frame(root, width=600, heigh=400)
# frame.pack()


# ----------- 8
# class BuckyButtons:
#     def __init__(self, master):
#         frame = Frame(master)
#         frame.pack()
#
#         self.printButton = Button(frame, text="Print message", command=self.printMessage)
#         self.printButton.pack(side=LEFT)
#
#         self.quitButton = Button(frame, text="Quit", command=frame.quit)
#         self.quitButton.pack(side=LEFT)
#
#     def printMessage(self):
#         print('This worked!')
#
# b = BuckyButtons(root)



# display the main window
root.mainloop()

