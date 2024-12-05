from agents.agent import Agent
from store import register_agent
import sys
import numpy as np
from copy import deepcopy
import time
from helpers import random_move, count_capture, execute_move, check_endgame, get_valid_moves
import heapq

@register_agent("fifth_agent")
class FifthAgent(Agent):

    def __init__(self):
        super(FifthAgent, self).__init__()
        self.name = "FifthAgent"
        self.avoid = [] #tells us which squares to avoid
        self.corners = [] #corners
        self.prefer = [] #tells us which squares to prioritize
        self.start = 0

    def itDepth(self):
        elapsed = time.time() - self.start
        if elapsed < 0.4:
            return 5
        elif elapsed < 0.8:
            return 4
        elif elapsed < 1.2:
            return 3
        elif elapsed < 1.6:
            return 2
        else:
            return 1

    def initprefer(self, board):
        for i in range(len(board)):
            self.prefer.append((0,i))
            self.prefer.append((len(board)-1,0))
            self.prefer.append((i,0))
            self.prefer.append((i,len(board)-1))

    def initavoid(self, board):
        for i in range(2,len(board)):
            self.avoid.append((1,i))
            self.avoid.append((len(board)-2,i))
            self.avoid.append((i,1))
            self.avoid.append((i,len(board)-2))

    def initcorners(self, board):
        #add corners
        size = len(board) - 1
        self.corners.append((0,0))
        self.corners.append((size,0))
        self.corners.append((0,size))
        self.corners.append((size,size))
        
    def evaluate_board(self, board, player, opp):
        # Initialize score
        score = 0
    
        # Ensure avoid, prefer, and corners are initialized
        if not self.avoid:
            self.initavoid(board)
        if not self.prefer:
            self.initprefer(board)
        if not self.corners:
            self.initcorners(board)
    
        # Weights for different positions
        WEIGHT_CORNER = 25
        WEIGHT_PREFER = 5
        WEIGHT_AVOID = -5
    
        # Iterate over the board to calculate positional score
        for i in range(len(board)):
            for j in range(len(board)):
                pos = (i, j)
                if board[i][j] == player:
                    if pos in self.corners:
                        score += WEIGHT_CORNER
                    elif pos in self.prefer:
                        score += WEIGHT_PREFER
                    elif pos in self.avoid:
                        score += WEIGHT_AVOID
                    else:
                        score += 1  # Neutral position
                elif board[i][j] == opp:
                    if pos in self.corners:
                        score -= WEIGHT_CORNER
                    elif pos in self.prefer:
                        score -= WEIGHT_PREFER
                    elif pos in self.avoid:
                        score -= WEIGHT_AVOID
                    else:
                        score -= 1  # Neutral position
    
        # Mobility: Difference in number of valid moves
        player_moves = len(get_valid_moves(board, player))
        opp_moves = len(get_valid_moves(board, opp))
        score += (player_moves - opp_moves) + (player_moves - opp_moves)  # Mobility weight
    
        return score

    def minimax(self, board, depth, alpha, beta, maximizing, player, opponent):
        is_endgame, p0_score, p1_score = check_endgame(board, player, opponent)
        if is_endgame:
            # Assign a large positive or negative score based on the game result
            if p0_score > p1_score:
                return 1000 if player == 1 else -1000
            elif p0_score < p1_score:
                return -1000 if player == 1 else 1000
            else:
                return 0  # Draw

        if depth == 0:
            return self.evaluate_board(board, player, opponent)

        if maximizing:
            moves = get_valid_moves(board, player)
            if not moves:
            # Pass the turn to the opponent
                return self.minimax(board, min(depth - 1, self.itDepth() - 1), alpha, beta, False, player, opponent)
            max_eval = -float('inf')
            for move in moves:
                board_copy = deepcopy(board)
                execute_move(board_copy, move, player)
                score = self.minimax(board_copy, min(depth - 1, self.itDepth() - 1), alpha, beta, False, player, opponent)
                max_eval = max(max_eval, score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break  # Beta cut-off
            return max_eval
    
        else:
            moves = get_valid_moves(board, opponent)
            if not moves:
                # Pass the turn back to the player
                return self.minimax(board, min(depth - 1, self.itDepth() - 1), alpha, beta, True, player, opponent)
        min_eval = float('inf')
        for move in moves:
            board_copy = deepcopy(board)
            execute_move(board_copy, move, opponent)
            score = self.minimax(board_copy, min(depth - 1, self.itDepth() -1), alpha, beta, True, player, opponent)
            min_eval = min(min_eval, score)
            beta = min(beta, score)
            if beta <= alpha:
                break  # Alpha cut-off
        return min_eval
            
    def step(self, chess_board, player, opponent):
        self.start = time.time()
        valid_moves = get_valid_moves(chess_board, player)
        if not valid_moves:
            return None
    
        depth = self.itDepth()
    
        best_move = None
        best_score = -float('inf')
        alpha = -float('inf')
        beta = float('inf')
    
        for move in valid_moves:
            # Check time to avoid exceeding time limit
            time_taken = time.time() - self.start
            if time_taken > 1.9:
                break
            board_copy = deepcopy(chess_board)
            execute_move(board_copy, move, player)
            score = self.minimax(board_copy, min(depth - 1, self.itDepth() - 1), alpha, beta, False, player, opponent)
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break  # Alpha-beta pruning
    
        time_taken = time.time() - self.start
        print("My AI's turn took ", time_taken, "seconds.")
        return best_move
