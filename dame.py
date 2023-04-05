import numpy as np
import itertools as it

class Dame:
    '''
        The main managing class of the game dame (or checkers, by its actual boring name).
    '''

    def __init__(self):
        '''
            Makes a board in a starting state.
        '''

        self.board = np.zeros([8,8], dtype=int)
        self.white_pieces = []
        self.black_pieces = []

        # Place White pieces
        offs = 1
        for y in range(5,8):
            offs = 1-offs
            for i in range(4):
                x = offs + 2*i
                self.board[x,y] = 1
                self.white_pieces.append((x,y))

        # Place Black pieces
        offs = 0
        for y in range(3):
            offs = 1-offs
            for i in range(4):
                x = offs + 2*i
                self.board[x,y] = 2
                self.black_pieces.append((x,y))

        # Used when the drawing board
        self.draw_as = { 
            0: '_', # Empty squares
            1: 'W', # White pieces 
            2: 'B', # Black pieces
        }

        # Used when moving pieces
        self.char_to_col = {
            'a':0,
            'b':1,
            'c':2,
            'd':3,
            'e':4,
            'f':5,
            'g':6,
            'h':7
        }

    def print_board(self):
        '''
            Draws the board to the console
        '''

        print()

        for y in range(8):
            print(f' {8-y}  ', end='')
            print(*[self.draw_as.get(self.board[x,y], '?') for x in range(8)], sep='|')

        print()
        print("    a b c d e f g h")
        print()

    def is_move_valid(self, fro, to, for_white):
        '''
            Examines the validity of a player moving from "fro" to "to".

            Player is white iff for_white is True
            fro and to are strings in the format of "{letter}{number}" as read from the board
            e.g.: "a8" for the upper-left corner.
        '''

        # Horrible input check
        if len(fro) != 2 or len(to) != 2: 
            print("Something went terribly wrong here.")
            return False
        

        # Making arguments usable
        xf,yf = fro.split()
        xf = self.char_to_col.get(xf, -1) # useful column number
        yf -= 1 # indexed from 0

        xto,yto = to.split()
        xto = self.char_to_col.get(xto, -1) # useful column number
        yto -= 1 # indexed from 0

        # Bad input check
        for coord in [xf,yf,xto,yto]:
            if coord not in range(8):
                print("I don't like that.")
                return False
            
        return True




if __name__ == "__main__":

    dame = Dame()
    dame.print_board()
    print(dame.is_move_valid('a1','b2', for_white=True))