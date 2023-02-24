class Piece(object):

    def __init__(self, color = 'red', is_king = False):
        if color.isalpha():
            color = color.lower()
            if color == 'red' or color == 'white':
                self.last_move = None
                self._color = color
                self._is_king  = is_king
            else:
                raise ValueError("A piece must be \'red\' or \'white\'.")
        else:
            raise ValueError("A piece must be \'red\' or \'white\'.")
        
    def color(self):
        return self._color
        
    def is_red(self):
        return self._color == 'red'
    
    def is_white(self):
        return self._color == 'white'
    
    def is_king(self):
        return self._is_king
    
    def set_last_move(self,last_move):
        self.last_move = last_move
        
    def last_move(self):
        return self.last_move
        
    def turn_king(self):
        self._is_king = True
        
    def turn_pawn(self):
        self.is_king = False
        