import RouteNode
import Cell
import Utility

___author = "Abdul Rubaye"


# The main class for A-Star implementation
class Algorithm:
    (grid_x, grid_y) = (Cell.World.X, Cell.World.Y)
    gridMatrix = [[0 for row in range(grid_y)] for col in range(grid_x)]
    start = ()
    goal = ()
    open_list = []
    close_list = []
    route_nodes = []

    def __init__(self, map_file, st, gl):
        self.gridMatrix = map_file
        self.open_list = [st]
        self.close_list = []
        self.start = st
        self.goal = gl
        self.route_nodes = [[0 for _ in range(self.grid_y)] for _ in range(self.grid_x)]

    # Finds the neighbors of a state
    def find_neighbors(self, node):
        neighbors_list = []
        (x,y) = node

        direct_neighbors = Utility.direct_neighbors(node, self.grid_x, self.grid_y)

        top_right = (x-1,y+1) if ((x-1) > -1) and ((y+1) < self.grid_y) else None
        bottom_right = (x+1, y+1) if ((x+1) < self.grid_x) and ((y+1) < self.grid_y) else None
        top_left = (x-1,y-1) if ((x-1) > -1) and ((y-1) > -1) else None
        bottom_left = (x+1, y-1) if ((x+1) < self.grid_x) and ((y-1) > -1) else None

        indirect_neighbors = [top_left, top_right, bottom_left, bottom_right]

        # adding those direct neighbors of node that are not obstacles and not in OL
        for i in range(4):
            if self.is_new_valid_neighbor(direct_neighbors[i]):
                neighbors_list.append(direct_neighbors[i])

        # adding those indirect neighbors of node that are not blocked or obstacles
        k = 0
        for i in range(2):
            for j in range(2,4):
                if self.is_clear(direct_neighbors[i]) or self.is_clear(direct_neighbors[j]):
                    if self.is_new_valid_neighbor(indirect_neighbors[k]):
                        neighbors_list.append(indirect_neighbors[k])
                k += 1

        return neighbors_list

    # Returns true if the node is not in OL and not obstacle
    def is_new_valid_neighbor(self, node):
        clear = self.is_clear(node)
        if clear and node not in self.open_list:
            return True
        else:
            return False

    # Checks a state if it's a clear one
    def is_clear(self, node):
        if node is None:
            return False
        (x,y) = node
        val = self.gridMatrix[x][y]
        if val == 1:
            return False
        else:
            return True

    # Add states to the open list
    def add_to_open_list(self, neighbor_list, parent_node):

        for i in range(len(neighbor_list)):
            if neighbor_list[i] not in self.close_list:
                if neighbor_list[i] not in self.open_list:
                    self.open_list.append(neighbor_list[i])
                    routeNode = RouteNode.New(parent_node)
                    routeNode.distance = self.cost(parent_node) + Utility.linear_distance(parent_node, neighbor_list[i])
                    (x,y) = neighbor_list[i]
                    self.route_nodes[x][y] = routeNode
                    self.route_nodes[x][y].f_score = self.f_score(neighbor_list[i])
                    self.route_nodes[x][y].heuristic = Utility.heuristic(neighbor_list[i], self.goal)

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

    # Finds the route going backward from goal to start
    def find_route(self):

        current = self.goal

        route = []
        neighbors = Utility.direct_neighbors(current, self.grid_x, self.grid_y)

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
                if self.route_nodes[x][y].distance < self.route_nodes[x_min][y_min].distance:
                    min_cell = sortable[i]
                    (x_min,y_min) = sortable[i]
            route.append(min_cell)
            neighbors = Utility.direct_neighbors(min_cell, self.grid_x, self.grid_y)
        route.append(self.start)
        return route

    # Calculates g(n)
    def cost(self, node):
        (x, y) = node
        if node == self.start:
            return 0
        else:
            return self.route_nodes[x][y].distance

    # Calculates f(n)
    def f_score(self, node):
        return self.cost(node) + Utility.heuristic(node, self.goal)

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
