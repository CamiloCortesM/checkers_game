class Piece(object):

    def __init__(self, color = 'red', is_king = False):
        if color.isalpha():
            color = color.lower()
            if color == 'red' or color == 'white':
                self._last_move = None
                self._color = color
                self._is_king  = is_king
                self._letter = 'r' if color == 'red' else 'w'
            else:
                raise ValueError("A piece must be \'red\' or \'white\'.")
        else:
            raise ValueError("A piece must be \'red\' or \'white\'.")
        
    def letter(self):
        return self._letter
        
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
        return self._last_move
        
    def turn_king(self):
        self._is_king = True
        self._letter = self._letter.upper()
        
    def turn_pawn(self):
        self.is_king = False
        