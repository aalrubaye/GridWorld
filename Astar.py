___author = "Abdul Rubaye"
import math

class Algorithm:
    gridMatrix = [[0 for row in range(10)] for col in range(10)]
    start = ()
    goal = ()

    open_list=[]
    close_list=[]

    def __init__(self, map_file, st, gl):
        global gridMatrix, start, goal, open_list
        gridMatrix = map_file

        open_list = [st]
        start = st
        goal = gl

    # Returns the neighbors of a node
    def neighbors(self, node):
        (x,y) = node
        i = x-1
        j = y-1
        for i in range(x-1,x+2):
            for j in range(y-1, y+2):
                if (i, j) != (x, y):
                    print (i,j,gridMatrix[i][j])


    def search(self):
        global start,open_list
        


    def heuristic(self, current):
        global goal
        (x1, y1) = current
        (x2, y2) = goal

        return math.sqrt(math.pow(abs(x2-x1),2) + math.pow(abs(y2-y1),2))










