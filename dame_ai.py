import dame as dm
import numpy as np

class Dame_AI:
    '''
        A robot that plays dame and tries not to lose
    '''

    def __init__(self, game:dm.Dame, is_white:bool):
        '''
            Links robot to the game
        '''

        self.game = game
        self.is_white = is_white

    def list_valid_moves(self, for_me:bool = True, board:np.array=None,
                         white_pieces:list=None, black_pieces:list=None):
        '''
            Gives a list of moves the robot can make,
            only includes jumps if the robot can jump.

            Or do that for the enemy.
        '''

        if board is None:
            board = self.game.board
            white_pieces = self.game.white_pieces
            black_pieces = self.game.white_pieces

        for_white = self.is_white if for_me else not self.is_white

        moves = dm.list_valid_moves(for_white, board, white_pieces, black_pieces)

        # Keep only jumps if needed
        if dm.can_jump(board, white_pieces, black_pieces, for_white):
            #print("Snip snip")
            moves = [move for move in moves if abs(move[0][0] - move[1][0]) == 2]
            #print(f"{len(moves)=} moves left")

        return moves
    
    def choose_move(self, depth:int, board:np.array=None, white_pieces:list=None, black_pieces:list=None):
        '''
            Chooses a move somehow.

            When depth is 0, pick the move that gives you the best score just now,
            return that move and the score it gives you.

            When depth is more than or equal to 1, uses minmax principles to choose the move that leads to the
            best score down the line assuming you're trying to force a low score for the robot.
        '''

        if board is None:
            board = self.game.board
            white_pieces = self.game.white_pieces
            black_pieces = self.game.black_pieces

        moves = self.list_valid_moves(True, board, white_pieces, black_pieces)
        hygames = []
        
        for fro, to in moves:

            # Hypothetic game for each move robot could make
            hygame = [board.copy(), list(white_pieces), list(black_pieces)]
            dm.move(hygame[0], hygame[1], hygame[2], fro, to, self.is_white)
            hygames.append(hygame)

        # At this point, hygames contains a boardstate for every move available now.

        if depth == 0: # No depth, just give the best move now
            best_idx = max(range(len(hygames)), key = lambda idx: 
                           dm.eval_board(hygames[idx][0], hygames[idx][1], hygames[idx][2], self.is_white))
            best_score = dm.eval_board(hygames[best_idx][0], hygames[best_idx][1],
                                       hygames[best_idx][2], self.is_white)
            return moves[best_idx], best_score
        
        else:
            potential_scores = [] # Gather the possible scorethe robot can end up with for each move the
                                  # Enemy (you) could make
            for gameno, hygame in enumerate(hygames):

                player_moves = self.list_valid_moves(False, hygame[0], hygame[1], hygame[2])
                player_games = []
                you_scores = []

                if len(player_moves) == 0: # The player loses if the robot picks this move
                    return moves[gameno], np.inf

                # The hypothetical you examines all moves they can make
                for pfro, pto in player_moves:
                    player_game = [hygame[0].copy(), list(hygame[1]), list(hygame[2])]
                    dm.move(player_game[0], player_game[1], player_game[2], pfro, pto, not self.is_white)
                    player_games.append(player_game)

                # robot picks a best move for every move you could make, tells the score this leads to. 
                for player_game in player_games:

                    # You get a bit dumber for the sake of finite runtime
                    _, best_score = self.choose_move(depth-1, player_game[0], player_game[1], player_game[2])
                    you_scores.append(best_score)

                # The enemy will pick a move that makes you end up with the least possible score in the end
                player_favorite_score = min(you_scores)
                potential_scores.append(player_favorite_score)

            # Pick the move that makes the enemy's favorite score the highest
            best_idx = max(range(len(potential_scores)), key=lambda idx: potential_scores[idx])
            return moves[best_idx], potential_scores[best_idx]
    
    def take_turn(self, depth:int, verbose:bool = False):
        '''
            The robot takes its turn at the game
        '''
        
        if verbose:
            print(f"The robot is thinking{depth * ' really'}{' hard'*int(depth>0)}...")

        turn_done = False
        while not turn_done: 

            (fro, to), _ = self.choose_move(depth)

            if verbose:
                print(f"{dm.name[self.is_white]}, the robot moves from {self.game.col_to_char[fro[0]] + str(8-fro[1])} to {self.game.col_to_char[to[0]] + str(8-to[1])}.")

            turn_done = not self.game.move(fro, to, self.is_white, verbose) # Stays as True if you jump

            if not turn_done:

                # Check to see if the jumping piece can jump again
                turn_done = True

                for (xf,yf), (xto,_) in self.list_valid_moves():

                    # We found the jumper, can he jump again?
                    if (xf,yf) == to and abs(xf-xto) == 2:
                        turn_done = False
                        
                        if verbose:
                            self.game.print_board()
                            print("The robot is hyperventilating.")

                        break # No need to keep checking

                if verbose:
                    print(f"It't a clean kill!{int(not turn_done) * ' keep going, robot!'}")
