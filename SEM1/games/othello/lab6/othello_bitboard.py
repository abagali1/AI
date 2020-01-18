#!/usr/bin/env python3
from sys import argv
from time import time as time

MASKS = {
    -1: 0xfefefefefefefefe,
    1: 0x7f7f7f7f7f7f7f7f,
    8: 0xffffffffffffffff,
    -8: 0xffffffffffffffff,
    7: 0xfefefefefefefefe,
    9: 0x7f7f7f7f7f7f7f7f,
    -7: 0x7f7f7f7f7f7f7f7f,
    -9: 0xfefefefefefefefe
}


MOVES = {i: 1 << (63 - i) for i in range(64)}
POS = {MOVES[63 - i]: 63 - i for i in range(64)}
FULL_BOARD = 0xffffffffffffffff

CORNERS = {0, 7, 56, 63}
CORNER_NEIGHBORS = {1: 63, 6: 56, 8: 63, 9: 63, 14: 56, 15: 56, 48: 7, 49: 7, 54: 0, 55: 0, 57: 7, 62: 0}
COL_EDGES = {1: {7, 15, 23, 31, 39, 47, 55, 63}, 0: {0, 8, 16, 24, 32, 40, 48, 56}}
ROW_EDGES = {0: {0, 1, 2, 3, 4, 5, 6, 7}, 1: {56, 57, 58, 59, 60, 61, 62, 6}}

EDGES = {0: {0, 1, 2, 3, 4, 5, 6, 7}, 1: {56, 57, 58, 59, 60, 61, 62, 6}, 2: {7, 15, 23, 31, 39, 47, 55, 63},
         3: {0, 8, 16, 24, 32, 40, 48, 56}}


FUNC_CACHE = {}
HAMMING_CACHE = {}
POSSIBLE_CACHE = {}
PLACE_CACHE = {}
TREE_CACHE = {}
FILL_CACHE = {}


def hamming_weight(n):
    if n in HAMMING_CACHE:
        return HAMMING_CACHE[n]
    else:
        orig = n
        c = 0
        while n:
            c+=1
            n ^= n&-n
        HAMMING_CACHE[orig] = c
        return HAMMING_CACHE[orig]


def fill(current, opponent, direction):
    mask = MASKS[direction]
    if direction > 0:
        w = ((current & mask) << direction) & opponent
        w |= ((w & mask) << direction) & opponent
        w |= ((w & mask) << direction) & opponent
        w |= ((w & mask) << direction) & opponent
        w |= ((w & mask) << direction) & opponent
        w |= ((w & mask) << direction) & opponent
        return (w & mask) << direction
    else:
        direction *= -1
        w = ((current & mask) >> direction) & opponent
        w |= ((w & mask) >> direction) & opponent
        w |= ((w & mask) >> direction) & opponent
        w |= ((w & mask) >> direction) & opponent
        w |= ((w & mask) >> direction) & opponent
        w |= ((w & mask) >> direction) & opponent
        return (w & mask) >> direction


def possible_moves(board, piece):
    key = (board[0]<<64)+board[1]+piece
    if key in POSSIBLE_CACHE:
        return POSSIBLE_CACHE[key]
    else:
        final = 0b0
        possible = set()
        for d in MASKS:
            final |= fill(board[piece], board[not piece], d) & (FULL_BOARD - (board[piece] | board[not piece]))
        while final:
            b = final & -final
            possible.add(POS[b])
            final -= b
        POSSIBLE_CACHE[key] = possible
        return possible


def place(b, piece, move):
    board = {0: b[0], 1: b[1]}
    board[piece] |= move

    for i in MASKS:
        c = fill(move, board[not piece], i)
        if c & board[piece] != 0:
            c = (c & MASKS[i * -1]) << i * -1 if i < 0 else (c & MASKS[i * -1]) >> i
            board[piece] |= c
            board[not piece] &= (FULL_BOARD - c)
    return board


def game_over(board, current):
    if board[current] | board[not current] == FULL_BOARD:
        return True
    player_moves = possible_moves(board, current)
    opponent_moves = possible_moves(board, not current)
    return True if len(player_moves) + len(opponent_moves) == 0 else player_moves


def minimax(board, piece, depth, alpha, beta):
    """
    Returns the best value, [sequence of the previous best moves]
    """
    if (board[0], board[1], piece) in TREE_CACHE:
        return TREE_CACHE[(board[0], board[1], piece)]

    state = game_over(board, piece)
    if state is True or depth == 0:
        return hamming_weight(board[1]) - hamming_weight(board[0]), []
    else:
        current_moves = state

    if len(current_moves) == 0:
        val = minimax(board, not piece, depth, alpha, beta)
        return val[0], val[1] + [-1]

    best_opp_moves = []
    if piece:
        max_move, best_move = -100, 0
        for i in current_moves:
            placed = place(board, piece, MOVES[i])
            tmp, opp_moves = minimax(placed, not piece, depth - 1, alpha, beta)
            if tmp > max_move:
                max_move, best_move, best_opp_moves = tmp, i, opp_moves
            alpha = max(max_move, alpha)
            if beta <= alpha:
                break
        TREE_CACHE[(board[0], board[1], piece)] = (max_move, best_opp_moves + [best_move])
        return TREE_CACHE[(board[0], board[1], piece)]
    else:
        min_move, best_move = 100, 0
        for i in current_moves:
            placed = place(board, piece, MOVES[i])
            tmp, opp_moves = minimax(placed, not piece, depth - 1, alpha, beta)
            if tmp < min_move:
                min_move, best_move, best_opp_moves = tmp, i, opp_moves
            beta = min(min_move, beta)
            if beta <= alpha:
                break
        TREE_CACHE[(board[0], board[1], piece)] = (min_move, best_opp_moves + [best_move])
        return TREE_CACHE[(board[0], board[1], piece)]


def mobility_heuristic(board, move, piece): # MAX: 0 MIN: -340
    placed = place(board, piece, move)
    opp_moves = possible_moves(placed, not piece)
    h = -len(opp_moves)*10
    if any(map(lambda x: x in CORNERS, opp_moves)):
        h -= 1000
    return h


def actual_best_move(board, moves, piece):
    final = (-1000, 0, 0) if piece else (1000, 0, 0)
    for move in moves:
        placed = place(board, piece, MOVES[move])
        val = minimax(placed, not piece, 12, -10000, 10000)
        final = max(final,(val[0], move, val[1]+[move])) if piece else min(final,(val[0], move, val[1]+[move]))
        print("Min score: {0}; move sequence: {1}".format(final[0], final[2]) if piece else "Min score: {0}; move sequence: {1}".format(final[0]*-1, final[2]))


def main():
    string_board, piece = argv[1].upper(), argv[2].upper()
    board = {
        0: int(string_board.replace('.', '0').replace('O', '1').replace('X', '0'), 2),
        1: int(string_board.replace('.', '0').replace('O', '0').replace('X', '1'), 2)
    }
    piece = 0 if piece == 'O' else 1
    possible = possible_moves(board, piece)
    if possible:
        actual_best_move(board, possible, piece)


if __name__ == "__main__":
    start = time()
    main()
    print("{0}".format(time() - start))
