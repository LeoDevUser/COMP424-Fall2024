from agents.agent import Agent
from store import register_agent
import sys
import numpy as np
from copy import deepcopy
import time
from helpers import random_move, count_capture, execute_move, check_endgame, get_valid_moves
import heapq

@register_agent("alpha2_agent")
class Alpha2Agent(Agent):

    def __init__(self):
        super(Alpha2Agent, self).__init__()
        self.name = "Alpha2Agent"
        self.boardfill = 0
        self.boardsize = -1
        self.avoid = [] #tells us which squares to avoid
        self.prefer = [] #tells us which squares to prioritize

    @staticmethod
    def evalfn(board, player, opponent):
        is_endgame, p0_score, p1_score = check_endgame(board, player, opponent)
        return (p0_score - p1_score)





    def updatefill(self, board, player):
        if self.boardsize == -1:
            self.boardsize = len(board) ** 2 #getboardsize
        count = 0
        for row in board:
            for entry in row:
                if entry != 0:
                    count += 1
        return count / self.boardsize


    def initavoid(self, board):
        for i in range(len(board)):
            self.avoid.append((1,i))
            self.avoid.append((len(board)-2,i))
            self.avoid.append((i,1))
            self.avoid.append((i,len(board)-2))

    def initprefer(self, board):
        #add corners
        size = len(board) - 1
        self.prefer.append((0,0))
        self.prefer.append((size,0))
        self.prefer.append((0,size))
        self.prefer.append((size,size))
        
    def promising_moves(self,valid_moves, board, player, opp, key):
        #returns up to 5 of the best moves
        #based on the utility of moves and position
        scores = []
        #compute the scores
        if len(self.avoid) == 0:
            self.initavoid(board)
        if len(self.prefer) == 0:
            self.initprefer(board)
        for move in valid_moves:
            simb = deepcopy(board)
            execute_move(simb,move,player)
            _,p1,p2 = check_endgame(simb, player, opp)
            if move in self.avoid:
                if key == find_low_n:
                    p1 += 3
                    p2 += 3
                else:
                    p1 -= 3
                    p2 -= 3
            if move in self.prefer:
                if key == find_low_n:
                    p1 -= 10
                    p2 -= 10
                else:
                    p1 += 10
                    p2 += 10
            if player == 1:
                scores.append((move,p1))
            else:
                scores.append((move,p2))
        return key(scores, 5)

















    


    
    @staticmethod
    def mc_eval(board, maximizing, player, opponent):
        is_endgame, p0_score, p1_score = check_endgame(board, player, opponent)
        if is_endgame:
            return Alpha2Agent.evalfn(board, player, opponent)
        
        if maximizing:
            move = random_move(board, player)
            if move == None: #if no avail moves for player
                is_endgame, _, _ = check_endgame(board, player, opponent) #check if game over
                if is_endgame:
                    return Alpha2Agent.evalfn(board, player, opponent)
                else:
                    move = random_move(board, opponent) #if not game over, generate play for opponent
                    if move == None:
                        return Alpha2Agent.evalfn(board, player, opponent) #if opponent also has no avail moves
                    board_copy = deepcopy(board)
                    execute_move(board_copy, move, opponent) 
                    return Alpha2Agent.mc_eval(board_copy, maximizing, player, opponent)
            
            board_copy = deepcopy(board)
            execute_move(board_copy, move, player)
            return Alpha2Agent.mc_eval(board_copy, not maximizing, player, opponent)
     
        else:
            move = random_move(board, opponent)
            if move == None: #if no avail moves for opponent
                is_endgame, _, _ = check_endgame(board, player, opponent) #check if game over
                if is_endgame:
                    return Alpha2Agent.evalfn(board, player, opponent)
                else:
                    move = random_move(board, player) #if not game over, generate play for player
                    if move == None:
                        return Alpha2Agent.evalfn(board, player, player) #if player also has no avail moves
                    board_copy = deepcopy(board)
                    execute_move(board_copy, move, player) 
                    return Alpha2Agent.mc_eval(board_copy, maximizing, player, opponent)
                        
            board_copy = deepcopy(board)
            execute_move(board_copy, move, opponent)
            return Alpha2Agent.mc_eval(board_copy, not maximizing, player, opponent)

    @staticmethod
    def montecarlo(board, maximizing, player, opponent, n_simulations):
        score_sum = 0
        for i in range(n_simulations):
            score_sum += Alpha2Agent.mc_eval(board, maximizing, player, opponent)

        return (score_sum/ n_simulations)



    
    def minimax(self, board, depth, alpha, beta, maximizing, player, opponent):
        is_endgame, p0_score, p1_score = check_endgame(board, player, opponent)    
        if   is_endgame or depth == 0:
            return p0_score - p1_score

        
        #if (depth == 0):
            #n = 3
            #return Alpha2Agent.montecarlo(board, maximizing, player, opponent, n)
            


        if maximizing:
            moves = get_valid_moves(board, player)

            if depth == 1:
                self.boardfill = Alpha2Agent.updatefill(self, board,player)
                maxscore = 0
                bestmove = None
                
                if self.boardfill < 0.3:
                    key = find_low_n
                else:
                    key = find_top_n

                moves = Alpha2Agent.promising_moves(self, moves, board, player, opponent, key)
            
            if moves == None:
            # Player has no valid moves; pass the turn to the opponent
                return Alpha2Agent.minimax(self, board, depth, alpha, beta, False, player, opponent)
            max_eval = -float('inf')

            
                
            
            for move in moves:
                board_copy = deepcopy(board)
                execute_move(board_copy, move, player)
                score_ = Alpha2Agent.minimax(self, board_copy, depth - 1, alpha, beta, False, player, opponent)
                max_eval = max(max_eval, score_)
                alpha = max(alpha, score_)
                if (beta <= alpha):
                    break

            return max_eval


        else:
            moves = get_valid_moves(board, opponent)

            if depth == 1:
                self.boardfill = Alpha2Agent.updatefill(self, board ,player)
                maxscore = 0
                bestmove = None
                
                if self.boardfill < 0.3:
                    key = find_low_n
                else:
                    key = find_top_n
        
                moves = Alpha2Agent.promising_moves(self, moves, board, player, opponent, key)




            
            if moves == None:
            # Opponent has no valid moves; pass the turn back to the player
                return Alpha2Agent.minimax(self, board, depth, alpha, beta, True, player, opponent)
            min_eval = float('inf')
            
            for move in moves:
                board_copy = deepcopy(board)
                execute_move(board_copy, move, opponent)
                score_ = Alpha2Agent.minimax(self, board_copy, depth - 1, alpha, beta, True, player, opponent)
                min_eval = min(min_eval, score_)
                beta = min(beta, score_)
                if (beta <= alpha):
                    break

            return min_eval
                    
                
            
            












    

    def step(self, chess_board, player, opponent):
        start_time = time.time()
        depth = 3
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
            score = Alpha2Agent.minimax(self, new_board, depth - 1, alpha, beta, False, player, opponent)
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        time_taken = time.time() - start_time

        print("My AI's turn took ", time_taken, "seconds.")
        return best_move





def find_top_n(nums, n):
    #Finds the n highest values in a list.
    #Create a heap of size n, with the smallest element at the top
    heap = []
    for tup in nums:
        heapq.heappush(heap, tup)
    return [tup[0] for tup in heapq.nlargest(n,heap, lambda x: x[1])]

def find_low_n(nums, n):
    #Finds the n highest values in a list.
    #Create a heap of size n, with the smallest element at the top
    heap = []
    for tup in nums:
        heapq.heappush(heap, tup)
    return [tup[0] for tup in heapq.nsmallest(n,heap, lambda x: x[1])]
