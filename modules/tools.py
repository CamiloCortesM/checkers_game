import copy
import pygame

def get_moves(board, row, col,my_color, is_sorted = False):
    down, up = [(+1, -1), (+1, +1)], [(-1, -1), (-1, +1)]
    length = board.get_length()
    piece = board.get(row, col)
    if piece:
        bottom = [(row + x, col + y) for (x, y) in down if (0 <= (row + x) < length) and (0 <= (col + y) < length) and board.is_free(row + x, col + y)]
        top = [(row + x, col + y) for (x, y) in up if (0 <= (row + x) < length) and (0 <= (col + y) < length) and board.is_free(row + x, col + y)]
        
        if my_color == "white":
            return (sorted(bottom + top) if piece.is_king() else (sorted(bottom) if piece.is_red() else sorted(top))) \
                    if is_sorted else (bottom + top if piece.is_king() else \
                                       (bottom if piece.is_red() else top))
        else:
            return (sorted(bottom + top) if piece.is_king() else (sorted(bottom) if piece.is_white() else sorted(top))) \
                    if is_sorted else (bottom + top if piece.is_king() else \
                                       (bottom if piece.is_white() else top))
    return []

def get_jumps(board, row, col,my_color, is_sorted = False):
    down, up = [(+1, -1), (+1, +1)], [(-1, -1), (-1, +1)]
    length = board.get_length()
    piece = board.get(row, col)
    if piece:
        bottom = \
            [(row + 2 * x, col + 2 * y) for (x, y) in down \
             if (0 <= (row + 2 * x) < length) \
                 and (0 <= (col + 2 * y) < length) \
                 and board.is_free(row + 2 * x, col + 2 * y) \
                 and (not board.is_free(row + x, col + y)) \
                 and (board.get(row + x, col + y).color() != piece.color())]
        top = \
            [(row + 2 * x, col + 2 * y) for (x, y) in up \
             if (0 <= (row + 2 * x) < length) \
                 and (0 <= (col + 2 * y) < length) \
                 and board.is_free(row + 2 * x, col + 2 * y) \
                 and (not board.is_free(row + x, col + y)) \
                 and (board.get(row + x, col + y).color() != piece.color())]
        if my_color =="white":
            return (sorted(bottom + top) if piece.is_king() else \
                (sorted(bottom) if piece.is_red() else sorted(top))) \
                    if is_sorted else (bottom + top if piece.is_king() else \
                                       (bottom if piece.is_red() else top))
        else:
            return (sorted(bottom + top) if piece.is_king() else \
                (sorted(bottom) if piece.is_white() else sorted(top))) \
                    if is_sorted else (bottom + top if piece.is_king() else \
                                       (bottom if piece.is_white() else top))
    return []

def search_path(board, row, col, path, paths,my_color, is_sorted = False):

    path.append((row, col))
    jumps = get_jumps(board, row, col,my_color, is_sorted)
    if not jumps:
        paths.append(path)
    else:
        for position in jumps:
            (row_to, col_to) = (position)
            piece = copy.copy(board.get(row, col))
            board.remove(row, col)
            board.place(row_to, col_to, piece)
            if (piece.color() == 'red' \
                and row_to == board.get_length() - 1) \
                    or (piece.color() == 'white' \
                        and row_to == 0) \
                            and (not piece.is_king()):
                                piece.turn_king()
            row_mid = row + 1 if row_to > row else row - 1
            col_mid = col + 1 if col_to > col else col - 1
            capture = board.get(row_mid, col_mid)
            board.remove(row_mid, col_mid)
            search_path(board, row_to, col_to, copy.copy(path), paths,my_color)
            board.place(row_mid, col_mid, capture)
            board.remove(row_to, col_to)
            board.place(row, col, piece)
            
def get_captures(board, row, col,mycolor, is_sorted = False):
    paths = []
    board_ = copy.copy(board)
    search_path(board_, row, col, [], paths,mycolor, is_sorted)
    if len(paths) == 1 and len(paths[0]) == 1:
        paths = []
    return paths

def choose_game(screen,cfg):
    screen.fill((255,255,255))
    font_title = pygame.font.Font(cfg.FONTPATH, 45)
    font = pygame.font.Font(cfg.FONTPATH, 25)
    tfont = font_title.render("Choose game mode:",True,(255,0,0))
    cfont1 = font.render("Enter 1 for play human vs AI",True,(0,0,0))
    cfont2 = font.render("Enter 2 for play human vs human",True,(0,0,0))
    cfont3 = font.render("Enter 3 for play AI vs AI",True,(0,0,0))
    cfont4 = font.render("Enter 4 for play ONLINE",True,(0,0,0))
    
    trect = tfont.get_rect()
    crect1 = cfont1.get_rect()
    crect2 = cfont2.get_rect()
    crect3 = cfont3.get_rect()
    crect4 = cfont4.get_rect()
    
    trect.midtop = (cfg.SCREENSIZE[0]/2,cfg.SCREENSIZE[1]/5)
    crect1.midtop = (cfg.SCREENSIZE[0]/2,cfg.SCREENSIZE[1]/2.5)
    crect2.midtop = (cfg.SCREENSIZE[0]/2,cfg.SCREENSIZE[1]/2)
    crect3.midtop = (cfg.SCREENSIZE[0]/2,cfg.SCREENSIZE[1]/1.66)
    crect4.midtop = (cfg.SCREENSIZE[0]/2,cfg.SCREENSIZE[1]/1.42)
    
    screen.blit(tfont,trect)
    screen.blit(cfont1,crect1)
    screen.blit(cfont2,crect2)
    screen.blit(cfont3,crect3)
    screen.blit(cfont4,crect4)
    
    while True:  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1
                elif event.key == pygame.K_2:
                    return 2           
                elif event.key == pygame.K_3:
                    return 3           
                elif event.key == pygame.K_4:
                    return 4           
        pygame.display.update()
    
    
    
def choose_color(screen,cfg):
    screen.fill((255,255,255))
    font_title = pygame.font.Font(cfg.FONTPATH, 45)
    font = pygame.font.Font(cfg.FONTPATH, 25)
    tfont = font_title.render("Choose a color:",True,(255,0,0))
    cfont1 = font.render("Enter w for play with white",True,(0,0,0))
    cfont2 = font.render("Enter r for play with red",True,(0,0,0))
    
    trect = tfont.get_rect()
    crect1 = cfont1.get_rect()
    crect2 = cfont2.get_rect()
    trect.midtop = (cfg.SCREENSIZE[0]/2,cfg.SCREENSIZE[1]/3.5)
    crect1.midtop = (cfg.SCREENSIZE[0]/2,cfg.SCREENSIZE[1]/2)
    crect2.midtop = (cfg.SCREENSIZE[0]/2,cfg.SCREENSIZE[1]/1.7)
    
    screen.blit(tfont,trect)
    screen.blit(cfont1,crect1)
    screen.blit(cfont2,crect2)
    
    while True:  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    return ("white","red")
                elif event.key == pygame.K_r:
                    return ("red","white")           
        pygame.display.update()

def endInterface (screen,winner,cfg):
    screen.fill((255,255,255))
    font_title = pygame.font.Font(cfg.FONTPATH, 45)
    font = pygame.font.Font(cfg.FONTPATH, 25)
    title = font_title.render("The game is over",True,(255,0,0))
    cfont = font.render("the winner is: {}".format(winner),True,(0,0,0))
    trect = title.get_rect()
    crect = cfont.get_rect()
    trect.midtop = (cfg.SCREENSIZE[0]/2,cfg.SCREENSIZE[1]/3.5)
    crect.midtop = (cfg.SCREENSIZE[0]/2,cfg.SCREENSIZE[1]/1.8)
    
    screen.blit(title,trect)
    screen.blit(cfont,crect)
    
    while True:  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()         
        pygame.display.update()

    