
import numpy as np

"""
Helpers.py is a collection of functions that primarily make up the Reversi/Othello game logic.
Beyond a few things in the World init, which can be copy/pasted this should be almost
all of what you'll need to simulate games in your search method.

Functions:
    get_directions    - a simple helper to deal with the geometry of Reversi moves
    count_capture     - how many flips does this move make. Game logic defines valid moves as those with >0 returns from this function. 
    count_capture_dir - a helper for the above, unlikely to be used externally
    execute_move      - update the chess_board by simulating a move
    flip_disks        - a helper for the above, unlikely to be used externally
    check_endgame     - check for termination, who's won but also helpful to score non-terminated games
    get_valid_moves   - use this to get the children in your tree
    random_move       - basis of the random agent and can be used to simulate play

    For all, the chess_board is an np array of integers, size nxn and integer values indicating square occupancies.
    The current player is (1: Blue, 2: Brown), 0's in the board mean empty squares.
    Move pos is a tuple holding [row,col], zero indexed such that valid entries are [0,board_size-1]
"""

def get_directions():
    """
    Get all directions (8 directions: up, down, left, right, and diagonals)

    Returns
    -------
    list of tuple
        List of direction vectors
    """
    return [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

def count_capture(chess_board, move_pos, player):
    """
    Check how many opponent's discs are captured.

    Returns
    -------
    int
        The number of stones that will be captured making this move, including all directions.
        Zero indicates any form of invalid move.
    """
    r, c = move_pos
    if chess_board[r, c] != 0:
        return 0
    
    captured = 0

    # Check if move captures any opponent discs in any direction
    for dir in get_directions():
        captured = captured + count_capture_dir(chess_board,move_pos, player, dir)

    return captured

def count_capture_dir(chess_board, move_pos, player, direction):
    """
    Check if placing a disc at move_pos captures any discs in the specified direction.

    Returns
    -------
    int
        Number of stones captured in this direction
    """
    r, c = move_pos
    dx, dy = direction
    r += dx
    c += dy
    captured = 0
    board_size = chess_board.shape[0]

    while 0 <= r < board_size and 0 <= c < board_size:
        if chess_board[r, c] == 0:
            return 0
        if chess_board[r, c] == player:
            return captured
        captured = captured + 1
        r += dx
        c += dy

    return 0


def execute_move(chess_board, move_pos, player):
    """
    Play the move specified by altering the chess_board.
    Note that chess_board is a pass-by-reference in/output parameter.
    Consider copy.deepcopy() of the chess_board if you want to consider numerous possibilities.
    """
    r, c = move_pos
    chess_board[r, c] = player

    # Flip opponent's discs in all directions where captures occur
    for direction in get_directions():
        flip_discs(chess_board,move_pos, player, direction)

def flip_discs(chess_board, move_pos, player, direction):
    
    if count_capture_dir(chess_board,move_pos, player, direction) == 0:
        return
    
    r, c = move_pos
    dx, dy = direction
    r += dx
    c += dy

    while chess_board[r, c] != player:
        chess_board[r, c] = player
        r += dx
        c += dy

def check_endgame(chess_board,player,opponent):
    """
    Check if the game ends and compute the final score. 
    
    Note that the game may end when a) the board is full or 
    b) when it's not full yet but both players are unable to make a valid move.
    One reason for b) occurring is when one player has no stones left. In human
    play this is sometimes scored as the max possible win (e.g. 64-0), but 
    we do not implement this scoring here and simply count the stones.

    Returns
    -------
    is_endgame : bool
        Whether the game ends.
    player_1_score : int
        The score of player 1.
    player_2_score : int
        The score of player 2.
    """

    is_endgame = False

    valid_moves = get_valid_moves(chess_board,player)
    if not valid_moves:
        opponent_valid_moves = get_valid_moves(chess_board,opponent)
        if not opponent_valid_moves:
            is_endgame = True  # When no-one can play, the game is over, score is current piece count

    p0_score = np.sum(chess_board == 1)
    p1_score = np.sum(chess_board == 2)
    return is_endgame, p0_score, p1_score

def get_valid_moves(chess_board,player):
    """
    Get all valid moves given the chess board and player.

    Returns

    -------
    valid_moves : [(tuple)]

    """

    board_size = chess_board.shape[0]
    valid_moves = []
    for r in range(board_size):
        for c in range(board_size):
            if count_capture(chess_board,(r, c), player) > 0:
                valid_moves.append((r, c))

    return valid_moves

def random_move(chess_board, player):
    """
    random move from the list of valid moves.

    Returns

    ------
    (tuple)


    """

    valid_moves = get_valid_moves(chess_board,player)

    if len(valid_moves) == 0:
        # If no valid moves are available, return None
        #print(f"No valid moves left for player {player}.")
        return None
    
    return valid_moves[np.random.randint(len(valid_moves))]
