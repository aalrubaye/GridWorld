___author = "Abdul Rubaye"
from random import *
import time
import Cell

class Algorithm:
    (grid_x, grid_y) = (Cell.World.X, Cell.World.Y)
    gridMatrix = [[0 for row in range(grid_y)] for col in range(grid_x)]
    qMatrix = [[0 for row in range(grid_y)] for col in range(grid_x)]
    actions = ['up','down','right','left']
    goal = ()
    gamma = 0.8

    def __init__(self, map_file):
        self.gridMatrix = map_file
        self.qMatrix = self.initialize_q_matrix()
        print self.grid_x, self.grid_y


    def initialize_q_matrix(self):
        q = [[[0 for _ in range(len(self.actions))] for _ in range(self.grid_y)] for _ in range(self.grid_x)]
        for i in range (self.grid_x):
            for j in range (self.grid_y):
                    if self.is_clear((i,j)):
                        for k in range (len(self.actions)):
                            q[i][j][k] = 0.0
                    else:
                        q[i][j] = None
        return q

    def e_greedy_policy(self, goal):
        print('Nothing implemnted yet!')

    def soft_max_policy(self, goal):
        self.goal = goal

        # i number of episodes per execution
        for i in range(3):
            current_state = self.initial_state()

            while current_state != self.goal:
                actions = self.find_possible_actions(current_state)

                # deterministic mode: to select an action with probability 1
                rand_action = randint(0,3)
                next_state = actions[rand_action]
                (x,y) = current_state
                self.qMatrix[x][y][rand_action] = self.calculate_q(next_state)
                # print '{}->{}'.format(current_state,next_state)
                if next_state is not None:
                    current_state = next_state

            # self.print_q()
            print (time.time())
        return self.qMatrix

    def calculate_q(self, next_state):
        if next_state is None:
            max = 0
        else:
            (x,y) = next_state
            index = self.max_q_index(next_state)
            max = self.qMatrix[x][y][index]

        q_a = self.reward(next_state)+self.gamma*max
        return q_a

    # Returns the max value among all the q values of a state and the index of the max value
    # the index is [0= top, 1= bottom, 2=right, 3=left]
    def max_q_index(self, state):
        if state is None:
            return 0

        max = self.q(state, 0)
        index = 0
        for i in range (1,4):
            q = self.q(state, i)
            if q > max:
                max = q
                index = i
        return index

    def initial_state(self):
        rand_x = randint(0, self.grid_x-1)
        rand_y = randint(0, self.grid_y-1)

        while self.is_clear((rand_x, rand_y)) is False:
            rand_x = randint(0, self.grid_x-1)
            rand_y = randint(0, self.grid_y-1)

        random_state = (rand_x, rand_y)
        return random_state

    #todo switcher
    def is_clear(self, state):
        if state is None:
            return False
        (x,y) = state
        val = self.gridMatrix[x][y]
        if val == 1:
            return False
        else:
            return True

    def print_q(self):
        print ('-'*50)
        for i in range (self.grid_x):
            for j in range (self.grid_y):
                state = (i,j)
                if self.is_clear(state):
                    print '{} => t=({}), b=({}), r=({}), l=({})'.format(state, self.q(state,0),self.q(state,1),self.q(state,2),self.q(state,3))

        print ('-'*50)


    def q(self,state,a):
        (x,y) = state
        switcher = {
            0: self.qMatrix[x][y][0],
            1: self.qMatrix[x][y][1],
            2: self.qMatrix[x][y][2],
            3: self.qMatrix[x][y][3]
        }
        return switcher.get(a, None)

    def reward(self,state):
        if state == self.goal:
            return 100
        else:
            return -1

    def direct_neighbors(self, state):
        (x,y) = state
        top = (x-1, y) if (x-1) > -1 else None
        bottom = (x+1, y) if (x+1) < self.grid_x else None
        right = (x, y+1) if (y+1) < self.grid_y else None
        left = (x, y-1) if (y-1) > -1 else None

        return [top,bottom,right,left]

    def find_possible_actions(self, state):
        actions = []
        direct_neighbors = self.direct_neighbors(state)

        # adding those direct neighbors of state that are not obstacles and not in OL
        for i in range (4):
            if self.is_clear(direct_neighbors[i]):
                actions.append(direct_neighbors[i])
            else:
                actions.append(None)
        return actions

    #todo switcher
    def is_clear(self, state):
        if state is None:
            return False
        (x,y) = state
        val = self.gridMatrix[x][y]
        if val == 1:
            return False
        else:
            return True
