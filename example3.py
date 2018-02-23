from Tkinter import *
from PIL import ImageTk,Image
import tkinter.messagebox
root = Tk()

# -------dialog messages
# tkinter.messagebox.showinfo('window Title', 'Monkey can live up to 200 years')
#
# answer = tkinter.messagebox.askquestion('Qustion 1', 'Do you like me ?')
# if answer == 'yes' :
#     print ('Thank you')


# canvas = Canvas(root, width=200, height=100)
# canvas.pack()
#
# blackline = canvas.create_line(0,0, 200,50)
# redline = canvas.create_line(0,100,200,50, fill="red")
# greenBox = canvas.create_rectangle(25,25,130,60, fill="Green")
#
# canvas.delete(redline)
# canvas.delete(ALL)

# displaying an image
canvas = Canvas(root, width = 300, height = 300)
canvas.pack()
img = ImageTk.PhotoImage(Image.open("smiley.png"))
canvas.create_image(20, 20, anchor=NW, image=img)


root.mainloop()
