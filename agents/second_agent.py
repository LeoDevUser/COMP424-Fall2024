# Student agent: Add your own agent here
from agents.agent import Agent
from store import register_agent
import sys
import numpy as np
from copy import deepcopy
import time
from helpers import random_move, count_capture, execute_move, check_endgame, get_valid_moves
import heapq

@register_agent("second_agent")
class SecondAgent(Agent):

    def __init__(self):
        super(SecondAgent, self).__init__()
        self.name = "SecondAgent"
        self.boardfill = 0
        self.boardsize = -1
        self.avoid = [] #tells us which squares to avoid

    def updatefill(self, board, player):
        if self.boardsize == -1:
            self.boardsize = len(board) ** 2 #getboardsize
        count = 0
        for row in board:
            for entry in row:
                if entry != 0:
                    count += 1
        return count / self.boardsize


    @staticmethod
    def promising_moves(valid_moves, board, player, opp, key):
        #returns up to 5 of the best moves
        #currently based on the utility of such moves
        scores = []
        #compute the scores
        for move in valid_moves:
            simb = deepcopy(board)
            execute_move(simb,move,player)
            _,p1,p2 = check_endgame(simb, player, opp)
            if player == 1:
                scores.append((move,p1))
            else:
                scores.append((move,p2))
        return key(scores, 5)


    def step(self, chess_board, player, opponent):
        start_time = time.time()
        valid_moves = get_valid_moves(chess_board, player)
        if len(valid_moves) == 0:
            return None
        self.boardfill = SecondAgent.updatefill(self,chess_board,player)
        maxscore = 0
        bestmove = None
        
        if self.boardfill < 0.3:
            key = find_low_n
        else:
            key = find_top_n

        valid_moves = SecondAgent.promising_moves(valid_moves, chess_board, player, opponent, key)
        for move in valid_moves:
            simb = deepcopy(chess_board)#simulated board
            is_endgame = False
            execute_move(simb,move,player)
            is_endgame,p1,p2 = check_endgame(simb, player, opponent)
            simplayer = player
            avgscore = 0
            time_taken = time.time() - start_time

            if (time_taken > 1.9):#to avoid exceeding time
                break

            for i in range(5):
                #simulate 5 games per chosen moves
                counter  = 100;#only go down to specified depth
                simb2 = deepcopy(simb)#simulated board
                while(not is_endgame and counter > 0):
                    tmp = random_move(simb2, simplayer)
                    if (tmp != None):
                        execute_move(simb2,tmp,simplayer)
                        is_endgame,p1,p2 = check_endgame(simb2, player, opponent)
                    if (simplayer == player):
                        simplayer = (3 - player)
                    else:
                        simplayer = player
                    counter -= 1 #decrement counter

                if(player == 1):#we are player 1
                    avgscore += p1
                else:#we are player 2
                    avgscore += p2

            #compute avg score
            avgscore /= 5
            if (avgscore > maxscore):
                maxscore = avgscore
                bestmove = move

        time_taken = time.time() - start_time
        print("My AI's turn took ", time_taken, "seconds.")
        return bestmove

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
