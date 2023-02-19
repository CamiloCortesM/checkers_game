import pygame
import cfg
from modules import *
import ai as ai

def choose_game(screen,cfg):
    board = Board(8)
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
                    game_play_human_vs_ai(screen,board)
                elif event.key == pygame.K_2:
                    game_play_human(screen,board)         
                elif event.key == pygame.K_3:
                    game_play_ai_vs_ai(screen,board)           
                elif event.key == pygame.K_4:
                    game_play_socket(screen,board)          
        pygame.display.update()

def main():
    pygame.init()
    screen = pygame.display.set_mode(cfg.SCREENSIZE)
    pygame.display.set_caption("Damas Inglesas")
    choose_game(screen,cfg)
   
def game_play_socket(screen,board):
    print("coming soon")  
    
def game_play_ai_vs_ai(screen,board):
    my_color,opponent_color = 'red','white'
    initialize(board)
    
def game_play_human_vs_ai(screen,board):
    (my_color, opponent_color) = tools.choose_color(screen,cfg)
    turn = my_color if my_color == 'red' else opponent_color
    initialize(board)
    piece_selected = None
    moves = []
    piece_count = None
    move_origin = None
    pre_moves = []
    jumps = []
    while not is_game_finished(board):
        
        if turn == opponent_color: # if Turn of machine
                move = ai.get_next_move(board, turn)
                if type(move) == list: # move is a move
                    apply_capture(board, move)
                if type(move) == tuple: # move is a jump
                    apply_move(board, move)
                print("\t{:s} played {:s}.".format(turn, str(move)))
                turn = my_color # change the turn
                continue
            
        jumps = find_jump(board,turn)
        
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
                        moves = get_moves(board,row,col)
                    else:
                        piece_selected = None
                if piece_selected and board.is_free(row,col):
                    move = [move_origin,(row,col)]
                    if apply_move(board,move):  
                        piece_selected = None
                        move_origin = None
                        moves = []
                        turn = "red" if turn == "white" else "white"
                    elif apply_capture(board,move):
                        piece_selected = None
                        move_origin = None
                        moves = []
                        turn = "red" if turn == "white" else "white" 
                if len(jumps)>0:
                    if (row,col) in moves:
                        for move_jump in pre_moves:
                            if move_jump[1] == (row,col):
                               move = move_jump
                        if apply_capture(board,move):
                           moves = []
                           pre_moves = []
                           jumps = get_jumps(board,row,col)
                           if len(jumps)>0:
                               break
                           turn = "red" if turn == "white" else "white"       
        board.draw(screen)
        piece_count = count_pieces(board)   
        board.display(screen,cfg,turn,piece_count)
        if moves: board.draw_moves(moves,screen)
        pygame.display.update()
    endInterface(screen,get_winner(board),cfg)     

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