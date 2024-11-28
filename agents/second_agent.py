# Student agent: Add your own agent here
from agents.agent import Agent
from store import register_agent
import sys
import numpy as np
from copy import deepcopy
import time
from helpers import random_move, count_capture, execute_move, check_endgame, get_valid_moves

@register_agent("second_agent")
class SecondAgent(Agent):
  """
  A class for your implementation. Feel free to use this class to
  add any helper functionalities needed for your agent.
  """

  def __init__(self):
    super(SecondAgent, self).__init__()
    self.name = "SecondAgent"

  def step(self, chess_board, player, opponent):
    """
    Implement the step function of your agent here.
    You can use the following variables to access the chess board:
    - chess_board: a numpy array of shape (board_size, board_size)
      where 0 represents an empty spot, 1 represents Player 1's discs (Blue),
      and 2 represents Player 2's discs (Brown).
    - player: 1 if this agent is playing as Player 1 (Blue), or 2 if playing as Player 2 (Brown).
    - opponent: 1 if the opponent is Player 1 (Blue), or 2 if the opponent is Player 2 (Brown).

    You should return a tuple (r,c), where (r,c) is the position where your agent
    wants to place the next disc. Use functions in helpers to determine valid moves
    and more helpful tools.

    Please check the sample implementation in agents/random_agent.py or agents/human_agent.py for more details.
    """
    start_time = time.time()
    valid_moves = get_valid_moves(chess_board, player)
    if len(valid_moves) == 0:
        return None
    maxscore = 0
    bestmove = None

    
    for move in valid_moves:
        simb = deepcopy(chess_board)#simulated board
        is_endgame = False
        score = 0
        execute_move(simb,move,player)
        is_endgame,p1,p2 = check_endgame(simb, player, opponent)
        simplayer = player
        time_taken = time.time() - start_time

        if (time_taken > 1.9):#to avoid exceeding time
            break
        counter  = 100;#only go down to depth 100
        while(not is_endgame and counter > 0):
            tmp = random_move(simb, simplayer)
            if (tmp != None):
                execute_move(simb,tmp,simplayer)
                is_endgame,p1,p2 = check_endgame(simb, player, opponent)
            if (simplayer == player):
                simplayer = (3 - player)
            else:
                simplayer = player
            counter -= 1 #decrement counter

        if(player == 1):#we are player 1
            score = p1
        else:#we are player 2
            score = p2

        if (score > maxscore):
            maxscore = score
            bestmove = move

    # Some simple code to help you with timing. Consider checking 
    # time_taken during your search and breaking with the best answer
    # so far when it nears 2 seconds.
    time_taken = time.time() - start_time

    print("My AI's turn took ", time_taken, "seconds.")
    return bestmove

