___author = "Abdul Rubaye"
import math
import RouteNode

class Algorithm:
    (grid_x, grid_y) = (10, 10)
    gridMatrix = [[0 for row in range(grid_y)] for col in range(grid_x)]
    start = ()
    goal = ()
    open_list=[]
    close_list=[]
    route_nodes = []

    def __init__(self, map_file, st, gl):
        self.gridMatrix = map_file
        self.open_list = [st]
        self.close_list = []
        self.start = st
        self.goal = gl
        self.route_nodes = [[0 for row in range(self.grid_y)] for col in range(self.grid_x)]


    def direct_neighbors(self, node):
        (x,y) = node
        top = (x-1, y) if (x-1) > -1 else None
        bottom = (x+1, y) if (x+1) < self.grid_x else None
        left = (x, y-1) if (y-1) > -1 else None
        right = (x, y+1) if (y+1) < self.grid_y else None

        return [top,bottom,left,right]


    def find_neighbors(self, node):
        neighbors_list = []
        (x,y) = node

        direct_neighbors = self.direct_neighbors(node)

        top_right = (x-1,y+1) if ((x-1) > -1) and ((y+1) < self.grid_y) else None
        bottom_right = (x+1, y+1) if ((x+1) < self.grid_x) and ((y+1) < self.grid_y) else None
        top_left = (x-1,y-1) if ((x-1) > -1) and ((y-1) > -1) else None
        bottom_left = (x+1, y-1) if ((x+1) < self.grid_x) and ((y-1) > -1) else None

        indirect_neighbors = [top_left, top_right, bottom_left, bottom_right]

        # adding those direct neighbors of node that are not obstacles and not in OL
        for i in range (4):
            if self.is_new_valid_neighbor(direct_neighbors[i]):
                neighbors_list.append(direct_neighbors[i])

        # adding those indirect neighbors of node that are not blocked or obstacles
        k = 0
        for i in range(2):
            for j in range(2,4):
                if self.is_clear(direct_neighbors[i]) or self.is_clear(direct_neighbors[j]):
                    if self.is_new_valid_neighbor(indirect_neighbors[k]):
                        neighbors_list.append(indirect_neighbors[k])
                k +=1

        return neighbors_list

    # Returns true if the node is not in OL and not obstacle
    def is_new_valid_neighbor(self, node):
        clear = self.is_clear(node)
        if clear and node not in self.open_list:
            return True
        else:
            return False

    #todo switcher
    def is_clear(self, node):
        if node is None:
            return False
        (x,y) = node
        val = self.gridMatrix[x][y]
        if val == 1:
            return False
        else:
            return True


    def add_to_open_list(self, neighbor_list, parent_node):

        for i in range(len(neighbor_list)):
            if neighbor_list[i] not in self.close_list:
                if neighbor_list[i] not in self.open_list:
                    self.open_list.append(neighbor_list[i])
                    routeNode = RouteNode.New(parent_node)
                    routeNode.distance = self.cost(parent_node) + self.linear_distance(parent_node, neighbor_list[i])
                    (x,y) = neighbor_list[i]
                    self.route_nodes[x][y] = routeNode
                    self.route_nodes[x][y].f_score = self.f_score(neighbor_list[i])
                    self.route_nodes[x][y].heuristic = self.heuristic(neighbor_list[i])

    # The main function of the short path search
    def search(self):
        current = self.fetch_from_open_list()
        if len(current) == 0:
            return None
        if current == self.goal:
            path = self.find_route()
            return (self.route_nodes, path)
        else:
            # Find the neighbors of the current node
            neighbors = self.find_neighbors(current)
            # Add the neighbors of the current node to the OL if not there yet
            self.add_to_open_list(neighbors, current)
            return self.search()


    def find_route(self):

        current = self.goal

        route = []
        neighbors = self.direct_neighbors(current)

        while self.start not in neighbors:
            sortable = []
            for i in range(4):
                if self.is_clear(neighbors[i]):
                    (x,y) = neighbors[i]
                    if self.route_nodes[x][y] != 0:
                        sortable.append(neighbors[i])

            min_cell = sortable[0]
            (x_min,y_min) = sortable[0]

            for i in range (1, len(sortable)):
                (x,y) = sortable[i]
                one = self.route_nodes[x][y].distance
                two = self.route_nodes[x_min][y_min].distance
                if one < two :
                    min_cell = sortable[i]
                    (x_min,y_min) = sortable[i]
            route.append(min_cell)
            neighbors = self.direct_neighbors(min_cell)

        return route

    # Calculates h(n)
    def heuristic(self, current):
        (x1, y1) = current
        (x2, y2) = self.goal
        return math.sqrt(math.pow(abs(x2-x1), 2) + math.pow(abs(y2-y1), 2))

    # Calculates g(n)
    def cost(self, node):
        (x, y) = node
        if node == self.start:
            return 0
        else:
            return self.route_nodes[x][y].distance

    def linear_distance(self, node1, node2):
        if node1 == node2:
            return 0
        (x1,y1) = node1
        (x2,y2) = node2

        dx = abs(x1-x2)
        dy = abs(y1-y2)

        neighbor_cells = True if (dx == 1) or (dy==1) else False

        if ((y1 == y2) or (x1 == x2)) and neighbor_cells:
            return 1
        else:
            return 2

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
            min_cost = self.f_score(self.open_list[0])
            (x_min, y_min) = self.open_list[0]
            for i in range(1, len(self.open_list)):
                if self.f_score(self.open_list[i]) < min_cost:
                    min_cost = self.f_score(self.open_list[i])
                    (x_min, y_min) = self.open_list[i]
            node = (x_min, y_min)
            self.close_list.append(node)
            self.open_list.remove(node)
            return node

