# Early-game positional values for each piece type. Referenced from https://www.chessprogramming.org/Simplified_Evaluation_Function
# To-do: Add late-game positional tables and implement a Tapered Eval to interpolate these values throughout the game

import chess

pawnEarly = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    5, -5, -10, 0, 0, -10, -5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0]

knightEarly = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50]

bishopEarly = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20]

rookEarly = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0]

queenEarly = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 5, 5, 5, 5, 5, 0, -10,
    0, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20]

kingEarly = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30]


def endState(board):
    if board.is_checkmate():
        if board.turn:
            return -9999
        else:
            return 9999
    if board.is_stalemate() or board.is_insufficient_material():
        return 0


def evalFunction(valuesList, moveList):
    materialValue = 100 * (valuesList[0] - valuesList[1]) + 305 * (valuesList[2] - valuesList[3]) + 333 * (
            valuesList[4] - valuesList[5]) + 563 * (valuesList[6] - valuesList[7]) + 950 * (
                            valuesList[8] - valuesList[9])
    moveValue = sum(item for item in moveList)

    return materialValue + moveValue


def evaluation(board):
    if isinstance(endState(board), int):
        return endState(board)

    valuesList = [len(board.pieces(chess.PAWN, chess.WHITE)),
                  len(board.pieces(chess.PAWN, chess.BLACK)),
                  len(board.pieces(chess.KNIGHT, chess.WHITE)),
                  len(board.pieces(chess.KNIGHT, chess.BLACK)),
                  len(board.pieces(chess.BISHOP, chess.WHITE)),
                  len(board.pieces(chess.BISHOP, chess.BLACK)),
                  len(board.pieces(chess.ROOK, chess.WHITE)),
                  len(board.pieces(chess.ROOK, chess.BLACK)),
                  len(board.pieces(chess.QUEEN, chess.WHITE)),
                  len(board.pieces(chess.QUEEN, chess.BLACK))]

    pawnMove = sum([pawnEarly[i] for i in board.pieces(chess.PAWN, chess.WHITE)]) + sum(
        [-pawnEarly[chess.square_mirror(i)] for i in board.pieces(chess.PAWN, chess.BLACK)])
    knightMove = sum([knightEarly[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)]) + sum(
        [-knightEarly[chess.square_mirror(i)] for i in board.pieces(chess.KNIGHT, chess.BLACK)])
    bishopMove = sum([bishopEarly[i] for i in board.pieces(chess.BISHOP, chess.WHITE)]) + sum(
        [-bishopEarly[chess.square_mirror(i)] for i in board.pieces(chess.BISHOP, chess.BLACK)])
    rookMove = sum([rookEarly[i] for i in board.pieces(chess.ROOK, chess.WHITE)]) + sum(
        [-rookEarly[chess.square_mirror(i)] for i in board.pieces(chess.ROOK, chess.BLACK)])
    queenMove = sum([queenEarly[i] for i in board.pieces(chess.QUEEN, chess.WHITE)]) + sum(
        [-queenEarly[chess.square_mirror(i)] for i in board.pieces(chess.QUEEN, chess.BLACK)])
    kingMove = sum([kingEarly[i] for i in board.pieces(chess.KING, chess.WHITE)]) + sum(
        [-kingEarly[chess.square_mirror(i)] for i in board.pieces(chess.KING, chess.BLACK)])

    moveList = [pawnMove, knightMove, bishopMove, rookMove, queenMove, kingMove]

    return evalFunction(valuesList, moveList)
