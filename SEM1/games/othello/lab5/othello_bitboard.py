#!/usr/bin/env python3
from sys import argv
from time import time as time
from re import compile, IGNORECASE, match

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

STABLE_EDGE_REGEX = {
    1: compile(r"\.|\.$|^x+o*\.|\.o*x+", IGNORECASE),
    0: compile(r"\.|\.$|^o+x*\.|\.x*o+", IGNORECASE)
}

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

MOVES = {i: 1 << (63 - i) for i in range(64)}
POS = {MOVES[63 - i]: 63 - i for i in range(64)}
FULL_BOARD = 0xffffffffffffffff

CORNERS = {0, 7, 56, 63}
CORNER_NEIGHBORS = {1: 63, 6: 56, 8: 63, 9: 63, 14: 56, 15: 56, 48: 7, 49: 7, 54: 0, 55: 0, 57: 7, 62: 0}
COL_EDGES = {1: {7, 15, 23, 31, 39, 47, 55, 63}, 0: {0, 8, 16, 24, 32, 40, 48, 56}}
ROW_EDGES = {0: {0, 1, 2, 3, 4, 5, 6, 7}, 1: {56, 57, 58, 59, 60, 61, 62, 6}}

EDGES = {0: {0, 1, 2, 3, 4, 5, 6, 7}, 1: {56, 57, 58, 59, 60, 61, 62, 6}, 2: {7, 15, 23, 31, 39, 47, 55, 63},
         3: {0, 8, 16, 24, 32, 40, 48, 56}}
LETTERS = {'a1': 0, 'b1': 1, 'c1': 2, 'd1': 3, 'e1': 4, 'f1': 5, 'g1': 6, 'h1': 7, 'A1': 0, 'B1': 1, 'C1': 2, 'D1': 3,
           'E1': 4, 'F1': 5, 'G1': 6, 'H1': 7, 'a2': 8, 'b2': 9, 'c2': 10, 'd2': 11, 'e2': 12, 'f2': 13, 'g2': 14,
           'h2': 15, 'A2': 8, 'B2': 9, 'C2': 10, 'D2': 11, 'E2': 12, 'F2': 13, 'G2': 14, 'H2': 15, 'a3': 16, 'b3': 17,
           'c3': 18, 'd3': 19, 'e3': 20, 'f3': 21, 'g3': 22, 'h3': 23, 'A3': 16, 'B3': 17, 'C3': 18, 'D3': 19, 'E3': 20,
           'F3': 21, 'G3': 22, 'H3': 23, 'a4': 24, 'b4': 25, 'c4': 26, 'd4': 27, 'e4': 28, 'f4': 29, 'g4': 30, 'h4': 31,
           'A4': 24, 'B4': 25, 'C4': 26, 'D4': 27, 'E4': 28, 'F4': 29, 'G4': 30, 'H4': 31, 'a5': 32, 'b5': 33, 'c5': 34,
           'd5': 35, 'e5': 36, 'f5': 37, 'g5': 38, 'h5': 39, 'A5': 32, 'B5': 33, 'C5': 34, 'D5': 35, 'E5': 36, 'F5': 37,
           'G5': 38, 'H5': 39, 'a6': 40, 'b6': 41, 'c6': 42, 'd6': 43, 'e6': 44, 'f6': 45, 'g6': 46, 'h6': 47, 'A6': 40,
           'B6': 41, 'C6': 42, 'D6': 43, 'E6': 44, 'F6': 45, 'G6': 46, 'H6': 47, 'a7': 48, 'b7': 49, 'c7': 50, 'd7': 51,
           'e7': 52, 'f7': 53, 'g7': 54, 'h7': 55, 'A7': 48, 'B7': 49, 'C7': 50, 'D7': 51, 'E7': 52, 'F7': 53, 'G7': 54,
           'H7': 55, 'a8': 56, 'b8': 57, 'c8': 58, 'd8': 59, 'e8': 60, 'f8': 61, 'g8': 62, 'h8': 63, 'A8': 56, 'B8': 57,
           'C8': 58, 'D8': 59, 'E8': 60, 'F8': 61, 'G8': 62, 'H8': 63, '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5,
           '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, '11': 11, '12': 12, '13': 13, '14': 14, '15': 15, '16': 16,
           '17': 17, '18': 18, '19': 19, '20': 20, '21': 21, '22': 22, '23': 23, '24': 24, '25': 25, '26': 26, '27': 27,
           '28': 28, '29': 29, '30': 30, '31': 31, '32': 32, '33': 33, '34': 34, '35': 35, '36': 36, '37': 37, '38': 38,
           '39': 39, '40': 40, '41': 41, '42': 42, '43': 43, '44': 44, '45': 45, '46': 46, '47': 47, '48': 48, '49': 49,
           '50': 50, '51': 51, '52': 52, '53': 53, '54': 54, '55': 55, '56': 56, '57': 57, '58': 58, '59': 59, '60': 60,
           '61': 61, '62': 62, '63': 63}

FUNC_CACHE = {}
HAMMING_CACHE = {}
POSSIBLE_CACHE = {}
PLACE_CACHE = {}
TREE_CACHE = {}
FILL_CACHE = {}


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
    if n in HAMMING_CACHE:
        return HAMMING_CACHE[n]
    else:
        orig = n
        c = 0
        while n:
            c += 1
            n ^= n & -n
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
    key = (board[0] << 64) + board[1] + piece
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
    # if (b[0], b[1], piece, move) in PLACE_CACHE:
    #     return PLACE_CACHE[(b[0], b[1], piece, move)]
    # else:
    board = {0: b[0], 1: b[1]}
    board[piece] |= move

    for i in MASKS:
        c = fill(move, board[not piece], i)
        if c & board[piece] != 0:
            c = (c & MASKS[i * -1]) << i * -1 if i < 0 else (c & MASKS[i * -1]) >> i
            board[piece] |= c
            board[not piece] &= (FULL_BOARD - c)
    # PLACE_CACHE[(b[0], b[1], piece, move)] = board
    return board


def game_over(board, current):
    if board[current] | board[not current] == FULL_BOARD:
        return True
    player_moves = possible_moves(board, current)
    opponent_moves = possible_moves(board, not current)
    return True if len(player_moves) + len(opponent_moves) == 0 else player_moves


def minimax(board, piece, depth):
    """
    Returns the best value, [sequence of the previous best moves]
    """
    key = (board[0] << 65) + board[1] + piece
    if key in TREE_CACHE:
        return TREE_CACHE[key]

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
        TREE_CACHE[key] = (max_move, best_opp_moves + [best_move])
        return TREE_CACHE[key]
    else:
        min_move, best_move = 100, 0
        for i in current_moves:
            placed = place(board, piece, MOVES[i])
            tmp, opp_moves = minimax(placed, not piece, depth - 1)
            if tmp < min_move:
                min_move, best_move, best_opp_moves = tmp, i, opp_moves
        TREE_CACHE[key] = (min_move, best_opp_moves + [best_move])
        return TREE_CACHE[key]


def actual_best_move(board, moves, piece):
    best = []
    for move in moves:
        placed = place(board, piece, MOVES[move])
        val = minimax(placed, not piece, 12)
        best.append((val[0], move, val[1]))
    final = max(best, key=lambda x: x[0]) if piece else min(best, key=lambda x: x[0])
    return (final[0], final[2] + [final[1]]) if piece else (final[0] * -1, final[2] + [final[1]])


def main():
    string_board, piece = argv[1].upper(), argv[2].upper()
    board = {
        0: int(string_board.replace('.', '0').replace('O', '1').replace('X', '0'), 2),
        1: int(string_board.replace('.', '0').replace('O', '0').replace('X', '1'), 2)
    }
    piece = 0 if piece == 'O' else 1
    possible = possible_moves(board, piece)
    print(sorted(possible))
    if possible:
        print("Min score: {0}; move sequence: {1}".format(*actual_best_move(board, [*possible], piece)))


if __name__ == "__main__":
    start = time()
    main()
    print("{0}".format(time() - start))
