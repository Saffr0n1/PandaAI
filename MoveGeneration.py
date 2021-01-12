# Negamax with alpha-beta pruning
# Quiescence search performed at the end of the main search to evaluate positions without winning moves

import chess, chess.svg, chess.polyglot, chess.pgn, chess.engine
from BoardEval import *


def quiesce(A, B, board):
    currState = evaluation(board)
    if currState >= B:
        return B
    if currState > A:
        A = currState

    for move in board.legal_moves:
        if board.is_capture(move):
            board.push(move)
            gameState = -quiesce(-B, -A, board)
            board.pop()

            if gameState >= B:
                return B
            if gameState > A:
                A = gameState

    return A


def negamaxAB(A, B, depth, board):
    if depth == 0:
        return quiesce(A, B, board)

    maxScore = -999999

    for move in board.legal_moves:
        board.push(move)
        score = -negamaxAB(-B, -A, depth - 1, board)
        board.pop()

        if score >= B:
            return score
        if score > maxScore:
            maxScore = score
        if score > A:
            A = score

    return maxScore


def nextMove(depth, board):
    try:
        return chess.polyglot.MemoryMappedReader("Perfect2019.bin").weighted_choice(board).move
    except:
        goodMove = chess.Move.null()
        maxScore = -999999
        A = -1000000
        B = 1000000
        for move in board.legal_moves:
            board.push(move)
            state = -negamaxAB(-B, -A, depth - 1, board)
            if state > maxScore:
                maxScore = state
                goodMove = move
            if state > A:
                A = state

            board.pop()
        return goodMove
