import numpy as np
from itertools import product

from mainmenu import MainMenu
import dame_ai as dai


# Non-Object-Functions to speed up robots, as fast robots are cool. 

# A convinience for printing
name = {
    True: "White",
    False: "Black"
}

def can_jump(for_white, board, white_pieces, black_pieces):

    """
        Returns True if the player can make a capture
        (for those unaware, the rules say that you MUST make that jump then.)
    """

    moves = list_valid_moves(for_white, board, white_pieces, black_pieces)
    for (xf,_), (xto,_) in moves:

        if abs(xf-xto) == 2:
            return True
        
    return False

def is_move_valid(board, fro: tuple, to: tuple, for_white: bool, must_jump: bool,
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

    if board[xf,yf] not in your_pieces:
        if verbose:
            print("You have no piece there, blindo.")
        return False
        
    
    # Is the destination empty?
    if board[xto,yto] != 0:
        if verbose:
            print("There is something in the way.")
        return False

    poss_moves = [] # Your movement should be in here somehow

    # Moving up
    if for_white or (not for_white and board[xf,yf] == your_pieces[1]):
        poss_moves.append(np.array([-1,-1]))
        poss_moves.append(np.array([1,-1]))

    # Moving down
    if not for_white or (for_white and board[xf,yf] == your_pieces[1]):
        poss_moves.append(np.array([-1,1]))
        poss_moves.append(np.array([1,1]))
    
    move_vec = np.array([xto-xf, yto-yf])

    # Check if you're trying to jump over someone
    if abs(move_vec[0]) == 2 and abs(move_vec[1]) == 2:
        move_vec //= 2
        ovx, ovy = np.array(fro) + move_vec
        if board[ovx, ovy] not in enemy_pieces:
            if verbose:
                print("You can only jump if an enemy is before you.")
            return False
        
    # Check if move is legal
    for pm in poss_moves:
        if (pm == move_vec).all():
            return True
    
    if verbose:
        print("That move is against the law.")
    return False
        
def list_valid_moves(for_white:bool, board:np.array, white_pieces:list, black_pieces:list):
    '''
        Makes a list of all possible moves that a player can make on a board.
        The moves are in the from of tuples.
    '''

    moves = []
    your_pieces = white_pieces if for_white else black_pieces

    for x,y in your_pieces:

        # This checks all 8 possible moves no matter what, which is honestly fine.
        for dx,dy in list(product([-1,1],[-1,1])) + list(product([-2,2],[-2,2])):

            if is_move_valid(board, (x,y), (x+dx, y+dy), for_white, must_jump = False,
                                        verbose = False):
                moves.append(( (x,y),(x+dx,y+dy) ))
                    
    return moves

def eval_board(board, white_pieces, black_pieces, for_white: bool):

    '''
        Gives an int score based on how good the position is for a player.
        The better the position, the higher the score.

        Things the score takes into account:

            + Number of pieces
            + Number of super pieces
            + Can you jump over an enemy piece

            - Similar things but for the enemy                       
    '''

    score = 0

    your_pieces = white_pieces if for_white else black_pieces
    enemy_pieces = black_pieces if for_white else white_pieces

    for x,y in your_pieces:

        # Head count

        score += 2 # +2 points per piece alive
        if board[x,y] > 2:
            score += 2 # +2 points per super piece

        score += len(list_valid_moves(for_white, board, white_pieces, black_pieces)) # +1 point for each potential legal move.

        frwrd = [-1] if for_white else [1]
        bckwrd = [1] if for_white else [-1]

        # Examining Weakness

        for dx,dy in product([-1,1],frwrd):
            try:
                if (x+dx, y+dy) in enemy_pieces and board[x-dx,y-dy] == 0:
                    score -= 30 # -20 points for each jump the opponent can make over you
            except:
                pass  # Ha kinyúlnánk a táblából (ez a komment valamiért magyarra sikerült, de nem javítom át.)

        for dx,dy in product([-1,1],bckwrd):
            try:
                if (board[x+dx,y+dy] > 2 and 
                    (x+dx, y+dy) in enemy_pieces and board[x-dx,y-dy] == 0):
                    score -= 30 # -20 points for each super jump the opponent can make over you
            except:
                pass # Ha kinyúlnánk a táblából

        # Examining Power
        
        for dx,dy in product([-1,1],frwrd):
            try:
                if (x+dx, y+dy) in enemy_pieces and board[x+2*dx,y+2*dy] == 0:
                    score += 10 # +10 points for each jump you can make over your opponent.
            except:
                pass # Ha kinyúlnánk a táblából

        for dx,dy in product([-1,1],bckwrd):
            try:
                if (board[x,y] > 2 and 
                    (x+dx, y+dy) in enemy_pieces and board[x+2*dx,y+2*dy] == 0):
                    score += 10 # +10 points for each super jump you can make over your opponent.
            except:
                pass # Ha kinyúlnánk a táblából

    return score

def move(board, white_pieces, black_pieces, fro: tuple, to: tuple, for_white: bool, verbose: bool = False):
    """
    Moves the piece on 'fro' to 'to'.
    Assumes the input is all good in all the ways.

    If it's a jump then obliterate anything inbetween and return True.
    (Returns False if not a jump, then.)

    If a regular piece reaches the opposite side, promote it to super piece.
    """
    your_pieces = white_pieces if for_white else black_pieces

    # Moving the piece and leaving nothing behind

    board[to] = board[fro]
    board[fro] = 0

    your_pieces.remove(fro)
    your_pieces.append(to)

    # Check for promotion (other side + regular piece)
    if to[1] == 7 - int(for_white) * 7 and board[to] < 3:
        board[to] += 2
        if verbose:
            print(f"The {name[for_white]} piece reaches the enemy lines! Promoted!")

    # (For the needy functions)
    to = np.array(to)
    fro = np.array(fro)


    # Remove over-jumped piece forever
    if abs(to[0] - fro[0]) == 2 and abs(to[1] - fro[1]) == 2:

        enemy_pieces = black_pieces if for_white else white_pieces

        ovx, ovy = (fro+to)//2
        board[ovx,ovy] = 0
        enemy_pieces.remove((ovx,ovy))
        return True
    
    return False

class Dame:
    '''
        The main managing class of the game dame (or checkers, by its actual boring name).
    '''

    def __init__(self, board: np.array = None, white_pieces: list = None, black_pieces: list = None,
                 interactive: bool = False):
        '''
            Makes a board in a starting state, or in a given state if a state is given.
        '''

        # The Board
        if board is None: # Starting position
            self.board = np.zeros([8,8], dtype=int)

            # Place White pieces
        
            self.white_pieces = []
            self.black_pieces = []
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

        else: # given start state
            self.board = board
            self.white_pieces = white_pieces
            self.black_pieces = black_pieces

        if interactive: # We don't need these when making hypothetical games (for the robot)

            # Used when the drawing the board
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

            # Used when saying moves
            self.col_to_char = {
                col: char for char, col in self.char_to_col.items() # A fenti inverze
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

            curr = input(f"Move for {name[for_white]}: ")

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

        return can_jump(for_white, self.board, self.white_pieces, self.black_pieces)
    
    def is_move_valid(self, fro: tuple, to: tuple, for_white: bool, must_jump: bool,
                      verbose: bool = True):
        '''
            Examines the validity of a player moving from "fro" to "to".

            Player is white iff for_white is True
            fro and to are tuples with the indices of the places in self.board

            If you must jump, you must jump.

            In verbose mode, shows a "helpful" message if your move cannot be moved
        '''

        return is_move_valid(self.board, fro, to, for_white, must_jump, verbose)
    
    def move(self, fro: tuple, to: tuple, for_white: bool, verbose: bool = False):
        """
        Moves the piece on 'fro' to 'to'.
        Assumes the input is all good in all the ways.

        If it's a jump then obliterate anything inbetween and return True.
        (Returns False if not a jump, then.)

        If a regular piece reaches the opposite side, promote it to super piece.
        """
        return move(self.board, self.white_pieces, self.black_pieces, fro, to, for_white, verbose)

    def take_turn(self, for_white: bool):
        '''
        A player keeps trying to make moves until they can,
        then the other.
        '''
    
        turn_done = False
        while not turn_done:

            move = self.get_input(for_white)
            if move == -1:
                return -1
            
            # Move examination
            fro,to = move
            must_jump = self.can_jump(for_white)
            valid = self.is_move_valid(fro, to, for_white, must_jump)

            if valid:

                print(f"{name[for_white]} moves from {self.col_to_char[fro[0]] + str(8-fro[1])} to {self.col_to_char[to[0]] + str(8-to[1])}.")
                turn_done = not self.move(fro, to, for_white, verbose=True) # Stays as True if you jump

                if not turn_done:

                    # Check to see if the jumping piece can jump again
                    turn_done = True

                    for (xf,yf), (xto,_) in self.list_valid_moves(for_white):

                        # We found the jumper, can he jump?
                        if (xf,yf) == to and abs(xf-xto) == 2:
                            turn_done = False
                            break

                    print(f"It't a clean kill!{int(not turn_done) * ' keep going!'}")
                    if not turn_done:
                        self.print_board()

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
        return list_valid_moves(for_white, self.board, self.white_pieces, self.black_pieces)

    def eval_board(self, for_white: bool):

        '''
            Gives an int score based on how good the position is for a player.
            The better the position, the higher the score.

            Things the score takes into account:

                + Number of pieces
                + Number of super pieces
                + Can you jump over an enemy piece

                - Similar things but for the enemy                       
        '''

        return eval_board(self.board, self.white_pieces, self.black_pieces, for_white)

    def is_game_over(self, for_white: bool, verbose:bool = True):
        '''
            Checks if the game is over for a player.
            Returns True if the player has no possible moves
            Return False if the player has possible moves.
        '''

        moves = self.list_valid_moves(for_white)

        if len(moves) == 0:
            if verbose:
                print(f"Not a move to make for {name[for_white]}. Sad.")
            return True

        elif verbose:
                print(f"{name[for_white]} has a move: {moves[0]}, so the game is still going.")
        return False

    def play_vs_man(self):

        '''
            Play a game of dame against one of your many friends
        '''

        for_white = True
        running = True

        # Base Game Loop
        while running:

            self.print_board()

            # Current player does things
            if self.take_turn(for_white) == -1: # -1 is the exit code
                running = False
            for_white = not for_white

            # Check for loser
            if self.is_game_over(for_white, verbose=False):
                
                running = False
                self.print_board()
                print(f"{name[not for_white]} has Won! The Game! Wow! Good job!")

    def play_vs_ai(self, team: bool, IQ:int):
        '''
            Play against a fully sentient, conscious artificial intelligence.
            You are playing on the team team, agiant an AI with an IQ of IQ.
        '''

        robot = dai.Dame_AI(self, is_white = False) #TODO: choose player

        for_white = team
        your_turn = team
        running = True

        while running:

            self.print_board()

            # Players and robots do things alike.
            
            # Human turn
            if your_turn:
                if self.take_turn(for_white) == -1:
                    running = False

            # Robot turn
            else:
                robot.take_turn(depth = IQ, verbose=True)

            for_white = not for_white
            your_turn = not your_turn

            # Check for loser
            if self.is_game_over(for_white, verbose=False):
                
                running = False
                self.print_board()
                print(f"{name[not for_white]} has Won! The Game! Wow! Good job!")

    def play(self):
        '''
            Pick and choose a way to play dame
        '''

        menu = MainMenu()
        command = menu.get_command()

        match command:

            case 0: # VS Man
                self.play_vs_man()

            case 1: # VS AI
                team, IQ = menu.setup_vs_ai()
                self.play_vs_ai(team, IQ)

            case 2: # QUIT
                print("Bye!")

if __name__ == "__main__":

    game = Dame(interactive=True)
    game.play()