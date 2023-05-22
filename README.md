# Dame Rules

This program lets you play dame, which is a game shockingly similar to checkers.
The rules of the game are as follows:

- The game takes place on an 8x8 grid, each space having a unique name.

- The name of the j-th space of the i-th row is the j-th letter of the alphabet followed by 9-i. For example, the name of the upper-left corner would be "a8", the upper-right "h8", and so on.

- The two players, white and black, each start with twelwe pieces, arranged on the following spaces:

    - White pieces: a1, c1, e1, g1, b2, d2, f2, h2, a3, c3, e3, g3
    - Black pieces: b6, d6, f6, h6, a7, c7, e7, g7, b8, d8, f8, h8

- The first turn is white's, and every time a player fininshes their turn, the other player's turn starts.

- During their turn, a player must move one of their pieces to another space.

- The pieces can be moved diagonally, one square at a time, always moving one row and one column at a time while staying on the board.

- White's pieces can initially only go upward, whilst black's only downward.

- You cannot move your piece onto a space that already has another piece on it.

- If there is an enemy piece on a space you could move to, but the space opposite to them is empty, the player can jump over that piece, moving two rows and two columns at once. The piece they jumped over is removed from the game.

- After jumping over an enemy, if another enemy can be jumped over using the same piece, the player can jump with that piece again.

- If it's possible for a player to jump over an enemy piece, they must choose a move that jumps over an enemy.

- If a piece reaches the opposite side of the board (row 8 for white, row 1 for black), then that piece is promoted, and can move in any of the 4 diagonal directions.

- If a player has no possible moves to make on their turn, they lose, and the other player is declared the winner.

# How to Play

When starting the game, the player must choose one of the listed options to get started.

When choosing to play against an AI, you must choose which color to play as, and how smart the robot should be.

Note: The robot's current version is not entirely optimized, so it gets kind of slow at high difficulties (high meaning 3+), so intelligence is limited to 3 in this version.

While playing, a player may input '-1' at any time to quit the game.

## VS player
 
The players must input their moves one after another. The program always shows who's turn it currently is.
To say what move you want to make, you have to type in the name of the space that your piece is on, and then the name of the space you want to move it to.
For example, if white has a piece on e3 that they want to move to c4, they should write "e3 c4" on their turn.
If your move is illegal for some reason, say, there is already a piece where you want to move, or a jump is available the you're ignoring, or if the input was not correctly formatted or anything like that, the game will show a message telling you that your input was wrong, and you can try to do it again.
The players must keep moving pieces until somone wins.

## VS AI

The game plays the same as against another person, except one of the players is a robot.
The human player inputs their moves the same way they would in a VS player game, but the robot's moves are calculated by a computer, and do not need to be put in.
The game always shows you what move the robot makes, and only asks you to move after the robot's turn is done.
The game keeps going until someone loses.

# How the robot supposedly works

Every time you make a move, the robot analizes every move that it could make in return. For each one of those hypothetical moves, the robot then thinks about what you could move in return to that, and so on like that, until some point determined by difficulty. The robot tries to pick its moves to make you end up in the worst position it can force you into. 