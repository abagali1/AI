#!/usr/bin/env python3
from sys import argv
from time import time as time

MASKS = {
    1: lambda x:  (x & 0xfefefefefefefefe) >> 1,
    -1: lambda x: (x & 0x7f7f7f7f7f7f7f7f) << 1,
    8: lambda x: x<<8,
    -8: lambda x: x>>8,
    9: lambda x: ((x & 0xfefefefefefefefe) >> 1)<<8,
    7: lambda x: ((x & 0x7f7f7f7f7f7f7f7f) << 1)<<8,
    -9: lambda x: ((x & 0x7f7f7f7f7f7f7f7f) << 1)>>8,
    -7: lambda x: ((x & 0xfefefefefefefefe) >> 1)>>8
}
MOVES = {i:1<<(63-i) for i in range(64)}
LOG = {MOVES[63-i]:i for i in range(64)}
CORNER_NEIGHBORS = {1:0, 6:7, 8:0, 9:0, 14:7, 15:7, 48:56, 49:56, 54:63, 55:63, 57:56, 62:63}
NEIGHBORS = {0: {8, 1}, 1: {0, 9, 2}, 2: {1, 10, 3}, 3: {2, 11, 4}, 4: {3, 12, 5}, 5: {4, 13, 6}, 6: {5, 14, 7}, 7: {6, 15}, 8: {16, 0, 9}, 9: {8, 17, 10, 1}, 10: {11, 9, 18, 2}, 11: {3, 10, 19, 12}, 12: {13, 11, 20, 4}, 13: {5, 12, 21, 14}, 14: {15, 13, 22, 6}, 15: {7, 14, 23}, 16: {24, 8, 17}, 17: {16, 25, 18, 9}, 18: {19, 17, 26, 10}, 19: {11, 18, 27, 20}, 20: {21, 19, 28, 12}, 21: {13, 20, 29, 22}, 22: {23, 21, 30, 14}, 23: {15, 22, 31}, 24: {32, 16, 25}, 25: {24, 33, 26, 17}, 26: {27, 25, 34, 18}, 27: {19, 26, 35, 28}, 28: {29, 27, 36, 20}, 29: {21, 28, 37, 30}, 30: {31, 29, 38, 22}, 31: {23, 30, 39}, 32: {40, 24, 33}, 33: {32, 41, 34, 25}, 34: {35, 42, 26, 33}, 35: {27, 34, 43, 36}, 36: {35, 37, 44, 28}, 37: {29, 36, 45, 38}, 38: {37, 39, 46, 30}, 39: {31, 38, 47}, 40: {48, 41, 32}, 41: {40, 49, 42, 33}, 42: {41, 50, 43, 34}, 43: {35, 42, 51, 44}, 44: {43, 52, 45, 36}, 45: {37, 44, 53, 46}, 46: {38, 45, 54, 47}, 47: {39, 46, 55}, 48: {56, 49, 40}, 49: {48, 57, 50, 41}, 50: {49, 58, 51, 42}, 51: {43, 50, 59, 52}, 52: {51, 60, 53, 44}, 53: {45, 52, 61, 54}, 54: {46, 53, 62, 55}, 55: {47, 54, 63}, 56: {48, 57}, 57: {56, 49, 58}, 58: {57, 50, 59}, 59: {58, 51, 60}, 60: {59, 52, 61}, 61: {60, 53, 62}, 62: {61, 54, 63}, 63: {62, 55}}
LETTERS = {'a1': 0, 'b1': 1, 'c1': 2, 'd1': 3, 'e1': 4, 'f1': 5, 'g1': 6, 'h1': 7, 'A1': 0, 'B1': 1, 'C1': 2, 'D1': 3, 'E1': 4, 'F1': 5, 'G1': 6, 'H1': 7, 'a2': 8, 'b2': 9, 'c2': 10, 'd2': 11, 'e2': 12, 'f2': 13, 'g2': 14, 'h2': 15, 'A2': 8, 'B2': 9, 'C2': 10, 'D2': 11, 'E2': 12, 'F2': 13, 'G2': 14, 'H2': 15, 'a3': 16, 'b3': 17, 'c3': 18, 'd3': 19, 'e3': 20, 'f3': 21, 'g3': 22, 'h3': 23, 'A3': 16, 'B3': 17, 'C3': 18, 'D3': 19, 'E3': 20, 'F3': 21, 'G3': 22, 'H3': 23, 'a4': 24, 'b4': 25, 'c4': 26, 'd4': 27, 'e4': 28, 'f4': 29, 'g4': 30, 'h4': 31, 'A4': 24, 'B4': 25, 'C4': 26, 'D4': 27, 'E4': 28, 'F4': 29, 'G4': 30, 'H4': 31, 'a5': 32, 'b5': 33, 'c5': 34, 'd5': 35, 'e5': 36, 'f5': 37, 'g5': 38, 'h5': 39, 'A5': 32, 'B5': 33, 'C5': 34, 'D5': 35, 'E5': 36, 'F5': 37, 'G5': 38, 'H5': 39, 'a6': 40, 'b6': 41, 'c6': 42, 'd6': 43, 'e6': 44, 'f6': 45, 'g6': 46, 'h6': 47, 'A6': 40, 'B6': 41, 'C6': 42, 'D6': 43, 'E6': 44, 'F6': 45, 'G6': 46, 'H6': 47, 'a7': 48, 'b7': 49, 'c7': 50, 'd7': 51, 'e7': 52, 'f7': 53, 'g7': 54, 'h7': 55, 'A7': 48, 'B7': 49, 'C7': 50, 'D7': 51, 'E7': 52, 'F7': 53, 'G7': 54, 'H7': 55, 'a8': 56, 'b8': 57, 'c8': 58, 'd8': 59, 'e8': 60, 'f8': 61, 'g8': 62, 'h8': 63, 'A8': 56, 'B8': 57, 'C8': 58, 'D8': 59, 'E8': 60, 'F8': 61, 'G8': 62, 'H8': 63, '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, '11': 11, '12': 12, '13': 13, '14': 14, '15': 15, '16': 16, '17': 17, '18': 18, '19': 19, '20': 20, '21': 21, '22': 22, '23': 23, '24': 24, '25': 25, '26': 26, '27': 27, '28': 28, '29': 29, '30': 30, '31': 31, '32': 32, '33': 33, '34': 34, '35': 35, '36': 36, '37': 37, '38': 38, '39': 39, '40': 40, '41': 41, '42': 42, '43': 43, '44': 44, '45': 45, '46': 46, '47': 47, '48': 48, '49': 49, '50': 50, '51': 51, '52': 52, '53': 53, '54': 54, '55': 55, '56': 56, '57': 57, '58': 58, '59': 59, '60': 60, '61': 61, '62': 62, '63': 63}
FUNC_CACHE = {}
HAMMING_CACHE = {}


bit_not = lambda x: 0xffffffffffffffff - x
is_on = lambda x, pos: x & MOVES[63-pos]

binary_to_board = lambda board: "".join(['o' if is_on(board[0], 63-i) else 'x' if is_on(board[1],63-i) else '.' for i in range(64)])

board_to_string = lambda x: '\n'.join([''.join([x[i*8+j]][0] for j in range(8)) for i in range(8)]).strip().lower()
binary_to_string = lambda x: '\n'.join([''.join(['{:064b}'.format(x)[i*8 +j][0] for j in range(8)]) for i in range(8)]).strip().lower()

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
            HAMMING_CACHE[n] = 1+hamming_weight(n-(n&-n))
        return HAMMING_CACHE[n]


def fill(current, opponent, direction):
    mask = MASKS[direction]
    w = mask(current) & opponent
    w |= mask(w) & opponent
    w |= mask(w) & opponent
    w |= mask(w) & opponent
    w |= mask(w) & opponent
    w |= mask(w) & opponent
    return mask(w) 


def possible_moves(board, piece):
    final = 0b0
    possible = set()
    for d in MASKS:
        final |= fill(board[piece], board[not piece], d) & (0xffffffffffffffff - (board[piece]|board[not piece]))
    while final:
        b = final & -final
        possible.add(63-LOG[b])
        final -= b
    return possible 


def place(b, piece, move):
    board = {0: b[0], 1:b[1]}
    board[piece] |= move

    for i in MASKS:
        c = fill(move, board[not piece], i)
        if c&board[piece] != 0:
            c = MASKS[i*-1](c)
            board[piece] |= c
            board[not piece] &= bit_not(c)
    return board


def coin_heuristic(board, move, piece):
    placed = place(board,piece,move)
    num_player = hamming_weight(placed[piece])
    num_opp = hamming_weight(placed[not piece])
    return 100*((num_player - num_opp)/(num_player + num_opp))


def mobility_heuristic(board, move, piece):
    tmp = place(board, piece, move)
    opponent = possible_moves(tmp, not piece)
    h = -len(opponent)
    for opp_move in opponent:
        h += len(possible_moves(place(tmp, not piece, opp_move), piece))
    return h


def next_to_corner(board, move, piece):
    """
    Return 10 if next to a captured(own) corner
    Return 0 if not next to a corner
    Return -10 if next to an empty/taken(opponent) corner
    """
    if move not in CORNER_NEIGHBORS:
        return 0
    elif is_on(board[piece], CORNER_NEIGHBORS[move]):
        return 10
    return -10


def stable_edge(board, move, piece):
    """
    Return 10 if connected to a stable edge
    Return 0 otherwise
    """
    return 0


def best_move(board, moves, piece):
    print("My move is {0}".format([*moves][0]))

    strat = coin_heuristic if hamming_weight(bit_not(board[0]|board[1])) <= 8 else mobility_heuristic

    best = ([*moves][0], -1000000)
    for move in moves:
        if 0 in moves:
            print("My move is 0")
            return
        elif 7 in moves:
            print("My move is 7")
            return
        elif 56 in moves:
            print("My move is 56")
            return
        elif 63 in moves:
            print("My move is 63")
            return

        actual_move = MOVES[move]
        h = strat(board, actual_move, piece)

        h += next_to_corner(board, actual_move, piece)
        h += stable_edge(board, actual_move, piece)

        best = max((move, h), best, key=lambda x: x[1])
    
    print("My move is {0}".format(best[0]))
    

def main():
    string_board, piece = argv[1].upper(), argv[2].upper()
    board = {
        0: int(string_board.replace('.','0').replace('O','1').replace('X','0'),2),
        1: int(string_board.replace('.','0').replace('O','0').replace('X','1'),2)
    }
    piece = 0 if piece == 'O' else 1
    possible = possible_moves(board, piece)
    if len(possible) > 0:
        best_move(board, possible, piece)
    
    
if __name__ == "__main__":
    start = time() 
    main()
    #print("{0}".format(time()-start))