import pygame
import cfg
from modules import *

def main():
    pygame.init()
    screen = pygame.display.set_mode(cfg.SCREENSIZE)
    pygame.display.set_caption("Damas Inglesas")
    (my_color, opponent_color) = tools.choose_color(screen,cfg)
    board = Board(8)
    turn = my_color if my_color == 'red' else opponent_color
    initialize(board,my_color)
    piece_selected = None
    moves = None
    piece_count = None
    
    while not is_game_finished(board,my_color):
        
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                x_pos = x//board.get_cell_size()
                y_pos = (y-20)//(board.get_cell_size()) 
                row, col = y_pos, x_pos
                if not board.is_free(row,col):
                    piece_selected = board.get(row,col)
                    if piece_selected.color() == turn:
                        moves = get_moves(board,row,col,my_color)
                        
        board.draw(screen)
        piece_count = count_pieces(board)   
        board.display(screen,cfg,turn,piece_count)
        if moves: board.draw_moves(moves,screen)
        pygame.display.update()
                


if __name__ == '__main__':
    main()