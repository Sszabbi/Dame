import numpy as np
from itertools import product

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
            0: '_', # Empty square
            1: 'W', # White piece 
            2: 'B', # Black piece
            3: "Q", # White super piece (queen)
            4: "D"  # Black super piece (dame)
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

    def coords_to_index(self, coords: str):
        """
        Turns an on-board coordinates into the index of said coordinates in self.board
        e.g. if coords="a8" it returns (0,0). Used at input parsing.
        Returns and off-board index if input is eugh.
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
    
    def get_input(self, for_white: bool):
        '''
            Keeps asking for input until you put in somthing that makes sense.
            Makes sense means two baord-read coordinates like "a4 f5"

            Returns np arrays to and fro with the appropriate coordinates
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
        
    def can_jump(self, for_white: bool):
        """
            Returns True if the player can make a capture
            (for those unaware, the rules say that you MUST make that jump then.)
        """

        moves = self.list_valid_moves(for_white)
        for (xf,_), (xto,_) in moves:

            if abs(xf-xto) == 2:
                print(f"{self.name[for_white]} sees a vulnerable enemy! They are seeing red!")
                return True
            
        return False
    
    def is_move_valid(self, fro: tuple, to: tuple, for_white: bool, must_jump: bool,
                      verbose: bool = True):
        '''
            Examines the validity of a player moving from "fro" to "to".

            Player is white iff for_white is True
            fro and to are tuples with the indices of the places in self.board

            If you must jump, you must jump.

            In verbose mode, shows a "helpful" message if your move cannot be moved
        '''

        xf, yf = fro
        xto, yto = to

        for coord in [xf,yf,xto,yto]:
            if coord not in range(8):
                return False
            
        # Check if you are jumping if you must.
        if must_jump and abs(xf-xto) != 2:
            print("You have to jump, you just have to.")
            return False
            
        # Do you have a piece there?
        your_pieces = [1, 3] if for_white else [2, 4]
        enemy_pieces = [2, 4] if for_white else [1, 3]

        if self.board[xf,yf] not in your_pieces:
            if verbose:
                print("You have no piece there, blindo.")
            return False
        
        
        # Is the destination empty?
        if self.board[xto,yto] != 0:
            if verbose:
                print("There is something in the way.")
            return False

        poss_moves = [] # Your movement should be in here somehow

        # Moving up
        if for_white or (not for_white and self.board[xf,yf] == your_pieces[1]):
            poss_moves.append(np.array([-1,-1]))
            poss_moves.append(np.array([1,-1]))

        # Moving down
        if not for_white or (for_white and self.board[xf,yf] == your_pieces[1]):
            poss_moves.append(np.array([-1,1]))
            poss_moves.append(np.array([1,1]))
        
        move_vec = np.array([xto-xf, yto-yf])

        # Check if you're trying to jump over someone
        if abs(move_vec[0]) == 2 and abs(move_vec[1]) == 2:
            move_vec //= 2
            ovx, ovy = np.array(fro) + move_vec
            if self.board[ovx, ovy] not in enemy_pieces:
                if verbose:
                    print("You can only jump over an enemy beforeward of you.")
                return False
            
        # Check if move is legal
        for pm in poss_moves:
            if (pm == move_vec).all():
                return True
        
        if verbose:
            print("That move is against the law.")
        return False
    
    def move(self, fro: tuple, to: tuple, for_white: bool):
        """
        Moves the piece on 'fro' to 'to'.
        Assumes the input is all good in all the ways.

        If it's a jump then obliterate anything inbetween and return True.
        (Returns False if not a jump, then.)

        If a regular piece reaches the opposite side, promote it to super piece.
        """

        # Moving the piece and leaving nothing behind
        self.board[to] = self.board[fro]
        self.board[fro] = 0

        # Check for promotion (other side + regular piece)
        if to[1] == 7 - int(for_white) * 7 and self.board[to] < 3:
            self.board[to] += 2
            print(f"The {self.name[for_white]} piece reaches the enemy lines! Promoted!")

        # (For the needy functions)
        to = np.array(to)
        fro = np.array(fro)


        # Remove over-jumped piece forever
        if abs(to[0] - fro[0]) == 2 and abs(to[1] - fro[1]) == 2:
            ovx, ovy = (fro+to)//2
            self.board[ovx,ovy] = 0
            return True
        
        return False

    def take_turn(self, for_white: bool):
        '''
        A player keeps trying to make moves until they can,
        then the other.
        '''
    
        turn_done = False
        while not turn_done:

            move = game.get_input(for_white)
            if move == -1:
                return -1
            
            # Move examination
            fro,to = move
            must_jump = self.can_jump(for_white)
            valid = game.is_move_valid(fro, to, for_white, must_jump)

            if valid:

                print(f"{self.name[for_white]} moves from {fro} to {to}.")
                turn_done = not game.move(fro, to, for_white) # Stays as True if you jump

                if not turn_done:

                    # Check to see if the jumping piece can jump again
                    turn_done = True

                    for (xf,yf), (xto,_) in self.list_valid_moves(for_white):

                        # We found the jumper, can he jump?
                        if (xf,yf) == to and abs(xf-xto) == 2:
                            turn_done = False
                            break

                    print(f"It't a clean kill!{int(not turn_done) * ' keep going!'}")

                else:
                    print()

            else:
                print("That simply cannot be done.")
                print()
  
    def list_valid_moves(self, for_white: bool):
        '''
            Makes a list of all possible moves that a player can make.
            The moves are in the from of tuples.
        '''
        moves = []
        your_pieces = [1,3] if for_white else [2, 4]

        for x,y in product(range(8),range(8)):

            # Piece found
            if self.board[x,y] in your_pieces:

                # This checks all 8 possible moves no matter what, which is honestly fine.
                for dx,dy in list(product([-1,1],[-1,1])) + list(product([-2,2],[-2,2])):

                    if self.is_move_valid((x,y), (x+dx, y+dy), for_white, must_jump = False,
                                          verbose = False):
                        moves.append(( (x,y),(x+dx,y+dy) ))
                        
        return moves

    def is_game_over(self, for_white: bool, verbose:bool = True):
        '''
            Checks if the game is over for a player.
            Returns True if the player has no possible moves
            Return False if the player has possible moves.
        '''

        moves = self.list_valid_moves(for_white)

        if len(moves) == 0:
            if verbose:
                print(f"Not a move to make for {self.name[for_white]}. Sad.")
            return True

        elif verbose:
                print(f"{self.name[for_white]} has a move: {moves[0]}, so the game is still going.")
        return False

    def play(self):
        '''
        Play a game of dame
        '''

        for_white = True
        running = True
        while running:

            self.print_board()
            if self.take_turn(for_white) == -1:
                break
            for_white = not for_white

            if self.is_game_over(for_white):
                
                running = False
                self.print_board()
                print(f"{self.name[not for_white]} has Won! The Game! Wow! Good job!")


if __name__ == "__main__":

    game = Dame()
    game.play()
        