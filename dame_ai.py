import dame as dm # helps vscode autofill stuff while coding
from random import choice
from time import sleep

class Dame_AI:
    '''
        A robot that plays dame and tries not to lose
    '''


    def __init__(self, game, is_white):
        '''
            Links robot to the game
        '''

        self.game = game
        self.is_white = is_white

    def list_valid_moves(self):
        '''
            Gives a list of moves the robot can make,
            only includes jumps if the robot can jump.
        '''

        moves = self.game.list_valid_moves(self.is_white)

        # Keep ony jumps if needed
        if self.game.can_jump(self.is_white):
            moves = [move for move in moves if abs(move[0][0] - move[1][0]) == 2]

        return moves
    
    def choose_move(self):
        '''
            Chooses a move somehow.
            TODO: make choice good
        '''

        moves = self.list_valid_moves()
        hmm = []

        for fro, to in moves:

            hypgame = dm.Dame(self.game.board.copy(),
                              list(self.game.white_pieces), list(self.game.black_pieces))
            hypgame.move(fro, to, self.is_white)
            hmm.append(hypgame)
            print(f"{self.game.col_to_char[fro[0]] + str(8-fro[1])} {self.game.col_to_char[to[0]] + str(8-to[1])} leads to score of {hypgame.eval_board(self.is_white)}")

        return moves[max(range(len(hmm)), key= lambda idx: hmm[idx].eval_board(self.is_white))]

    
    def take_turn(self):
        '''
            The robot takes its turn at the game
        '''

        print("The robot is thinking REALLY hard...")
        sleep(1) # For authenticity

        turn_done = False
        while not turn_done: 

            fro, to = self.choose_move()

            print(f"{self.game.name[self.is_white]}, the robot moves from {self.game.col_to_char[fro[0]] + str(8-fro[1])} to {self.game.col_to_char[to[0]] + str(8-to[1])}.")

            turn_done = not self.game.move(fro, to, self.is_white) # Stays as True if you jump

            if not turn_done:

                # Check to see if the jumping piece can jump again
                turn_done = True

                for (xf,yf), (xto,_) in self.list_valid_moves():

                    # We found the jumper, can he jump?
                    if (xf,yf) == to and abs(xf-xto) == 2:
                        turn_done = False
                        self.game.print_board()
                        print("The robot is hyperventilating.")
                        sleep(1) # For authenticity
                        break

                print(f"It't a clean kill!{int(not turn_done) * ' keep going, robot!'}")
