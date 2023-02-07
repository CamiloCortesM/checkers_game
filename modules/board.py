import pygame

class Board(object):
    def __init__(self, length = 8):
        self._length = length 
        self._cell = [[None for c in range(self._length)] for r in range(self._length)]
        self.cell_size = 60
        
    def draw(self, screen):
        screen.fill((0,0,0))
        for row in range(self._length):
            for col in range(self._length):
                color = (255, 253, 208) if (row + col) % 2 == 0 else (128, 70, 27)
                pygame.draw.rect(screen, color, [(self.cell_size) * col,
                                                 (self.cell_size) * row+20,
                                                 self.cell_size,
                                                 self.cell_size])
                piece = self._cell[row][col]
                if piece is not None:
                    if piece.is_black():
                        color = (255, 0, 0)
                    elif piece.is_white():
                        color = (255, 255,255)
                    pygame.draw.circle(screen, color, [(self.cell_size) * col + self.cell_size // 2,
                                                       (self.cell_size) * row+20 + self.cell_size // 2],
                                                       self.cell_size // 3)
        pygame.display.update()
    def get_length(self):
        return self._length
    
    def get_cells(self):
        return self._cell
    
    def is_free(self, row, col):
        return self._cell[row][col] is None
        
    def place(self, row, col, piece):
        self._cell[row][col] = piece
        
    def get(self, row, col):
        return self._cell[row][col]
    
    def remove(self, row, col):
        self._cell[row][col] = None
        
    def is_empty(self):
        for r in range(self._length):
            for c in range(self._length):
                if not self.is_free(r,c):
                    return False
        return True
    
    def is_full(self):
        for r in range(self._length):
            for c in range(self._length):
                if self.is_free(r, c):
                    return False
        return True
    
    def display(self, screen,cfg, count = None):
        self.draw(screen)
        if count is not None:
            font = pygame.font.Font(cfg.FONTPATH, 36)
            text = font.render("Black: {:d}, White: {:d}".format(count[0], count[1]), True, (255, 255, 255))
            screen.blit(text, [10, 10])
