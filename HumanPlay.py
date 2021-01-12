import chess, chess.svg, chess.polyglot, chess.pgn, chess.engine
from MoveGeneration import *

board = chess.Board()

# To have the engine select a move:

mov = nextMove(3, board)
board.push(mov)

# To have a player select a move:

board.push_san("e5")


