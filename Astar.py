___author = "Abdul Rubaye"
import math
import RouteNode

class Algorithm:
    gridMatrix = [[0 for row in range(10)] for col in range(10)]
    start = ()
    goal = ()
    open_list=[]
    close_list=[]

    def __init__(self, map_file, st, gl):
        self.gridMatrix = map_file
        self.open_list = [st]
        self.close_list = []
        self.start = st
        self.goal = gl

    # Returns the neighbors of a node
    def find_neighbors(self, node):

        neighbors_list = []

        (x,y) = node

        offset_x = x-1 if x>0 else 0
        offset_y = y-1 if y>0 else 0

        for i in range(offset_x,x+2):
            for j in range(offset_y, y+2):
                if (i, j) != (x, y):
                    if (i,j) not in self.open_list:
                        neighbors_list.append((i,j))
        return neighbors_list

    #todo switcher
    def node_status(self, node):

        (x,y) = node
        val = self.gridMatrix[x][y]
        if val == 0:
            return "Clear"
        elif val == 1:
            return "Obstacle"
        elif val == 2:
            return "Start"
        else:
            return "Goal"


    def add_to_open_list(self, neighbor_list, parent_node):

        for i in range(len(neighbor_list)):
            if neighbor_list[i] not in self.close_list:
                if (neighbor_list[i] not in self.open_list) and (self.node_status(neighbor_list[i]) != "Obstacle"):
                    self.open_list.append(neighbor_list[i])
                    nn = RouteNode.New(parent_node)
                    print (neighbor_list[i], nn.parent_node)




    # The main function of the short path search
    def search(self):
        self.printoc()
        current = self.fetch_from_open_list()
        self.printoc()
        if current == self.goal:
            print ("we are in the goal state")
        else:
            # Find the neighbors of the current node
            neighbors = self.find_neighbors(current)
            # Add the neighbors of the current node to the OL if not there yet
            self.add_to_open_list(neighbors, current)
            self.printoc()




    # Calculates h(n)
    def heuristic(self, current):
        (x1, y1) = current
        (x2, y2) = self.goal
        return math.sqrt(math.pow(abs(x2-x1), 2) + math.pow(abs(y2-y1), 2))

    # Calculates g(n)
    def cost(self, current):
        (x1, y1) = self.start
        (x2, y2) = current
        if current == self.start:
            return 0
        else:
            return -1

    # Calculates f(n)
    def f_score(self, node):
        return self.cost(node) + self.heuristic(node)

    # Returns the node with shortest estimated distance
    def fetch_from_open_list(self):
        if len(self.open_list) == 0:
            return ()
        elif len(self.open_list) == 1:
            node = self.open_list[0]
            self.close_list.append(node)
            self.open_list.remove(node)
            return node
        else:
            min_cost = self.f_score(open_list[0])
            (x_min, y_min) = self.open_list[0]
            for i in range(1, len(self.open_list)):
                if self.f_score(self.open_list[i]) < min_cost:
                    min_cost = self.f_score(self.open_list[i])
                    (x_min, y_min) = self.open_list[i]
            node = (x_min, y_min)
            self.close_list.append(node)
            self.open_list.remove(node)
            return node


    def printoc(self):
        print ("OL = ", self.open_list)
        print ("CL = ", self.close_list)
        print ("--------------------")
