import pygame
import cfg
from modules import *

def initGame():
    pygame.init()
    
    screen = pygame.display.set_mode(cfg.SCREENSIZE)
    pygame.display.set_caption("Damas Inglesas")




if __name__ == '__main__':
    initGame()