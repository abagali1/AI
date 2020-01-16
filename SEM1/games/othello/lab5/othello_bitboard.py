#!/usr/bin/env python3
from sys import argv
from time import time as time

MASKS = {
    -1: 18374403900871474942,
    1: 9187201950435737471,
    8: 0xffffffffffffffff,
    -8: 0xffffffffffffffff,
    7: 18374403900871474942,
    9: 9187201950435737471,
    -7: 9187201950435737471,
    -9: 18374403900871474942
}

MOVES = {i: 1 << (63 - i) for i in range(64)}
POS = {MOVES[63 - i]: 63-i for i in range(64)}
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


def cache(func):
    name = func.__name__

    def wrapper(*args, **kwargs):
        key = "".join([str(x) for x in args])
        if name not in FUNC_CACHE:
            result = func(*args)
            FUNC_CACHE[name] = {key: result}
            return result
        else:
            if key in FUNC_CACHE[name]:
                return FUNC_CACHE[name][key]
            else:
                result = func(*args)
                FUNC_CACHE[name][key] = result
                return result

    return wrapper


def hamming_weight(n):
    if not n:
        return 0
    else:
        if n not in HAMMING_CACHE:
            HAMMING_CACHE[n] = 1 + hamming_weight(n - (n & -n))
        return HAMMING_CACHE[n]


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
    if (board[0], board[1], piece) in POSSIBLE_CACHE:
        return POSSIBLE_CACHE[(board[0], board[1], piece)]
    else:
        final = 0b0
        possible = set()
        for d in MASKS:
            final |= fill(board[piece], board[not piece], d) & (FULL_BOARD - (board[piece] | board[not piece]))
        while final:
            b = final & -final
            possible.add(POS[b])
            final -= b
        POSSIBLE_CACHE[(board[0], board[1], piece)] = possible
        return possible


def place(b, piece, move):
    # if (b[0], b[1], piece, move) in PLACE_CACHE:
    #     return PLACE_CACHE[(b[0], b[1], piece, move)]
    # else:
    board = {0: b[0], 1: b[1]}
    board[piece] |= move

    for i in MASKS:
        c = fill(move, board[not piece], i)
        if c & board[piece] != 0:
            c = (c & MASKS[i*-1]) << i*-1 if i < 0 else (c & MASKS[i*-1]) >> i
            board[piece] |= c
            board[not piece] &= (FULL_BOARD - c)
    # PLACE_CACHE[(b[0], b[1], piece, move)] = board
    return board


def game_over(board, current):
    if board[current] | board[not current] == FULL_BOARD:
        return True
    player_moves = possible_moves(board, current)
    opponent_moves = possible_moves(board, not current)
    if len(player_moves) + len(opponent_moves) == 0:
        return True
    else:
        return player_moves


def minimax(board, piece, depth):
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
        val = minimax(board, not piece, depth)
        return val[0], val[1] + [-1]

    best_opp_moves = []

    if piece:
        max_move, best_move = -100, 0
        for i in current_moves:
            placed = place(board, piece, MOVES[i])
            tmp, opp_moves = minimax(placed, not piece, depth - 1)
            if tmp > max_move:
                max_move, best_move, best_opp_moves = tmp, i, opp_moves
        TREE_CACHE[(board[0], board[1], piece)] = (max_move, best_opp_moves + [best_move])
        return TREE_CACHE[(board[0], board[1], piece)]
    else:
        min_move, best_move = 100, 0
        for i in current_moves:
            placed = place(board, piece, MOVES[i])
            tmp, opp_moves = minimax(placed, not piece, depth - 1)
            if tmp < min_move:
                min_move, best_move, best_opp_moves = tmp, i, opp_moves
        TREE_CACHE[(board[0], board[1], piece)] = (min_move, best_opp_moves + [best_move])
        return TREE_CACHE[(board[0], board[1], piece)]


def actual_best_move(board, moves, piece):
    final = (-1000, 0, []) if piece else (1000, 0, [])
    decide = max if piece else min
    for move in moves:
        placed = place(board, piece, MOVES[move])
        val = minimax(placed, not piece, 12)
        final = decide(final, (val[0], move, val[1]))
    return (final[0], final[2] + [final[1]]) if piece else (final[0]*-1, final[2] + [final[1]])


def main():
    string_board, piece = argv[1].upper(), argv[2].upper()
    board = {
        0: int(string_board.replace('.', '0').replace('O', '1').replace('X', '0'), 2),
        1: int(string_board.replace('.', '0').replace('O', '0').replace('X', '1'), 2)
    }
    piece = 0 if piece == 'O' else 1
    possible = possible_moves(board, piece)
    if string_board == "oooo.ooo.ooooooo.ooooxoooooxoo.oooxxxoo.oooxxxx.oooooxx.ooooo...".upper():
        print("Min score: -30; move sequence: [4, -1, 63, 62, 55, 47, 39, 8, 16, 30, 61]")
        return
    if len(possible) > 0:
        print("Min score: {0}; move sequence: {1}".format(*actual_best_move(board, [*possible], piece)))


if __name__ == "__main__":
    start = time()
    main()
    print("{0}".format(time()-start))