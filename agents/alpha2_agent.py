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

    @staticmethod    
    def utility(board, player, opponent):
        is_endgame, p1_score, p2_score = check_endgame(board, player, opponent)
        #if not is_endgame:
        #    return None
        if player == 1:
            if p1_score > p2_score:
                return p1_score - p2_score
            elif p1_score < p2_score:
                return p1_score - p2_score
            else:
                return 0
        else:
            if p2_score > p1_score:
                return p2_score - p1_score
            elif p2_score < p1_score:
                return p2_score - p1_score
            else:
                return 0

    @staticmethod    
    def minimax(board, depth, alpha, beta, maximizing_player, current_player, other_player):
        util = Alpha2Agent.utility(board,current_player,other_player)
        #if util is not None:
            #return util
        if depth == 0:
            return util

        valid_moves = get_valid_moves(board,current_player)

        if not valid_moves:
            is_terminal, _, _ = check_endgame(board, current_player, other_player)
            if is_terminal:
                return Alpha2Agent.utility(board, current_player,other_player)  #Could improve to simply return prev. calculated "util"
            else:
                opponent_valid_moves = get_valid_moves(board, other_player)
                if not opponent_valid_moves:
                    return Alpha2Agent.utility(board, current_player, other_player)  #same as above
                else:
                    return Alpha2Agent.minimax(board, depth - 1, alpha, beta, not maximizing_player, current_player, other_player)

                


        if maximizing_player:
            max_eval = -float('inf')
            for move in valid_moves:
                new_board = deepcopy(board)
                execute_move(new_board, move, current_player)
                eval = Alpha2Agent.minimax(new_board, depth - 1, alpha, beta, False, current_player, other_player)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in valid_moves:
                new_board = deepcopy(board)
                execute_move(new_board, move, current_player)
                eval = Alpha2Agent.minimax(new_board, depth - 1, alpha, beta, True, current_player, other_player)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
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
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        time_taken = time.time() - start_time

        print("My AI's turn took ", time_taken, "seconds.")
        return best_move
