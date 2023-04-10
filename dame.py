import numpy as np

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

        # A convinience for printing
        self.name = {
            True: "White",
            False: "Black"
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

    def coords_to_index(self, coords):
        """
        Turns an on-board coordinates into the index of said coordinates in self.board
        e.g. if coords="a8" it returns (0,0)
        """

        # Horrible input check
        if len(coords) != 2:
            print("Something went terribly wrong here.")
            return (-1,-1)
        
        x, y = coords
        
        # Useful column number
        x = self.char_to_col.get(x, -1)

        # Turning game-accurate input code-accurate, also on the lookout for non-number input
        try:
            y = 8 - int(y)
        except:
            print("That makes no sense.")
            return(x,-1)
        
        return x, y
    
    def get_input(self, for_white):
        '''
            Keeps asking for input until you put in somthing that makes sense.
            Makes sense means two baord-read coordinates like "a4 f5"
        '''

        try_again = True
        while try_again: # Only escape loop if everything goes well
            try_again = False

            curr = input(f"Move for {self.name[for_white]}: ")

            if curr == "-1": # To quit debug without ctrl+c
                return -1

            curr = curr.split()
            if len(curr) != 2:
                try_again = True
                curr = ["i9","i9"]

            fro,to = curr

            # Making arguments usable
            xf, yf = self.coords_to_index(fro)
            xto, yto = self.coords_to_index(to)
            
            # Bad input check
            for idx in [xf, yf, xto, yto]:
                if idx not in range(8):
                    print("That makes no sense.")
                    try_again = True

        return (xf,yf), (xto,yto)

    def is_move_valid(self, fro, to, for_white):
        '''
            Examines the validity of a player moving from "fro" to "to".

            Player is white iff for_white is True
            fro and to are strings in the format of "{letter}{number}" as read from the board
            e.g.: "a8" for the upper-left corner.
        '''

        xf, yf = fro
        xto, yto = to
            
        # Do you have a piece there?
        your_pieces = [1] if for_white else [2]

        if self.board[xf,yf] not in your_pieces:
            print("You have no piece there, blindo.")
            return False

        # Possible Movements (just single-moves as of now)
        move_vec = np.array([xto-xf, yto-yf])
        poss_moves = []

        if for_white:
            poss_moves.append(np.array([-1,-1]))
            poss_moves.append(np.array([1,-1]))

        else:
            poss_moves.append(np.array([-1,1]))
            poss_moves.append(np.array([1,1]))
        
        # Is the destination empty?
        if self.board[xto,yto] != 0:
            print("There is something in the way.")
            return False
            
        # Check if move is legal
        for pm in poss_moves:
            if (pm == move_vec).all():
                return True
        
        return False
    
    def move(self, fro, to):
        """
        Moves the piece on 'fro' to 'to'.
        Assumes the input is all good in all the ways
        """

        self.board[to] = self.board[fro]
        self.board[fro] = 0

    def take_turn(self, for_white):
        '''
        A player keeps trying to make moves until they can,
        then the other.
        '''
    
        turn_done = False
        while not turn_done:

            move = game.get_input(for_white)
            if move == -1:
                return -1
            
            fro,to = move
            valid = game.is_move_valid(fro, to, for_white)
            if valid:
                print(f"{self.name[for_white]} moves from {fro} to {to}.")
                game.move(fro,to)
                turn_done = True
            else:
                print("That simply cannot be done.")

            print()
  
    def play(self):
        '''
        Play a game of dame
        '''

        for_white = True
        while True:
            self.print_board()
            if self.take_turn(for_white) == -1:
                break
            for_white = not for_white


if __name__ == "__main__":

    game = Dame()
    game.play()
        