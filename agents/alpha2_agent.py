from agents.agent import Agent
from store import register_agent
import sys
import numpy as np
from copy import deepcopy
import time
from helpers import random_move, count_capture, execute_move, check_endgame, get_valid_moves

@register_agent("alpha2_agent")
class Alpha2Agent(Agent):

    def __init__(self):
        super(Alpha2Agent, self).__init__()
        self.name = "Alpha2Agent"


    def eval(board, player, opponent):
        is_endgame, p0_score, p1_score = check_endgame(board, player, opponent)
        return p0_score - p1_score


    def minimax(board, depth, alpha, beta, maximizing, player, opponent):
        is_endgame, p0_score, p1_score = check_endgame(board, player, opponent)
        
        if (depth == 0 or is_endgame):
            return eval(board, player, opponent)


        if maximizing:
            max_eval = -float('inf')
            moves = get_valid_moves(board, player)
            for move in moves:
                board_copy = deepcopy(board)
                execute_move(board_copy, move, player)
                eval = minimax(board_copy, depth - 1, alpha, beta, False, player, opponent)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if (beta <= alpha):
                    break

            return max_eval


        else:
            min_eval = float('inf')
            moves = get_valid_moves(board, opponent)
            for move in moves:
                board_copy = deepcopy(board)
                execute_move(board_copy, move, opponent)
                eval = minimax(board_copy, depth - 1, alpha, beta, True, player, opponent)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if (beta <= alpha):
                    break

            return min_eval
                    
                
            
            












    

    def step(self, chess_board, player, opponent):
        start_time = time.time()
        depth = 10
        valid_moves = get_valid_moves(chess_board, player)

        if not valid_moves:
            return None

        best_move = None
        best_score = -float('inf')
        alpha = -float('inf')
        beta = float('inf')


        for move in valid_moves:
            new_board = deepcopy(chess_board)
            execute_move(new_board, move, player)
            score = Alpha2Agent.minimax(new_board, depth - 1, alpha, beta, False, player, opponent)
            if score > best_score:
                best_score = score
                best_move = move
            #alpha = max(alpha, best_score)
            #if beta <= alpha:
                #break
        time_taken = time.time() - start_time

        print("My AI's turn took ", time_taken, "seconds.")
        return best_move
