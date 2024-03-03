import numpy as np
import random

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
        self.players = [1,-1] # player A and player B
        self.current_player = random.choice(self.players)

    def reset(self):
        self.board = np.zeros((3,3))
        self.current_player = random.choice(self.players)

    def get_available_actions(self):
        # available action is throwing a stone into every column whose upmost element is empty (i.e. not yet full)
        return [col for col in range(3) if self.board[0][col]==0]

    def is_valid_action(self, action):
        # check if a certain action is valid
        return action in self.get_available_actions()

    def apply_ation(self, action):
        # iterate through each row from bottom (2) to top (0) (-1 is last)
        for row in range(2,-1,-1):
            #place the piece of the player into the first free field of the column chosen as column to act on
            if self.board[row][action]==0:
                self.board[row][action]=self.current_player
                break

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






env = connect_three_board()
print(env.board[0])


