from tkinter import *
import ttk
from tkFileDialog import askopenfilename
import tkMessageBox
import threading
import queue
import Cell
import Qlearning
import Astar
import Utility
import numpy
import pprint

___author = "Abdul Rubaye"


# The main class that includes the GUI interface
class MainApp:
    cellWidth = Cell.World.CELL_WIDTH
    is_start_created = False
    is_goal_created = False
    start = ()
    goal = ()
    (grid_x, grid_y) = (Cell.World.X, Cell.World.Y)
    qMatrix_calculated = False
    pause = False
    right_elements_starting_row = 3
    path = 0
    alpha_text_var = None
    gamma_text_var = None

    def __init__(self, root):
        self.root = root
        self.root.title("My GridWorld")
        self.root.resizable(width=FALSE, height=FALSE)
        self.rightFrame = Frame(self.root)
        self.rightFrame.pack(side=RIGHT, fill=Y)
        self.leftFrame = Frame(self.root)
        self.leftFrame.pack(side=LEFT, fill=Y)
        Label(self.rightFrame, text="    ", fg='white').grid(row=0, column=2, sticky=W)
        Label(self.rightFrame, text="    ", fg='white').grid(row=0, column=0, sticky=E)

        self.grid = Canvas(self.leftFrame, width=640, heigh=640)

        self.gridMatrix = [[0 for row in range(self.grid_y)] for col in range(self.grid_x)]
        self.qMatrix = [[0 for row in range(self.grid_y)] for col in range(self.grid_x)]

        self.qlearner = Qlearning.Algorithm(self.gridMatrix)
        self.qMatrix_calculated = False
        # Radio Buttons for Add/remove cell section
        self.cell_radio_btn_val = IntVar()
        self.cell_radio_btn_val.set(1)
        # Radio Buttons for QL selection policies
        self.policy_radio_btn_val = IntVar()
        self.policy_radio_btn_val.set(1)
        # Radio Buttons for heat map selection
        self.heatmap_radio_btn_val = IntVar()
        self.heatmap_radio_btn_val.set(2)
        self.set_new_grid()
        self.create_left_side_elements()
        self.grid.bind('<Button-2>', self.reset_start_goal_cell)
        self.grid.bind('<Button-1>', self.add_start_goal_cell)
        self.alpha_text_var = StringVar()
        self.gamma_text_var = StringVar()

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
        self.qMatrix = None

    # Renders the heatmap after each episode
    def heat_map(self, x, y, cell_q_values):
        q_vals = Utility.q_values(cell_q_values)
        cellWidth = self.cellWidth
        if self.heatmap_radio_btn_val.get() == 2:
            self.grid.create_rectangle(x*cellWidth, y*cellWidth, (x+1)*cellWidth, (y+1)*cellWidth, fill=Utility.ql_color(q_vals), width=1)
        else:
            self.grid.create_polygon([x*cellWidth,y*cellWidth,x*cellWidth,(y+1)*cellWidth,(x+0.5)*cellWidth,(y+0.5)*cellWidth,x*cellWidth,y*cellWidth], fill=Utility.poly_color(q_vals[3]), width=1, outline='gray')
            self.grid.create_polygon([x*cellWidth,y*cellWidth,(x+1)*cellWidth,y*cellWidth,(x+0.5)*cellWidth,(y+0.5)*cellWidth,x*cellWidth,y*cellWidth], fill=Utility.poly_color(q_vals[0]), width=1, outline='gray')
            self.grid.create_polygon([x*cellWidth,(y+1)*cellWidth,(x+1)*cellWidth,(y+1)*cellWidth,(x+0.5)*cellWidth,(y+0.5)*cellWidth,x*cellWidth,(y+1)*cellWidth], fill=Utility.poly_color(q_vals[1]), width=1, outline='gray')
            self.grid.create_polygon([(x+1)*cellWidth,y*cellWidth,(x+1)*cellWidth,(y+1)*cellWidth,(x+0.5)*cellWidth,(y+0.5)*cellWidth,(x+1)*cellWidth,y*cellWidth], fill=Utility.poly_color(q_vals[2]), width=1, outline='gray')

        self.insert_text_ql(x,y,cell_q_values)

    # Adds the text for QL path planning
    def insert_text_ql(self, x, y, cell_q_values):
        q_vals = Utility.q_values(cell_q_values)
        self.grid.create_text(((x+0.5)*self.cellWidth, (y+0.25)*self.cellWidth), text=q_vals[0], fill='black')
        self.grid.create_text(((x+0.5)*self.cellWidth, (y+0.75)*self.cellWidth), text=q_vals[1], fill='black')
        self.grid.create_text(((x+0.75)*self.cellWidth, (y+0.5)*self.cellWidth), text=q_vals[2], fill='black')
        self.grid.create_text(((x+0.25)*self.cellWidth, (y+0.5)*self.cellWidth), text=q_vals[3], fill='black')

    # Adds the text for A_star path planning
    def insert_text_a_star(self, x, y, routeNode):
        fscore = "f="+str(round(routeNode.f_score,1))
        cost = "g="+ str(routeNode.distance)
        heuristic = "h="+str(round(routeNode.heuristic,1))
        self.grid.create_text(((x+0.5)*self.cellWidth, (y+0.25)*self.cellWidth), text=fscore, fill='black')
        self.grid.create_text(((x+0.5)*self.cellWidth, (y+0.5)*self.cellWidth), text=cost, fill='black')
        self.grid.create_text(((x+0.5)*self.cellWidth, (y+0.75)*self.cellWidth), text=heuristic, fill='black')

    # Creates and renders the world grid
    def create_grid(self):
        for i in range(self.grid_x):
            for j in range(self.grid_y):
                color = Utility.cell_color(self.gridMatrix[j][i])
                self.grid.create_rectangle(i*self.cellWidth, j*self.cellWidth, (i+1)*self.cellWidth, (j+1)*self.cellWidth, fill=color, width=1)
        self.grid.pack(side=LEFT)

    # Opens a map matrix from a file and renders it to the grid
    def open_file(self):
        map_file = askopenfilename(title="Select map file")
        if len(map_file) == 0:
            tkMessageBox.showwarning('No Selection', 'No map file was selected!')
        self.goal = ()
        self. start = ()
        self.is_start_created = False
        self.is_goal_created = False
        self.convert_file_to_matrix(map_file)
        self.create_grid()
        self.pause = False
        self.path = 0

    # Returns an specific color for each one of the paths
    def get_path_color(self):
        switcher = {
            0: ("#ff8586","#ce9ec9"),
            1: ("#cd85ff","#9c9dfc"),
            2: ("#858aff","#4dc8f6")
        }
        path = self.path
        self.path += 1
        return switcher.get(path, ("#ff8586","#ce9ec9"))

        self.path += 1

    # Returns orders of the right side elements
    def get_elements_order(self):
        self.right_elements_starting_row += 1
        return self.right_elements_starting_row

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
                if (self.cell_radio_btn_val.get() == 2) & (self.is_start_created is False):
                    self.grid.create_rectangle(i*self.cellWidth, j*self.cellWidth, (i+1)*self.cellWidth, (j+1)*self.cellWidth,
                                          fill=Cell.Color.START, width=1)
                    self.grid.create_text(((i+0.5)*self.cellWidth, (j+0.5)*self.cellWidth), text="Start", fill='black')
                    self.gridMatrix[j][i] = Cell.Type.START
                    self.start = (j,i)
                    self.is_start_created = True
                elif (self.cell_radio_btn_val.get() == 3) & (self.is_goal_created is False):
                    self.grid.create_rectangle(i*self.cellWidth, j*self.cellWidth, (i+1)*self.cellWidth, (j+1)*self.cellWidth,fill=Cell.Color.GOAL, width=1)
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
                if self.cell_radio_btn_val.get() == 2:
                    self.gridMatrix[j][i] = Cell.Type.CLEAR
                    self.start = ()
                    self.is_start_created = False
            elif self.gridMatrix[j][i] == Cell.Type.GOAL:
                if self.cell_radio_btn_val.get() == 3:
                    self.grid.create_rectangle(i*self.cellWidth, j*self.cellWidth, (i+1)*self.cellWidth, (j+1)*self.cellWidth,fill=Cell.Color.CLEAR, width=1)
                    self.gridMatrix[j][i] = Cell.Type.CLEAR
                    self.goal = ()
                    self.is_goal_created = False

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
        Label(self.rightFrame, text="Cell to add/remove?").grid(row=self.get_elements_order(), column=1, sticky=W)
        self.create_radio_buttons("Start State", "Goal State", self.cell_radio_btn_val)
        self.horizontal_line()
        Label(self.rightFrame, text="Q-Learning Path Finder").grid(row=self.get_elements_order(), column=1, sticky=W)
        self.create_radio_buttons("Softmax Policy", "epsilon-greedy Policy", self.policy_radio_btn_val)
        self.create_button("Start QL", 20, self.run_through_threading)
        self.create_button("Pause", 20, self.pause_q_learning)
        self.create_button("Find Path", 20, self.find_path_ql)
        self.horizontal_line()
        Label(self.rightFrame, text="A* Path Finder").grid(row=self.get_elements_order(), column=1, sticky=W)
        self.create_button("Start A*", 20, self.a_star)
        self.horizontal_line()
        Label(self.rightFrame, text="Select the type of the heat map:").grid(row=self.get_elements_order(), column=1, sticky=W)
        self.create_radio_buttons("Total Reward Heat Map", "Polygon Heat Map", self.heatmap_radio_btn_val)
        self.horizontal_line()
        self.alpha_entry = Entry(self.rightFrame, textvariable=self.alpha_text_var)
        Label(self.rightFrame, text="alpha:").grid(row=self.get_elements_order(), column=1, sticky=W)
        self.alpha_entry.insert(0, "1")
        self.alpha_entry.grid(row=self.get_elements_order(), column=1, sticky=W)
        Label(self.rightFrame, text="gamma:").grid(row=self.get_elements_order(), column=1, sticky=W)
        self.gamma_entry = Entry(self.rightFrame, textvariable=self.gamma_text_var)
        self.gamma_entry.insert(0, "0.8")
        self.gamma_entry.grid(row=self.get_elements_order(), column=1, sticky=W)

    # Pauses the QL learning algorithm
    def pause_q_learning(self):
        self.pause = True

    # Creates the radio button for start/goal
    def create_radio_buttons(self, text1, text2, variable):
        Radiobutton(self.rightFrame, text=text1, variable=variable, value=2).grid(row=self.get_elements_order(), column=1, sticky=W)
        Radiobutton(self.rightFrame, text=text2, variable=variable, value=3).grid(row=self.get_elements_order(), column=1, sticky=W)

    # The main function that calls the QL algorithm
    def q_learning(self, tt):
        self.create_grid()
        alpha = float(self.alpha_entry.get())
        gamma = float(self.gamma_entry.get())
        if self.goal == ():
            tkMessageBox.showwarning('No Goal', 'Please select the goal state!')
            return

        if self.policy_radio_btn_val.get() == 2:
            self.qMatrix = self.qlearner.soft_max_policy(self.goal, (alpha,gamma))
            self.qMatrix_calculated = True
            tt.put(0)
            #todo disable the radio button so no more interactions occure
        elif self.policy_radio_btn_val.get() == 3:
            self.qMatrix = self.qlearner.e_greedy_policy(self.goal, (alpha, gamma))
            self.qMatrix_calculated = True
            tt.put(0)
        else:
            tkMessageBox.showwarning('No Policy', 'Please select the selection policy before the Qlearning alg starts!')
            return

    # Populate the q matrix value after each episode
    def populate_q_to_graph(self):
            for i in range(self.grid_x):
                for j in range(self.grid_y):
                    if self.gridMatrix[i][j] == Cell.Type.CLEAR:
                        self.heat_map(j, i, self.qMatrix[i][j])
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
        path.append(current)
        while current != self.goal:
            max_q_index = self.qlearner.max_q_index(current)
            while True:
                next_state = Utility.next_state_on_path(current, max_q_index)
                (x,y) = next_state
                if self.gridMatrix[x][y] != Cell.Type.OBSTACLE:
                    break
            if next_state != self.goal:
                path.append(next_state)
            current = next_state
        (path_color, start_color) = self.get_path_color()
        for (i,j) in path:
            if (i,j) == self.start:
                self.grid.create_rectangle(j*self.cellWidth, i*self.cellWidth, (j+1)*self.cellWidth, (i+1)*self.cellWidth,fill=start_color, width=1)
                self.grid.create_text(((j+0.5)*self.cellWidth, (i+0.5)*self.cellWidth), text="Start", fill='black')
            else:
                self.grid.create_rectangle(j*self.cellWidth, i*self.cellWidth, (j+1)*self.cellWidth, (i+1)*self.cellWidth,fill=path_color, width=1)
                self.insert_text_ql(j,i,self.qMatrix[i][j])

    # the main function of the A* algorithm
    def a_star(self):
        if (self.start != ()) and (self.goal != ()):
            astar = Astar.Algorithm(self.gridMatrix, self.start, self.goal)
            (x,y) = self.goal
            # (x_start, y_start) = self.start
            (evaluated_nodes, path) = astar.search()

            cellWidth = self.cellWidth
            g_matrix = [[0 for _ in range(self.grid_y)] for _ in range(self.grid_x)]

            (path_color,start_color) = self.get_path_color()
            if evaluated_nodes:
                for i in range(self.grid_x):
                    for j in range(self.grid_y):
                        if evaluated_nodes[i][j] != 0:
                            if (i,j) == (x,y):
                                self.grid.create_rectangle(j*cellWidth, i*cellWidth, (j+1)*cellWidth, (i+1)*cellWidth,fill=Cell.Color.GOAL, width=1)
                            elif (i,j) == self.start:
                                self.grid.create_rectangle(j*cellWidth, i*cellWidth, (j+1)*cellWidth, (i+1)*cellWidth,fill=start_color, width=1)
                            elif (i,j) in path:
                                self.grid.create_rectangle(j*cellWidth, i*cellWidth, (j+1)*cellWidth, (i+1)*cellWidth,fill=path_color, width=1)
                            else:
                                self.grid.create_rectangle(j*cellWidth, i*cellWidth, (j+1)*cellWidth, (i+1)*cellWidth,fill=Cell.Color.VISITED, width=1)

                            self.insert_text_a_star(j, i, evaluated_nodes[i][j])

            else:
                tkMessageBox.showwarning('No Route Found', 'There is no possible route to the goal! You still can re select either one of the start or goal cell.')
        else:
            tkMessageBox.showwarning('Required Values', 'Make sure you select the start and goal cells!')

        print ('-'*100)
        print('the path is = ', path)
        print ('-'*100)

    # The main function that runs the QLearner using threading
    # Spawn a new thread for running long loops in background
    def run_through_threading(self):
        self.thread_queue = queue.Queue()
        self.new_thread = threading.Thread(target=self.q_learning(self.thread_queue))
        self.new_thread.start()
        self.root.after(1, self.listen_for_result())

    # Fetches the results and renderds them via threading
    def listen_for_result(self):
        try:
            res = self.thread_queue.get(0)
            if self.qMatrix_calculated is True:
                self.populate_q_to_graph()
                if self.pause is False:
                    self.root.after(1200, self.run_through_threading)
        except queue.Empty:
            self.root.after(1000, self.listen_for_result)


# MAIN
if __name__ == "__main__":
    root = Tk()
    main_app = MainApp(root)
    root.mainloop()
