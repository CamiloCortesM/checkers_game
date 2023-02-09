import pygame

class Board(object):
    def __init__(self, length = 8):
        self._length = length 
        self._cell = [[None for c in range(self._length)] for r in range(self._length)]
        self.cell_size = 60
        
    def draw(self, screen):
        for row in range(self._length):
            for col in range(self._length):
                color = (255, 253, 208) if (row + col) % 2 == 0 else (128, 70, 27)
                pygame.draw.rect(screen, color, [(self.cell_size) * col,
                                                 (self.cell_size) * row+20,
                                                 self.cell_size,
                                                 self.cell_size])
                piece = self._cell[row][col]
                if piece is not None:
                    if piece.is_red():
                        color = (255, 0, 0)
                    elif piece.is_white():
                        color = (255, 255,255)
                    pygame.draw.circle(screen, color, [(self.cell_size) * col + self.cell_size // 2,
                                                       (self.cell_size) * row+20 + self.cell_size // 2],
                                                       self.cell_size // 3) 
                    if piece.is_king():
                        # dibujar una corona
                        x = ((self.cell_size) * col + self.cell_size // 2)-1
                        y = ((self.cell_size) * row+20 + self.cell_size // 2)-6
                        size = self.cell_size // 3
                        crown_points = [(x, y - size), (x + size / 2, y - size / 2), (x + size, y - size),
                        (x + size, y), (x + size / 2, y + size / 2), (x, y),
                        (x - size / 2, y + size / 2), (x - size, y), (x - size, y - size),
                        (x - size / 2, y - size / 2)]
                        pygame.draw.polygon(screen, (255, 255, 0), crown_points, 0)                  
    def draw_moves(self, moves,screen):
        for move in moves:
            pygame.draw.circle(screen, (0,255,0), [(self.cell_size) * move[1] + self.cell_size // 2,
                                                       (self.cell_size) * move[0]+20 + self.cell_size // 2],
                                                       self.cell_size // 4)  
    def get_length(self):
        return self._length
    
    def get_cells(self):
        return self._cell
    
    def get_cell_size(self):
        return self.cell_size
    
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
    
    def display(self, screen,cfg,turn, count = None):
        font = pygame.font.Font(cfg.FONTPATH, 20)
        text_string = "turn to play for: {}".format(turn)
        text_turn = font.render(text_string, True, (255, 255, 255))
        trect = text_turn.get_rect()
        trect.topright = (cfg.SCREENSIZE[0],-2)
        screen.blit(text_turn,trect)
        if count is not None:
            text = font.render("Red: {:d}, White: {:d}".format(count[0], count[1]), True, (255, 255, 255))
            screen.blit(text, [0, -2])
