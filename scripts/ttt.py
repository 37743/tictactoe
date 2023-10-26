# Yousef (Ibrahim) Gomaa - ID: 320210207
# Egypt-Japan University of Science and Technology
# Artificial Intelligence and Data Science Department
# Tic-Tac-Toe Board Code
# ---
import numpy as np
import scripts.datastructures.stack as stack
import collections

AI_CELL = 0
BOARD_X = 3
BOARD_Y = 3
BOARD_DIMENSIONS = (BOARD_X, BOARD_Y)
# Current state of the game.
state = {"DRAW" : 0,
        "X WON" : 1,
        "O WON" : 2,
        "ONGOING" : 3}

# X/O Symbols to populate the matrix with.
MARK_EMPTY = 0
MARK_X = 1
MARK_O = 2
# Current turn, X always starts first.
TURN_PVP = 1
TURN_PVA = 1

empty_board = np.zeros(BOARD_DIMENSIONS, dtype = int).flatten()
# print(empty_board)

def pvp_mod(reset=False):
    global TURN_PVP
    if (reset):
        TURN_PVP = 1
    else:
        TURN_PVP = TURN_PVP + 1


def pva_mod(reset=False):
    global TURN_PVA
    if (reset):
        TURN_PVA = 1
    else:
        TURN_PVA = TURN_PVA + 1
# ----------------------------------
# RANDOM IMPLEMENTATION
# def optimal_move(board, cturn, depth=0):
#     ''' Find the best possible move for the A.I.
#         TODO: FIX THIS PART ~~> TEMPORARILY RANDOM.'''
#     bestmove = np.random.choice(board.get_valid_indices(), 1)[0]
#     if (depth<10):
#         for move in board.get_valid_indices():
#             # Test if A.I. move is best
#             depth = depth+1
#             bestmove = optimal_move(board, cturn, depth)
#             player = MARK_O if (cturn%2 == 0) else MARK_X
#             # Try A.I. move
#             board.board[move] = player
#             # Change turn to IRL player
#             cturn = cturn+1
#             # Revert A.I. move
#             tempresult = board.get_result()
#             board.board[move] = 0
#             # Check if A.I. player wins on this move.
#             if (player==MARK_O and (tempresult==state['O WON']) or\
#                      (player==MARK_X and (tempresult==state['X WON']))):
#                 bestmove = move
#                 break
#     return bestmove
# ----------------------------------
# DEPTH FIRST SEARCH:
def dfs_move(boards, cboard, cturn, best_move, pbest_move, depth=0):
    if (depth<10):
        for mv in cboard.get_valid_indices():
            depth = depth + 1
            player = MARK_O if (cturn%2 ==0) else MARK_X
            cboard.board[mv] = player
            boards.push(cboard, mv)
            cturn = cturn+1
            temp_result = boards.top().get_result()
            pbest_move = dfs_move(boards, boards.top(), cturn, best_move, pbest_move)
            cboard.board[mv] = 0
            if (player==MARK_O and (temp_result==state['O WON']) or\
                (player==MARK_X and (temp_result==state['X WON']))):
                return mv
        while not (boards.is_empty()):
            pbest_move = best_move
            best_move = boards.pop()
    return pbest_move

def optimal_move(board, cturn):
    boards = stack.Stack()
    boards.push(board)
    best_move = dfs_move(boards, boards.top(), cturn, best_move=0, pbest_move=0)
    return best_move
# ----------------------------------
# BREADTH FIRST SEARCH:
# def bfs_move(boards):
#     pass

# def optimal_move(board, cturn):
#     boards = queue.Queue()
#     boards.push(board)
#     best_move = bfs_move(boards, boards.top(), cturn, best_move=0, pbest_move=0)
#     return best_move
# ----------------------------------
class TTT():
    ''' Class that contains Tic-Tac-Toe's game logic'''
    def __init__(self, new_board=None):
        if new_board is None:
            self.board = np.copy(empty_board)
        else:
            self.board = new_board
        # Transform from 1 dimensional to 2 dimensional.
        self.board_2d = self.board.reshape(BOARD_DIMENSIONS)
        print(self.board_2d)
    
    def __str__(self):
        return str(self.board)

    def get_result(self):
        ''' Get current state of the match'''
        for sym in[MARK_X,MARK_O]:
            if self.check_rows_cols_diags(sym):
                return sym
        if MARK_EMPTY not in self.board_2d:
            return state['DRAW']
        return state['ONGOING']
    
    def get_valid_indices(self):
        ''' Get all valid indexes that could potentially be marked'''
        return ([i for i in range(self.board.size) if self.board[i] == MARK_EMPTY])
    
    def is_over(self):
        ''' Returns True if game has ended'''
        return self.get_result() != state['ONGOING']
    
    def check_rows_cols_diags(self, sym):
        ''' Check if there exists a winning condition for symbol \'sym\' '''
        # Rotate to get columns.
        temp_board = np.rot90(np.copy(self.board_2d))
        return self.check_rows(self.board_2d, sym) or\
            self.check_rows(temp_board, sym) or\
            self.check_diags(self.board_2d, sym)

    def check_rows(self, board, sym):
        ''' Check rows for a winning combination'''
        test = collections.Counter([sym,sym,sym])
        for i in board:
            if collections.Counter(i) == test:
                return True
        return False
        
    def check_diags(self, board, sym):
        ''' Check diagonals for a winning combination'''
        test = collections.Counter([sym,sym,sym])
        if collections.Counter(board.diagonal()) == test\
        or collections.Counter(np.fliplr(board).diagonal()) == test:
            return True
        return False
    
    def get_player(self, pvp=True):
        ''' Returns which player's turn'''
        # X always starts first
        turn = TURN_PVP if pvp else TURN_PVA
        return MARK_X if (turn%2 != 0) else MARK_O
    
    def get_turn(self, pvp=True):
        ''' Returns count of turns'''
        return TURN_PVP if pvp else TURN_PVA
    
    def play(self, move, pvp=True):
        ''' Marks the board with given index if it is a valid move'''
        temp_board = self.board
        if move not in self.get_valid_indices():
            return TTT(temp_board)
        temp_board[move] = self.get_player()
        pvp_mod() if pvp else pva_mod()
        return TTT(temp_board)
    
    def play_ai(self):
        ''' A.I. plays generates moves recursively and picks the best option'''
        aimove = optimal_move(self, self.get_turn(pvp=False))
        global AI_CELL
        AI_CELL = aimove
        # It's O but its so I can change this later to reverse play order.
        # vvv
        self.board[aimove] = self.get_player(pvp=False)
        # Turn gets incremented in the IRL player's code.
        pva_mod()
        return TTT(self.board)
            
    def get_ai_cell(self):
        global AI_CELL
        return AI_CELL

    def reset(self, pvp=True):
        ''' Reset to a blank board'''
        self.board = np.copy(empty_board)
        self.board_2d = self.board.reshape(BOARD_DIMENSIONS)
        if (pvp):
            pvp_mod(reset=True)
        else:
            pva_mod(reset=True)
        return