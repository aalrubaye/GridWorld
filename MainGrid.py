from tkinter import *
import ttk
from tkFileDialog import askopenfilename
import tkMessageBox
import threading
import queue
import Cell
import Qlearning
import Astar

___author = "Abdul Rubaye"


# The main class that includes the GUI interface
class MainApp:
    global root, rightFrame, leftFrame, radio_button_value,grid, gridMatrix, qMatrix, qlearner

    cellWidth = Cell.World.CELL_WIDTH
    is_start_created = False
    is_goal_created = False
    start = ()
    goal = ()
    (grid_x, grid_y) = (Cell.World.X, Cell.World.Y)
    qMatrix_calculated = False
    pause = False
    entry = "1"
    element_order = 3

    def __init__(self, root):
        self.root = root
        self.root.title("GridWorld HomeWork")
        self.root.resizable(width=FALSE, height=FALSE)
        self.rightFrame = Frame(self.root)
        self.rightFrame.pack(side=RIGHT, fill=Y)
        self.leftFrame = Frame(self.root)
        self.leftFrame.pack(side=LEFT, fill=Y)
        Label(self.rightFrame, text="    ", fg='white').grid(row=0, column=2, sticky=W)
        Label(self.rightFrame, text="    ", fg='white').grid(row=0, column=0, sticky=E)

        self.grid = Canvas(self.leftFrame, width=800, heigh=800)

        self.gridMatrix = [[0 for row in range(self.grid_y)] for col in range(self.grid_x)]
        self.qMatrix = [[0 for row in range(self.grid_y)] for col in range(self.grid_x)]

        self.qlearner = Qlearning.Algorithm(self.gridMatrix)
        self.qMatrix_calculated = False

        self.radio_button_value = IntVar()
        self.radio_button_value.set(1)

        self.set_new_grid()
        self.create_left_side_elements()
        self.grid.bind('<Button-2>', self.reset_start_goal_cell)
        self.grid.bind('<Button-1>', self.add_start_goal_cell)

    # The world grid matrix initializer
    def initialize_grid_matrix(self):
        for i in range(self.grid_x):
            for j in range(self.grid_y):
                self.gridMatrix[i][j] = 0

    # Used to reset/set a new grid
    def set_new_grid(self):
        self.initialize_grid_matrix()
        self.create_grid()
        self.goal = ()
        self.start = ()
        self.is_start_created = False
        self.is_goal_created = False

    # Returns a cell color based on the value from the map matrix
    def cell_color(self, value):
        switcher = {
            0: Cell.Color.CLEAR,
            1: Cell.Color.OBSTACLE,
            2: Cell.Color.START,
            3: Cell.Color.GOAL
        }
        return switcher.get(value, Cell.Color.CLEAR)


    def ql_color(self, top,bottom,right,left):
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
    def insert_text_ql(self, x, y, q_matrix):

        top = round(q_matrix[0],1)
        bottom = round(q_matrix[1],1)
        right = round(q_matrix[2],1)
        left = round(q_matrix[3],1)

        qlc = self.ql_color(top,bottom,right,left)
        self.grid.create_rectangle(x*self.cellWidth, y*self.cellWidth, (x+1)*self.cellWidth, (y+1)*self.cellWidth, fill=qlc, width=1)

        self.grid.create_text(((x+0.5)*self.cellWidth, (y+0.25)*self.cellWidth), text=top, fill='black')
        self.grid.create_text(((x+0.5)*self.cellWidth, (y+0.75)*self.cellWidth), text=bottom, fill='black')
        self.grid.create_text(((x+0.75)*self.cellWidth, (y+0.5)*self.cellWidth), text=right, fill='black')
        self.grid.create_text(((x+0.25)*self.cellWidth, (y+0.5)*self.cellWidth), text=left, fill='black')

    # Adds the text for A_star path planning
    def insert_text_a_star(self, x, y, routeNode):
        cost = "d="+ str(routeNode.distance)
        fscore = "f="+str(round(routeNode.f_score,1))
        heuristic = "h="+str(round(routeNode.heuristic,1))
        self.grid.create_text(((x+0.5)*self.cellWidth, (y+0.25)*self.cellWidth), text=fscore, fill='black')
        self.grid.create_text(((x+0.5)*self.cellWidth, (y+0.5)*self.cellWidth), text=cost, fill='black')
        self.grid.create_text(((x+0.5)*self.cellWidth, (y+0.75)*self.cellWidth), text=heuristic, fill='black')

    # Creates and renders the world grid
    def create_grid(self):
        for i in range(self.grid_x):
            for j in range(self.grid_y):
                color = self.cell_color(self.gridMatrix[j][i])
                self.grid.create_rectangle(i*self.cellWidth, j*self.cellWidth, (i+1)*self.cellWidth, (j+1)*self.cellWidth, fill=color, width=1)
        self.grid.pack(side=LEFT)

    # opens a map matrix from a file and renders it to the grid
    def open_file(self):
        print (self.entry)
        map_file = askopenfilename(title="Select map file")
        if len(map_file) == 0:
            tkMessageBox.showwarning('No Selection', 'No map file was selected!')
        self.convert_file_to_matrix(map_file)
        self.create_grid()
        self.is_start_created = False
        self.is_goal_created = False

    # Returns orders of the right side elements
    def get_elements_order(self):
        self.element_order += 1
        return self.element_order

    # converts a map file content to a grid matrix
    def convert_file_to_matrix(self, map_file):
        content = open(map_file, "r")
        index_i = 0
        for line in content:
            index_j = 0
            number_strings = line.split()
            for val in number_strings:
                self.gridMatrix[index_i][index_j] = int(val)
                index_j += 1
            index_i += 1

    # Adds the start cell or goal cell via click event
    def add_start_goal_cell(self,coordination):
        (i, j) = (coordination.x/self.cellWidth, coordination.y/self.cellWidth)
        if (i < self.grid_x) & (j < self.grid_y):
            if self.gridMatrix[j][i] == Cell.Type.CLEAR:
                if (self.radio_button_value.get() == 2) & (self.is_start_created is False):
                    self.grid.create_rectangle(i*self.cellWidth, j*self.cellWidth, (i+1)*self.cellWidth, (j+1)*self.cellWidth,
                                          fill=Cell.Color.START, width=1)
                    self.grid.create_text(((i+0.5)*self.cellWidth, (j+0.5)*self.cellWidth), text="Start", fill='black')
                    self.gridMatrix[j][i] = Cell.Type.START
                    self.start = (j,i)
                    self.is_start_created = True
                elif (self.radio_button_value.get() == 3) & (self.is_goal_created is False):
                    self.grid.create_rectangle(i*self.cellWidth, j*self.cellWidth, (i+1)*self.cellWidth, (j+1)*self.cellWidth,
                                          fill=Cell.Color.GOAL, width=1)
                    self.grid.create_text(((i+0.5)*self.cellWidth, (j+0.5)*self.cellWidth), text="Goal", fill='black')
                    self.gridMatrix[j][i] = Cell.Type.GOAL
                    self.goal = (j,i)
                    self.is_goal_created = True

    # Resets the start cell or goal cell via click event
    def reset_start_goal_cell(self, coordination):
        global is_start_created, is_goal_created, start, goal
        (i, j) = (coordination.x/self.cellWidth, coordination.y/self.cellWidth)
        if (i < self.grid_x) & (j < self.grid_y):
            if self.gridMatrix[j][i] == Cell.Type.START:
                if self.radio_button_value.get() == 2:
                    self.grid.create_rectangle(i*self.cellWidth, j*self.cellWidth, (i+1)*self.cellWidth, (j+1)*self.cellWidth,
                                          fill=Cell.Color.CLEAR, width=1)
                    self.gridMatrix[j][i] = Cell.Type.CLEAR
                    start = ()
                    is_start_created = False
            elif self.gridMatrix[j][i] == Cell.Type.GOAL:
                if self.radio_button_value.get() == 3:
                    self.grid.create_rectangle(i*self.cellWidth, j*self.cellWidth, (i+1)*self.cellWidth, (j+1)*self.cellWidth,
                                          fill=Cell.Color.CLEAR, width=1)
                    self.gridMatrix[j][i] = Cell.Type.CLEAR
                    goal = ()
                    is_goal_created = False

    # Renders a horizontal gray line
    def horizontal_line(self):
        ttk.Separator(self.rightFrame, orient="horizontal").grid(row=self.get_elements_order(),column=1,sticky="ew",padx=10, pady=10)

    # Creates the buttons
    def create_button(self, text, width, command):
        return Button(self.rightFrame, text=text, width=width, command=command).grid(row=self.get_elements_order(), column=1, sticky=W)

    # Creates and Displays the buttons on the right side of the screen
    def create_left_side_elements(self):
        self.create_button("Upload Map",  20, self.open_file)
        self.create_button("Reset Grid", 20, self.set_new_grid)
        self.horizontal_line()
        self.create_radio_buttons()
        self.horizontal_line()
        Label(self.rightFrame, text="Q-Learning Path Finder").grid(row=self.get_elements_order(), column=1, sticky=W)
        self.create_button("Start QL", 20, self.update_text)
        self.create_button("Pause", 20, self.pause_q_learning)
        self.create_button("Find Path", 20, self.find_path_ql)
        Label(self.rightFrame, text="Enter Speed (1 to 10)").grid(row=self.get_elements_order(), column=1, sticky=W)
        Entry(self.rightFrame, textvariable=self.entry).grid(row=self.get_elements_order(), column=1, sticky=W)
        self.horizontal_line()
        Label(self.rightFrame, text="A* Path Finder").grid(row=self.get_elements_order(), column=1, sticky=W)
        self.create_button("Start A*", 20, self.a_star)

    # Pauses the QL learning algorithm
    def pause_q_learning(self):
        self.pause = True
        self.pqb.config(text='Loop terminated')

    # Creates the radio button for start/goal
    def create_radio_buttons(self):
        Label(self.rightFrame, text="Cell to add/remove?").grid(row=self.get_elements_order(), column=1, sticky=W)
        Radiobutton(self.rightFrame, text="Start", variable=self.radio_button_value, value=2).grid(row=self.get_elements_order(), column=1, sticky=W)
        Radiobutton(self.rightFrame, text="Goal", variable=self.radio_button_value, value=3).grid(row=self.get_elements_order(), column=1, sticky=W)

    # The main function that calls the QL algorithm
    def q_learning(self, tt):
        self.create_grid()
        if self.goal == ():

            tkMessageBox.showwarning('No Goal', 'Please select the goal state!')
            return
        self.qMatrix = self.qlearner.learn(self.goal)
        self.qMatrix_calculated = True
        tt.put(0)

    # Populate the q matrix value after each episode
    def create_gg(self):
            for i in range(self.grid_x):
                for j in range(self.grid_y):
                    if self.gridMatrix[i][j] == Cell.Type.CLEAR:
                        self.insert_text_ql(j, i, self.qMatrix[i][j])
                    if self.gridMatrix[i][j] == Cell.Type.GOAL:
                        self.grid.create_text(((j+0.5)*self.cellWidth, (i+0.5)*self.cellWidth), text="Goal", fill='black')

    # Finds the path after the ql algorithm is done
    def find_path_ql(self):

        if self.start == ():
            tkMessageBox.showwarning('No Start', 'Please select the start state!')
            return
        if self.qMatrix_calculated is False:
            tkMessageBox.showwarning('QLearning Error', 'Please run the Q Learning Algorithm')
            return
        current = self.start
        path = []
        while current != self.goal:
            max_q_index = self.qlearner.max_q_index(current)
            next_state = self.next_state_on_path(current, max_q_index)
            if next_state != self.goal:
                path.append(next_state)
            current = next_state

        for (i,j) in path:
            self.grid.create_rectangle(j*self.cellWidth, i*self.cellWidth, (j+1)*self.cellWidth, (i+1)*self.cellWidth,fill='green', width=1)

    # the main function of the A* algorithm
    def a_star(self):
        if (self.start != ()) and (self.goal != ()):
            astar = Astar.Algorithm(self.gridMatrix, self.start, self.goal)
            (x,y) = self.goal
            (x_start, y_start) = self.start
            (evaluated_nodes, path) = astar.search()

            cellWidth = self.cellWidth

            if evaluated_nodes:
                for i in range (self.grid_x):
                    for j in range (self.grid_y):
                        if evaluated_nodes[i][j] != 0:
                            if (i,j) == (x,y):
                                self.grid.create_rectangle(j*cellWidth, i*cellWidth, (j+1)*cellWidth, (i+1)*cellWidth,fill=Cell.Color.GOAL, width=1)
                            elif (i,j) in path:
                                self.grid.create_rectangle(j*cellWidth, i*cellWidth, (j+1)*cellWidth, (i+1)*cellWidth,fill='green', width=1)
                            else:
                                self.grid.create_rectangle(j*cellWidth, i*cellWidth, (j+1)*cellWidth, (i+1)*cellWidth,fill=Cell.Color.VISITED, width=1)
                            self.insert_text_a_star(j,i,evaluated_nodes[i][j])
                self.grid.create_text(((y_start+0.5)*cellWidth, (x_start+0.5)*cellWidth), text='Start', fill='black')
            else:
                tkMessageBox.showwarning('No Route Found', 'There is no possible route to the goal! You still can re select either one of the start or goal cell.')
        else:
            tkMessageBox.showwarning('Required Values', 'Make sure you select the start and goal cells!')

    # Find the states on the path for QL Algorithm
    def next_state_on_path(self, state, index):
        (x,y) = state
        switcher = {
            0: (x-1, y),
            1: (x+1, y),
            2: (x, y+1),
            3: (x, y-1)
        }
        return switcher.get(index, (x,y))

    # The main function that runs the QLearner using threading
    def update_text(self):
        '''
        Spawn a new thread for running long loops in background
        '''
        self.thread_queue = queue.Queue()

        # self.new_thread = threading.Thread(target=runloop(self.thread_queue))
        self.new_thread = threading.Thread(target=self.q_learning(self.thread_queue))
        self.new_thread.start()
        self.root.after(1, self.listen_for_result())

    # Fetches the results and renderds them via threading
    def listen_for_result(self):
        '''
        Check if there is something in the queue
        '''
        try:
            self.res = self.thread_queue.get(0)
            self.create_gg()
            if self.pause is False:
                self.root.after(700, self.update_text)
        except queue.Empty:
            self.root.after(1000, self.listen_for_result)


# MAIN
if __name__ == "__main__":
    root = Tk()
    main_app = MainApp(root)

    root.mainloop()
