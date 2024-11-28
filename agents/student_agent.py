# Student agent: Add your own agent here
from agents.agent import Agent
from store import register_agent
import sys
import numpy as np
from copy import deepcopy
import time
from helpers import random_move, count_capture, execute_move, check_endgame, get_valid_moves

@register_agent("student_agent")
class StudentAgent(Agent):
  """
  A class for your implementation. Feel free to use this class to
  add any helper functionalities needed for your agent.
  """

  def __init__(self):
    super(StudentAgent, self).__init__()
    self.name = "StudentAgent"

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
    valid_moves = get_valid_moves(chess_board, player)
    if len(valid_moves) == 0:
        # If no valid moves are available, return None
        #print(f"No valid OUR CODE OUR CODE moves left for player {player}.")
        return None
    maxscore = 0
    bestmove = None

    for i in range(5):
        simb = deepcopy(chess_board)
        is_endgame = False;
        move = random_move(simb, player)
        #print("NO MOVES AFTER 1ST RANDMOVE")
        score = 0
        if (move != None):
            execute_move(simb,move,player)
        else:
            return None

        is_endgame,p1,p2 = check_endgame(simb, player, opponent)
        if (is_endgame):
          print("ENDGAME POSITION")

        while(not is_endgame):
            tmp = random_move(simb, player)
            if (tmp != None):
                execute_move(simb,move,player)
            else:
                break
                execute_move(simb,tmp,player)
                is_endgame,p1,p2 = check_endgame(simb, player, opponent)

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
    start_time = time.time()
    time_taken = time.time() - start_time

    print("My AI's turn took ", time_taken, "seconds.")

    # Dummy return (you should replace this with your actual logic)
    # Returning a random valid move as an example
    return bestmove

