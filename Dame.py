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

        self.draw_as = {
            0: '_', # Empty squares
            1: 'W', # White pieces 
            2: 'B', # Black pieces
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



if __name__ == "__main__":

    dame = Dame()
    dame.print_board()
    print("White pieces at", *dame.white_pieces, sep= " ")
    print("Black pieces at", *dame.black_pieces, sep= " ")