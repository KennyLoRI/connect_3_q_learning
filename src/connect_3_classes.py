import numpy as np
import random
random.seed(42)

"""
Defining the environemnt class of a connect-3 game on a 3x3 grid. 
It consists of: 
- Initialization 
- Reset function (to start a new game)
- Function to determine available actions for a given state
- Function to perform an action 
- Function to check if end-state is reached. If yes: determine the winner
"""

class connect_three_board:

    def __init__(self):
        # initialize the the playing board as empty
        self.board = np.zeros((3,3))
        self.players = [1,-1] # Agend and opponent
        self.current_player = 1 # Agent makes first move

    def reset(self):
        self.board = np.zeros((3,3))
        self.current_player = 1 # Agent makes first move again

    def get_available_actions(self):
        # available action is throwing a stone into every column whose upmost element is empty (i.e. not yet full)
        return [col for col in range(3) if self.board[0][col]==0]

    def is_valid_action(self, action):
        # check if a certain action is valid
        return action in self.get_available_actions()

    def apply_action(self, action):
        # iterate through each row from bottom (2) to top (0) (-1 is last)
        for row in range(2,-1,-1):
            #place the piece of the player into the first free field of the column chosen as column to act on
            if self.board[row][action]==0:
                self.board[row][action]=self.current_player
                break #stop filling in pieces if one piece is filled in


    def check_winner(self):
        for player in self.players:
            #check if 3 pieces in a row
            for row in range(3):
                if all(self.board[row][col]==player for col in range(3)):
                    return player
            #check if 3 pieces in a column
            for col in range(3):
                if all(self.board[row][col]==player for row in range(3)):
                    return player
            ##check if 3 pieces in diagonal
            #left or right diagonal
            if all(self.board[i,i]==player for i in range(3)) or all(self.board[i,2-i]==player for i in range(3)):
                return player

        return 0 #if not yet a winner exists

class agent:
    def __init__(self, q_table = {}, exp_rate = 0.1, learn_rate = 0.05, discount_rate=0.95):
        self.exp_rate = exp_rate
        self.learn_rate = learn_rate
        self.discount_rate=discount_rate
        self.q_table = q_table

    def get_q_value(self, state, action):
        #return q value of state-action pair in q-table.
        # Return 0, if pair does not exist yet, and create the entry in the q_table
        return self.q_table.get((state, action), 0.0)

    def update_q_value(self, state, action, reward, next_state):
        #determine best_next action of all available actions
        #Shuffle to ensure we not always pick the first value, if all next_state, action pairs have value 0
        best_next_action = np.argmax([self.get_q_value(next_state, a) for a in range(3)])
        new_q_value = self.get_q_value(state,action) + self.learn_rate * (reward + self.discount_rate * self.get_q_value(next_state, best_next_action) - self.get_q_value(state,action))
        self.q_table[(state, action)] = new_q_value

    def choose_action(self, state, available_actions):
        if random.uniform(0,1) < self.exp_rate:
            return random.choice(available_actions)
        else:
            #to make sure we choose a random action, if the q valu is 0 everywhere at the beginning
            shuffled_actions = np.random.permutation(available_actions)
            action_index = np.argmax([self.get_q_value(state, a) for a in shuffled_actions])
            selected_action = shuffled_actions[action_index]
            return selected_action










