import pygame
import cfg
from modules import *

def main():
    pygame.init()
    screen = pygame.display.set_mode(cfg.SCREENSIZE)
    pygame.display.set_caption("Damas Inglesas")
    board = Board(8)
    game = choose_game(screen,cfg)
    print(game)
    # game_play_human(screen,board)
      
    
def game_play_human_vs_ai(screen,board):
    (my_color, opponent_color) = tools.choose_color(screen,cfg)
    turn = my_color if my_color == 'red' else opponent_color
    initialize(board,my_color)

def game_play_human(screen,board):
    (my_color, opponent_color) = ("red","white")
    turn = my_color if my_color == 'red' else opponent_color
    initialize(board,my_color)
    piece_selected = None
    moves = []
    piece_count = None
    move_origin = None
    pre_moves = []
    jumps = []
    while not is_game_finished(board,my_color):
        jumps = find_jump(board,my_color,turn)
        if len(jumps)>0 and moves==[]: 
            for jump in jumps:    
                move_origin,moves_jumps = jump
                for mv in moves_jumps:
                    moves.append(mv)
                    pre_moves.append([move_origin,mv])
            move_origin = None
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                x_pos = x//board.get_cell_size()
                y_pos = (y-20)//(board.get_cell_size()) 
                row, col = y_pos, x_pos
                if not board.is_free(row,col) and len(jumps)==0:
                    piece_selected = board.get(row,col)
                    if piece_selected.color() == turn:
                        move_origin = (row,col)
                        moves = get_moves(board,row,col,my_color)
                    else:
                        piece_selected = None
                if piece_selected and board.is_free(row,col):
                    move = [move_origin,(row,col)]
                    if apply_move(board,move,my_color):  
                        piece_selected = None
                        move_origin = None
                        moves = []
                        turn = "red" if turn == "white" else "white"
                    elif apply_capture(board,move,my_color):
                        piece_selected = None
                        move_origin = None
                        moves = []
                        turn = "red" if turn == "white" else "white" 
                if len(jumps)>0:
                    if (row,col) in moves:
                        for move_jump in pre_moves:
                            if move_jump[1] == (row,col):
                               move = move_jump
                        if apply_capture(board,move,my_color):
                           moves = []
                           pre_moves = []
                           jumps = get_jumps(board,row,col,my_color)
                           if len(jumps)>0:
                               break
                           turn = "red" if turn == "white" else "white" 
                           
                    
        board.draw(screen)
        piece_count = count_pieces(board)   
        board.display(screen,cfg,turn,piece_count)
        if moves: board.draw_moves(moves,screen)
        pygame.display.update()
    endInterface(screen,get_winner(board),cfg)      
         


if __name__ == '__main__':
    main()