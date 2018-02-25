___author = "Abdul Rubaye"
from random import *
import math

class Algorithm:
    gridMatrix = [[0 for row in range(10)] for col in range(10)]
    qMatrix = [[0 for row in range(10)] for col in range(10)]

    def __init__(self, map_file):
        self.gridMatrix = map_file
        self.qMatrix = self.initialize_q_matrix()


    def initialize_q_matrix(self):
        q = [[0 for row in range(10)] for col in range(10)]
        for i in range (10):
            for j in range (10):
                 q[i][j]= 0.0
        return q

    def learn(self):
        print self.initial_node()

    def initial_node(self):
        rand_x = randint(0, 10)
        rand_y = randint(0, 10)

        while self.is_clear((rand_x, rand_y)) is False:
            rand_x = randint(0, 10)
            rand_y = randint(0, 10)

        random_node = (rand_x, rand_y)
        return random_node

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
