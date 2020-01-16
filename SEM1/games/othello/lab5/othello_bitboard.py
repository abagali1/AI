#!/usr/bin/env python3
from sys import argv
from time import time as time

MASKS = {
    1: lambda x: (x & 0xfefefefefefefefe) >> 1,
    -1: lambda x: (x & 0x7f7f7f7f7f7f7f7f) << 1,
    8: lambda x: x << 8,
    -8: lambda x: x >> 8,
    9: lambda x: ((x & 0xfefefefefefefefe) >> 1) << 8,
    7: lambda x: ((x & 0x7f7f7f7f7f7f7f7f) << 1) << 8,
    -9: lambda x: ((x & 0x7f7f7f7f7f7f7f7f) << 1) >> 8,
    -7: lambda x: ((x & 0xfefefefefefefefe) >> 1) >> 8
}

MOVES = {i: 1 << (63 - i) for i in range(64)}
LOG = {MOVES[63 - i]: i for i in range(64)}
FULL_BOARD = 0xffffffffffffffff

CORNERS = {0, 7, 56, 63}
CORNER_NEIGHBORS = {1: 63, 6: 56, 8: 63, 9: 63, 14: 56, 15: 56, 48: 7, 49: 7, 54: 0, 55: 0, 57: 7, 62: 0}
COL_EDGES = {1: {7, 15, 23, 31, 39, 47, 55, 63}, 0: {0, 8, 16, 24, 32, 40, 48, 56}}
ROW_EDGES = {0: {0, 1, 2, 3, 4, 5, 6, 7}, 1: {56, 57, 58, 59, 60, 61, 62, 6}}

EDGES = {0: {0, 1, 2, 3, 4, 5, 6, 7}, 1: {56, 57, 58, 59, 60, 61, 62, 6}, 2: {7, 15, 23, 31, 39, 47, 55, 63},
         3: {0, 8, 16, 24, 32, 40, 48, 56}}

FUNC_CACHE = {}
HAMMING_CACHE = {}
TREE_CACHE = {}
POSSIBLE_CACHE = {}
PLACE_CACHE = {}
FILL_CACHE = {}
fill_cached = 0

bit_not = lambda x: 0xffffffffffffffff - x
is_on = lambda x, pos: x & MOVES[63 - pos]

binary_to_board = lambda board: "".join(
    ['o' if is_on(board[0], 63 - i) else 'x' if is_on(board[1], 63 - i) else '.' for i in range(64)])

board_to_string = lambda x: '\n'.join([''.join([x[i * 8 + j]][0] for j in range(8)) for i in range(8)]).strip().lower()
binary_to_string = lambda x: '\n'.join(
    [''.join(['{:064b}'.format(x)[i * 8 + j][0] for j in range(8)]) for i in range(8)]).strip().lower()

print_binary = lambda x: print(binary_to_string(x))
print_board = lambda x: print(board_to_string(x))
print_board_binary = lambda x: print(board_to_string(binary_to_board(x)))


def cache(func):
    name = func.__name__

    def wrapper(*args, **kwargs):
        if name not in FUNC_CACHE:
            result = func(*args)
            FUNC_CACHE[name] = {args: result}
            return result
        else:
            if args in FUNC_CACHE[name]:
                return FUNC_CACHE[name][args]
            else:
                result = func(*args)
                FUNC_CACHE[name][args] = result
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
    if (current, opponent, direction) in FILL_CACHE:
        return FILL_CACHE[(current, opponent, direction)]
    else:
        mask = MASKS[direction]
        w = mask(current) & opponent
        w |= mask(w) & opponent
        w |= mask(w) & opponent
        w |= mask(w) & opponent
        w |= mask(w) & opponent
        w |= mask(w) & opponent
        FILL_CACHE[(current, opponent, direction)] = mask(w)
        return FILL_CACHE[(current, opponent, direction)]


def possible_moves(board, piece):
    if (board[0], board[1], piece) in POSSIBLE_CACHE:
        return POSSIBLE_CACHE[(board[0], board[1], piece)]
    else:
        final = 0b0
        possible = set()
        for d in MASKS:
            final |= fill(board[piece], board[not piece], d) & (0xffffffffffffffff - (board[piece] | board[not piece]))
        while final:
            b = final & -final
            possible.add(63 - LOG[b])
            final -= b
        POSSIBLE_CACHE[(board[0], board[1], piece)] = possible
        return possible


@cache
def place(current, opponent, piece, move):
    board = {piece: current, not piece: opponent}
    board[piece] |= move

    for i in MASKS:
        c = fill(move, board[not piece], i)
        if c & board[piece] != 0:
            c = MASKS[i * -1](c)
            board[piece] |= c
            board[not piece] &= bit_not(c)
    return board


def game_over(board, current):
    if (board[current] | board[not current]) == FULL_BOARD:
        return True
    player_moves = possible_moves(board, current)
    opponent_moves = possible_moves(board, not current)
    return player_moves, (len(player_moves) + len(opponent_moves)) == 0


def minimax(board, piece, past_moves, depth):
    """
    Returns the best value, [sequence of the previous best moves]
    """
    # if (board[0], board[1], piece) in TREE_CACHE:
    #     return TREE_CACHE[(board[0], board[1], piece)]

    current_moves, state = game_over(board, piece)
    if state or depth == 0:
        score = hamming_weight(board[1]) - hamming_weight(board[0])
        return score, past_moves

    if not len(current_moves):
        score, moves = minimax(board, not piece, past_moves + [-1], depth - 1)
        return score, moves

    best_opp_moves = []

    if piece:
        max_move = -100
        for i in current_moves:
            score, opp_moves = minimax(place(board[piece], board[not piece], piece, MOVES[i]), not piece,
                                       past_moves + [i], depth - 1)
            if score > max_move:
                max_move, best_opp_moves = score, opp_moves
        # TREE_CACHE[(board[0], board[1], piece)] = (max_move, best_opp_moves + [best_move])
        return max_move, best_opp_moves
    else:
        min_move = 100
        for i in current_moves:
            score, opp_moves = minimax(place(board[piece], board[not piece], piece, MOVES[i]), not piece,
                                       past_moves + [i], depth - 1)
            if score < min_move:
                min_move, best_opp_moves = score, opp_moves
        # TREE_CACHE[(board[0], board[1], piece)] = (min_move, best_opp_moves + [best_move])
        return min_move, best_opp_moves


def actual_best_move(board, moves, piece):
    best = []
    for move in moves:
        placed = place(board[piece], board[not piece], piece, MOVES[move])
        val = minimax(placed, not piece, [], 12)
        best.append((val[0], move, val[1]))
    final = max(best, key=lambda x: x[0]) if piece else min(best, key=lambda x: x[0])
    return final[0], final[2] + [final[1]]


def main():
    string_board, piece = argv[1].upper(), argv[2].upper()
    board = {
        0: int(string_board.replace('.', '0').replace('O', '1').replace('X', '0'), 2),
        1: int(string_board.replace('.', '0').replace('O', '0').replace('X', '1'), 2)
    }
    piece = 0 if piece == 'O' else 1
    possible = possible_moves(board, piece)
    moves = len(possible)
    if moves > 0:
        print("Min score: {0}; move sequence: {1}".format(*actual_best_move(board, [*possible], piece)))


if __name__ == "__main__":
    start = time()
    main()
    # print("{0}".format(time() - start))
