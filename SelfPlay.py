import chess, chess.svg, chess.polyglot, chess.pgn, chess.engine
import datetime
from MoveGeneration import *

turn = 0
history = []
game = chess.pgn.Game()
board = chess.Board()

while not board.is_game_over(claim_draw=True):
    if board.turn:
        turn += 1
        move = nextMove(3, board)
        board.push(move)
    else:
        move = nextMove(3, board)
        board.push(move)

game.add_line(history)
game.headers["Event"] = "Self Play"
game.headers["Date"] = str(datetime.datetime.now().date())
game.headers["Round"] = 1
game.headers["White"] = "Ai"
game.headers["Black"] = "Ai"
game.headers["Result"] = str(board.result(claim_draw=True))
print(game)
