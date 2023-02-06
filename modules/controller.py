from piece import Piece
from tools import get_moves,get_captures

def initialize(board):
    row = col = board.get_length()
    initrows = (row // 2) - 1
    for r in range(row - 1, row - (initrows + 1), -1):
        for c in range(0 if r % 2 == 1 else 1, col, 2):
            board.place(r, c, Piece('white'))
    for r in range(0, initrows):
        for c in range(0 if r % 2 == 1 else 1, col, 2):
            board.place(r, c, Piece())
            
def count_pieces(board):
    row = col = board.get_length()
    black, white = 0, 0
    for r in range(row):
        for c in range(col):
            piece = board.get(r, c)
            if piece:
                if piece.is_black():
                    black += 1
                if piece.is_white():
                    white += 1
    return (black, white)

def get_all_moves(board, color, is_sorted = False):
    row = col = board.get_length()
    final_list = []
    for r in range(row):
        for c in range(col):
            piece = board.get(r, c)
            if piece:
                if piece.color() == color:
                    path_list = get_moves(board, r, c, is_sorted)
                    path_start = (r, c)
                    for path in path_list:
                        final_list.append((path_start, path))
    
    if is_sorted == True:
        final_list.sort()
    return final_list

def get_all_captures(board, color, is_sorted = False):
    row = col = board.get_length()
    final_list = []
    for r in range(row):
        for c in range(col):
            piece = board.get(r, c)
            if piece:
                if piece.color() == color:
                    path_list = get_captures(board, r, c, is_sorted)
                    for path in path_list:
                        final_list.append(path) 
    return sorted(final_list, key = lambda x: (-len(x), x[0]))\
    if is_sorted else final_list
    
def apply_move(board, move):
    row,col = (move[0])
    row_end,col_end = (move[1])
    path_list = get_moves(board, row, col, is_sorted = False)
    
    if move[1] in path_list:
        piece = board.get(row, col)
        if piece.is_black() and row_end == board.get_length()-1 \
        or piece.is_white() and row_end == 0:
            piece.turn_king()
        board.remove(row, col)
        board.place(row_end, col_end, piece)
    else:
        raise RuntimeError("Invalid move, please type" \
                         + " \'hints\' to get suggestions.")