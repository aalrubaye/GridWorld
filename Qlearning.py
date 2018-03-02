from random import *
import Cell
import Utility

___author = "Abdul Rubaye"


# The main class for Q-Learning implementation
class Algorithm:
    (grid_x, grid_y) = (Cell.World.X, Cell.World.Y)
    gridMatrix = [[0 for row in range(grid_y)] for col in range(grid_x)]
    qMatrix = [[0 for row in range(grid_y)] for col in range(grid_x)]
    actions = ['up','down','right','left']
    goal = ()

    def __init__(self, map_file):
        self.gridMatrix = map_file
        self.qMatrix = self.initialize_q_matrix()

    # Initializing the Q value matrix
    def initialize_q_matrix(self):
        q = [[[0 for _ in range(len(self.actions))] for _ in range(self.grid_y)] for _ in range(self.grid_x)]
        for i in range (self.grid_x):
            for j in range (self.grid_y):
                    if self.is_clear((i,j)):
                        for k in range(len(self.actions)):
                            q[i][j][k] = 0.0
                    else:
                        q[i][j] = None
        return q

    # Sets the probabilities of a state list according to max q value
    def stochastic_probabilities(self, state):
        index_of_max_q = self.max_q_index(state)
        probabilities = []
        index_list = []
        for i in range (4):
            index_list.append(i)
            if i == index_of_max_q:
                probabilities.append(0.6)
            else:
                probabilities.append(0.1)
        return probabilities

    # The implementation of epsilon greedy selection policy
    def e_greedy_policy(self, goal, parameters):
        self.goal = goal
        for i in range(50):
            current_state = self.initial_state()

            tries_to_terminate_episode = 0
            while current_state != self.goal and tries_to_terminate_episode <= 100:
                actions = self.find_possible_actions(current_state)
                rand_action = Utility.random_pick(self.stochastic_probabilities(current_state))
                next_state = actions[rand_action]

                # policyType = [softmax = 0, e-greedy = 1]
                self.update_q_value(current_state, rand_action, next_state, parameters, 1)
                if next_state is not None:
                    current_state = next_state
                tries_to_terminate_episode += 1
        return self.qMatrix

    # The implementation of softmax selection policy
    def soft_max_policy(self, goal, parameters):
        self.goal = goal

        # i number of episodes per execution
        for i in range(50):
            current_state = self.initial_state()
            tries_to_terminate_episode = 0
            # the episode will be terminated after the goal state is reached or a 100 episodes occur
            while current_state != self.goal and tries_to_terminate_episode <= 100:
                actions = self.find_possible_actions(current_state)
                # deterministic mode: to select an action with probability 1
                rand_action = randint(0,3)
                next_state = actions[rand_action]
                # policyType = [softmax = 0, e-greedy = 1]
                self.update_q_value(current_state, rand_action, next_state, parameters, 0)
                # print '{}->{}'.format(current_state,next_state)
                if next_state is not None:
                    current_state = next_state
                tries_to_terminate_episode += 1
        return self.qMatrix

    # Updates the Q value of a specific (S,a)
    def update_q_value(self, current, action, next_state, (alpha, gamma), policy_type):
        (x,y) = current
        self.qMatrix[x][y][action] += alpha*(self.calculate_q(current, next_state, gamma, policy_type) - self.qMatrix[x][y][action])

    # Calculates the q value of a specific (S,a) for a policy
    def calculate_q(self, current, next_state, gamma, policy_type):
        was_none = False
        if next_state is None:
            next_state = current
            was_none = True
        (x, y) = next_state

        index = self.max_q_index(next_state)
        max = self.qMatrix[x][y][index]

        probabilities = self.stochastic_probabilities(next_state)
        new_max = 0
        for i in range(4):
            if probabilities[i] != 0.6:
                new_max += (self.qMatrix[x][y][i] * 0.1)
            else:
                new_max += (self.qMatrix[x][y][i] * 0.6)

        if policy_type == 0:
            q_a = self.reward(next_state, was_none)+gamma*max
        else:

            q_a = self.reward(next_state, was_none)+gamma*new_max
        return q_a

    # Returns the max value among all the q values of a state and the index of the max value
    # the index is [0= top, 1= bottom, 2=right, 3=left]
    def max_q_index(self, state):
        if state is None:
            return 0

        max = self.q(state, 0)
        index = 0
        for i in range(1,4):
            q = self.q(state, i)
            if q > max:
                max = q
                index = i
        return index

    # Returns an random state that is used in the stochastic search
    def initial_state(self):
        while True:
            rand_x = randint(0, self.grid_x-1)
            rand_y = randint(0, self.grid_y-1)
            if self.is_clear((rand_x, rand_y)) is True:
                break
        random_state = (rand_x, rand_y)
        return random_state

    # Checks to see if a given state is clear
    def is_clear(self, state):
        if state is None:
            return False
        (x,y) = state
        val = self.gridMatrix[x][y]
        if val == 1:
            return False
        else:
            return True

    # Prints the q values
    def print_q(self):
        print ('-'*50)
        for i in range (self.grid_x):
            for j in range (self.grid_y):
                state = (i,j)
                if self.is_clear(state):
                    print '{} => t=({}), b=({}), r=({}), l=({})'.format(state, self.q(state,0),self.q(state,1),self.q(state,2),self.q(state,3))

        print ('-'*50)

    # Returns the q value of a (S,a)
    def q(self, state, a):
        (x,y) = state
        switcher = {
            0: self.qMatrix[x][y][0],
            1: self.qMatrix[x][y][1],
            2: self.qMatrix[x][y][2],
            3: self.qMatrix[x][y][3]
        }
        return switcher.get(a, None)

    # Returns the reward of an action
    # to reach to goal = 100
    # to reach an obstacle or a wall = -2
    # to do any other action = -1
    def reward(self,state, was_none):
        if was_none is True:
            return -2
        if state == self.goal:
            return 100
        return -1

    # Returns the possible actions of a state
    def find_possible_actions(self, state):
        actions = []
        direct_neighbors = Utility.direct_neighbors(state, self.grid_x, self.grid_y)

        # adding those direct neighbors of state that are not obstacles and not in OL
        for i in range (4):
            if self.is_clear(direct_neighbors[i]):
                actions.append(direct_neighbors[i])
            else:
                actions.append(None)
        return actions

