import dame as dm
import numpy as np
from time import sleep

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

    def list_valid_moves(self, for_me:bool = True, game:dm.Dame=None):
        '''
            Gives a list of moves the robot can make,
            only includes jumps if the robot can jump.

            Or do that for the enemy.
        '''

        if game is None:
            game = self.game

        for_white = self.is_white if for_me else not self.is_white

        moves = game.list_valid_moves(for_white)

        # Keep ony jumps if needed
        if game.can_jump(for_white):
            moves = [move for move in moves if abs(move[0][0] - move[1][0]) == 2]

        return moves
    
    def choose_move(self, depth:int, game:dm.Dame=None):
        '''
            Chooses a move somehow.

            When depth is 0, pick the move that gives you the best score just now,
            return that move and the score it gives you.

            When depth is more than or equal to 1, it simulates depth moves, each with less depth-calculation,
            then chooses the move that led to the highest score you would hypothetically end up with.
        '''

        if game is None:
            game = self.game

        moves = self.list_valid_moves(game=game)
        hygames = []
        
        for fro, to in moves:

            # Hypothetic game for each move robot could make
            hygame = dm.Dame(game.board.copy(),
                              list(game.white_pieces), list(game.black_pieces))
            hygame.move(fro, to, self.is_white)
            hygames.append(hygame)

        # At this point, hygames contains a boardstate for every move available now.

        if depth == 0: # No depth, just give the best move now
            best_idx = max(range(len(hygames)), key = lambda idx: hygames[idx].eval_board(self.is_white))
            return moves[best_idx], hygames[best_idx].eval_board(self.is_white)
        
        else:
            potential_scores = [] # You'll see
            for hygame in hygames:

                enemy_moves = self.list_valid_moves(for_me=False, game=hygame)
                enemy_games = []
                you_scores = []

                # The hypothetical you examines all moves they can make
                for efro, eto in enemy_moves:
                    enemy_game = dm.Dame(hygame.board.copy(),
                              list(hygame.white_pieces), list(hygame.black_pieces))
                    enemy_game.move(efro, eto, not self.is_white)
                    enemy_games.append(enemy_game)

                # robot picks a best move for every move you could make, tells their score at the end. 
                for enemy_game in enemy_games:

                    # You get a bit dumber for the sake of finite runtime
                    _, best_score = self.choose_move(depth-1, enemy_game)
                    you_scores.append(best_score)

                # The enemy will pick a move that makes you end up with the least possible score in the end
                enemy_favorite_score = min(you_scores)
                potential_scores.append(enemy_favorite_score)

            # Pick the move that makes the enemy's favorite score the highest
            best_idx = max(range(len(potential_scores)), key=lambda idx: potential_scores[idx])
            return moves[best_idx], potential_scores[best_idx]
    
    def take_turn(self, depth:int, verbose:bool = False):
        '''
            The robot takes its turn at the game
        '''
        
        if verbose:
            print(f"The robot is thinking{depth * ' really'} hard...")

        turn_done = False
        while not turn_done: 

            (fro, to), _ = self.choose_move(depth)

            if verbose:
                print(f"{self.game.name[self.is_white]}, the robot moves from {self.game.col_to_char[fro[0]] + str(8-fro[1])} to {self.game.col_to_char[to[0]] + str(8-to[1])}.")

            turn_done = not self.game.move(fro, to, self.is_white, verbose) # Stays as True if you jump

            if not turn_done:

                # Check to see if the jumping piece can jump again
                turn_done = True

                for (xf,yf), (xto,_) in self.list_valid_moves():

                    # We found the jumper, can he jump?
                    if (xf,yf) == to and abs(xf-xto) == 2:
                        turn_done = False
                        
                        if verbose:
                            self.game.print_board()
                            print("The robot is hyperventilating.")
                            sleep(1) # For authenticity

                        break # No need to keep checking

                if verbose:
                    print(f"It't a clean kill!{int(not turn_done) * ' keep going, robot!'}")
