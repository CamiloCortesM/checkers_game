class Piece(object):

    def __init__(self, color = 'black', is_king = False):
        if color.isalpha():
            color = color.lower()
            if color == 'black' or color == 'white':
                self._color = color
                self._is_king  = is_king
            else:
                raise ValueError("A piece must be \'black\' or \'white\'.")
        else:
            raise ValueError("A piece must be \'black\' or \'white\'.")
        
    def color(self):
        return self._color
        
    def is_black(self):
        return self._color == 'black'
    
    def is_white(self):
        return self._color == 'white'
    
    def is_king(self):
        return self._is_king
    
        
    def turn_king(self):
        self._is_king = True
        
    def turn_pawn(self):
        self.is_king = False
        