from agents.agent import Agent
from store import register_agent
import sys
import numpy as np
from copy import deepcopy
import time
from helpers import random_move, count_capture, execute_move, check_endgame, get_valid_moves

@register_agent("alphabeta_agent")
class AlphabetaAgent(Agent):

    def __init__(self):
        super(AlphabetaAgent, self).__init__()
        self.name = "AlphabetaAgent"

    @staticmethod    
    def utility(board, player, opponent):
        is_endgame, p1_score, p2_score = check_endgame(board, player, opponent)
        if not is_endgame:
            return None
        if player == 1:
            if p1_score > p2_score:
                return 1
            elif p1_score < p2_score:
                return -1
            else:
                return 0
        else:
            if p2_score > p1_score:
                return 1
            elif p2_score < p1_score:
                return -1
            else:
                return 0

    @staticmethod    
    def minimax(board, depth, alpha, beta, maximizing_player, current_player, other_player):
        util = AlphabetaAgent.utility(board,current_player,other_player)
        if util is not None:
            return util
        if depth == 0:
            return 0

        valid_moves = get_valid_moves(board,current_player)

        if not valid_moves:
            is_terminal, _, _ = check_endgame(board, current_player, other_player)
            if is_terminal:
                return AlphabetaAgent.utility(board, current_player,other_player)
            else:
                opponent_valid_moves = get_valid_moves(board, other_player)
                if not opponent_valid_moves:
                    return AlphabetaAgent.utility(board, current_player, other_player)
                else:
                    return Alpha.betaAgent.minimax(board, depth - 1, alpha, beta, not maximizing_player, other_player, current_player)

                


        if maximizing_player:
            print("entered max player loop")
            max_eval = -float('inf')
            for move in valid_moves:
                new_board = deepcopy(board)
                execute_move(new_board, move, current_player)
                eval = AlphabetaAgent.minimax(new_board, depth - 1, alpha, beta, False, other_player, current_player)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    print("exit max player loop")
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in valid_moves:
                print("enter min player loop")
                new_board = deepcopy(board)
                execute_move(new_board, move, current_player)
                eval = AlphabetaAgent.minimax(new_board, depth - 1, alpha, beta, True, other_player, current_player)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    print("exit min player loop")
                    break
            return min_eval

    def step(self, chess_board, player, opponent):
        start_time = time.time()
        depth = 10000
        valid_moves = get_valid_moves(chess_board, player)

        if not valid_moves:
            return None

        best_move = None
        best_score = -float('inf')
        alpha = -float('inf')
        beta = float('inf')


        for move in valid_moves:
            print("entered for loop in step")
            new_board = deepcopy(chess_board)
            execute_move(new_board, move, player)
            score = AlphabetaAgent.minimax(new_board, depth - 1, alpha, beta, False, player, opponent)
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)
            if beta <= alpha:
                print("exit for loop in step")
                break
        time_taken = time.time() - start_time

        print("My AI's turn took ", time_taken, "seconds.")
        return best_move
