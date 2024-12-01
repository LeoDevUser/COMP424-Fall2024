# Student agent: Add your own agent here
from agents.agent import Agent
from store import register_agent
import sys
import numpy as np
from copy import deepcopy
import time
from helpers import random_move, count_capture, execute_move, check_endgame, get_valid_moves
import heapq

@register_agent("third_agent")
class ThirdAgent(Agent):

    def __init__(self):
        super(ThirdAgent, self).__init__()
        self.name = "ThirdAgent"
        self.boardfill = 0
        self.boardsize = -1
        self.avoid = [] #tells us which squares to avoid
        self.corners = [] #corners
        self.prefer = [] #tells us which squares to prioritize

    def updatefill(self, board, player):
        if self.boardsize == -1:
            self.boardsize = len(board) ** 2 #getboardsize
        count = 0
        for row in board:
            for entry in row:
                if entry != 0:
                    count += 1
        return count / self.boardsize


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
            #now, we want to minimize the avail moves for the opp
            opp_score = len(get_valid_moves(simb, 3 - player))
            if move in self.avoid:
                if key == find_low_n:
                    p1 += 6
                    p2 += 6
                else:
                    p1 -= 6
                    p2 -= 6
            if move in self.corners:
                if key == find_low_n:
                    p1 -= 12
                    p2 -= 12
                else:
                    p1 += 12
                    p2 += 12
            if move in self.prefer:
                if key == find_low_n:
                    p1 -= 6
                    p2 -= 6
                else:
                    p1 += 6
                    p2 += 6

            #adjust to minimize opp avail moves
            if key == find_low_n:
                p1 += opp_score
                p2 += opp_score
            else:
                p2 -= opp_score
                p2 -= opp_score

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
        if self.boardfill < 0.25:
            self.boardfill = ThirdAgent.updatefill(self,chess_board,player)
        maxscore = 0
        bestmove = None
        
        if self.boardfill < 0.25:
            key = find_low_n
        else:
            key = find_top_n

        valid_moves = ThirdAgent.promising_moves(self,valid_moves, chess_board, player, opponent, key)
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
                #simulate 6 games per chosen moves
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
