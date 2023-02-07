import pygame
import cfg
from modules import *

def main():
    pygame.init()
    
    screen = pygame.display.set_mode(cfg.SCREENSIZE)
    pygame.display.set_caption("Damas Inglesas")
    (my_color, opponent_color) = tools.choose_color(screen,cfg)
    print(my_color,opponent_color)
    board = Board(8)
    turn = my_color if my_color == 'black' else opponent_color
    initialize(board)
    while not is_game_finished(board):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        board.draw(screen)
                


if __name__ == '__main__':
    main()