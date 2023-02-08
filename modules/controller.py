from .piece import Piece
from .tools import get_moves,get_captures,get_jumps

def initialize(board,mycolor):
    row = col = board.get_length()
    initrows = (row // 2) - 1
    for r in range(row - 1, row - (initrows + 1), -1):
        for c in range(0 if r % 2 == 1 else 1, col, 2):
            board.place(r, c, Piece(mycolor))
    for r in range(0, initrows):
        for c in range(0 if r % 2 == 1 else 1, col, 2):
            board.place(r, c, Piece('white' if mycolor=='red' else 'red'))
            
def count_pieces(board):
    row = col = board.get_length()
    red, white = 0, 0
    for r in range(row):
        for c in range(col):
            piece = board.get(r, c)
            if piece:
                if piece.is_red():
                    red += 1
                if piece.is_white():
                    white += 1
    return (red, white)

def get_all_moves(board, color,mycolor, is_sorted = False,):
    row = col = board.get_length()
    final_list = []
    for r in range(row):
        for c in range(col):
            piece = board.get(r, c)
            if piece:
                if piece.color() == color:
                    path_list = get_moves(board, r, c, is_sorted,mycolor)
                    path_start = (r, c)
                    for path in path_list:
                        final_list.append((path_start, path))
    
    if is_sorted == True:
        final_list.sort()
    return final_list

def get_all_captures(board, color,mycolor, is_sorted = False):
    row = col = board.get_length()
    final_list = []
    for r in range(row):
        for c in range(col):
            piece = board.get(r, c)
            if piece:
                if piece.color() == color:
                    path_list = get_captures(board, r, c,mycolor, is_sorted)
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
        if piece.is_red() and row_end == board.get_length()-1 \
        or piece.is_white() and row_end == 0:
            piece.turn_king()
        board.remove(row, col)
        board.place(row_end, col_end, piece)
    else:
        raise RuntimeError("Invalid move, please type" \
                         + " \'hints\' to get suggestions.")
        
def apply_capture(board, capture_path):
    counter = 0
    while counter < len(capture_path)-1:
        path = [capture_path[counter], capture_path[counter + 1]]
        counter += 1
        row,col = (path[0])
        row_end,col_end = (path[1])
        path_list = get_jumps(board, row, col, is_sorted = False)
        
        if path[1] in path_list:
            piece = board.get(row, col)
            if piece.is_red() and row_end == board.get_length()-1 \
            or piece.is_white() and row_end == 0:
                piece.turn_king()
            board.remove(row, col)
            row_eat, col_eat = max(row, row_end)-1, max(col, col_end)-1
            board.remove(row_eat, col_eat)
            board.place(row_end, col_end, piece)
        else:
            raise RuntimeError("Invalid jump/capture, please type" \
                             + " \'hints\' to get suggestions.")

def get_hints(board, color,mycolor, is_sorted = False):
    move = get_all_moves(board, color,mycolor, is_sorted)
    jump = get_all_captures(board, color,mycolor, is_sorted)
    if jump:
        return ([], jump)
    else:
        return (move, jump)

def get_winner(board, is_sorted = False):
    red_hint = get_hints(board, 'red', is_sorted)
    white_hint = get_hints(board, 'white', is_sorted)
    if red_hint != ([],[]) and white_hint == ([],[]):
        return 'red'
    elif red_hint == ([],[]) and white_hint != ([],[]):
        return 'white'
    else:
        red_king,white_king = 0,0
        red, white = 0,0
        row = col = board.get_length()
        for r in range(row):
            for c in range(col):
                piece = board.get(r, c)
                if piece:
                    if piece.is_red():
                        red += 1
                        if piece.is_king():
                            red_king += 1
                    else:
                        white += 1
                        if piece.is_king():
                            white_king += 1
        if white_king == 1 and red_king == 1 and white == 1 and red == 1:
            return 'draw'
        else:
            if white > red:
                return 'white'
            elif red > white:
                return 'red'
            else:
                return 'draw'

def is_game_finished(board,mycolor, is_sorted = False):
    red_hint = get_hints(board, 'red', is_sorted,mycolor)
    white_hint = get_hints(board, 'white', is_sorted,mycolor)
    if red_hint == ([],[]) or white_hint == ([],[]):
        return True
    else:
        return False