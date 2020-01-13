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
NEIGHBORS = {0: {8, 1}, 1: {0, 9, 2}, 2: {1, 10, 3}, 3: {2, 11, 4}, 4: {3, 12, 5}, 5: {4, 13, 6}, 6: {5, 14, 7}, 7: {6, 15}, 8: {16, 0, 9}, 9: {8, 17, 10, 1}, 10: {11, 9, 18, 2}, 11: {3, 10, 19, 12}, 12: {13, 11, 20, 4}, 13: {5, 12, 21, 14}, 14: {15, 13, 22, 6}, 15: {7, 14, 23}, 16: {24, 8, 17}, 17: {16, 25, 18, 9}, 18: {19, 17, 26, 10}, 19: {11, 18, 27, 20}, 20: {21, 19, 28, 12}, 21: {13, 20, 29, 22}, 22: {23, 21, 30, 14}, 23: {15, 22, 31}, 24: {32, 16, 25}, 25: {24, 33, 26, 17}, 26: {27, 25, 34, 18}, 27: {19, 26, 35, 28}, 28: {29, 27, 36, 20}, 29: {21, 28, 37, 30}, 30: {31, 29, 38, 22}, 31: {23, 30, 39}, 32: {40, 24, 33}, 33: {32, 41, 34, 25}, 34: {35, 42, 26, 33}, 35: {27, 34, 43, 36}, 36: {35, 37, 44, 28}, 37: {29, 36, 45, 38}, 38: {37, 39, 46, 30}, 39: {31, 38, 47}, 40: {48, 41, 32}, 41: {40, 49, 42, 33}, 42: {41, 50, 43, 34}, 43: {35, 42, 51, 44}, 44: {43, 52, 45, 36}, 45: {37, 44, 53, 46}, 46: {38, 45, 54, 47}, 47: {39, 46, 55}, 48: {56, 49, 40}, 49: {48, 57, 50, 41}, 50: {49, 58, 51, 42}, 51: {43, 50, 59, 52}, 52: {51, 60, 53, 44}, 53: {45, 52, 61, 54}, 54: {46, 53, 62, 55}, 55: {47, 54, 63}, 56: {48, 57}, 57: {56, 49, 58}, 58: {57, 50, 59}, 59: {58, 51, 60}, 60: {59, 52, 61}, 61: {60, 53, 62}, 62: {61, 54, 63}, 63: {62, 55}}


CORNER_NEIGHBORS = {1:0, 6:7, 8:0, 9:0, 14:7, 15:7, 48:56, 49:56, 54:63, 55:63, 57:56, 62:63}
COL_EDGES =  {1:{7,15,23,31,39,47,55,63}, 0:{0,8,16,24,32,40,48,56}}
ROW_EDGES = {0: {0,1,2,3,4,5,6,7}, 1:{56,57,58,59,60,61,62,6}}


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


def get_col(board, col):
    return ((((board << col) & 0x8080808080808080) * 0x2040810204081)>>56) & 0xff


def get_row(board, row):
    return (board >> 8*(7-row)) & 0xff


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
    possible = []
    for d in MASKS:
        final |= fill(board[piece], board[not piece], d) & (0xffffffffffffffff - (board[piece]|board[not piece]))
    while final:
        b = final & -final
        possible.append(63-LOG[b])
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
    return -len(possible_moves(place(board, piece, move), not piece))*100


def next_to_corner(board, move, piece):
    """
    Return 10 if next to a captured(own) corner
    Return 0 if not next to a corner
    Return -10 if next to an empty/taken(opponent) corner
    """

    if is_on(board[piece], CORNER_NEIGHBORS[move]):
        return True
    return False


def stable_edge(b, move, piece):
    """
    Return 10 if connected to a stable edge
    Return 0 otherwise
    """
    placed = place(b,piece,move)

    if move in ROW_EDGES[0]:
        num_tokens = move
        l = int("1"*num_tokens,2)
        r = (l << 8-num_tokens)
        row = get_row(placed[piece],0)
        if (row & l) == l or (row & r)==r:
            return 100000
    elif move in ROW_EDGES[1]:
        num_tokens = 64-move
        l = int("1"*(64-move),2)
        r = (l << (8-num_tokens))
        row = get_row(placed[piece],7)
        if (row & l) == l or (row & r)==r:
            return 100000
    elif move in COL_EDGES[0]:
        num_tokens = (56-move)//8
        l = int("1"*(num_tokens), 2)
        r = (l << (8-num_tokens))
        col = get_col(placed[piece], 0)
        if (col & l) == l or (col & r) == r:
            return 100000
    elif move in COL_EDGES[1]:
        num_tokens = (63-move)//8
        l = int("1"*(num_tokens), 2)
        r = (1 << (8-num_tokens))
        col = get_col(placed[piece], 0)
        if (col & l) == 1 or (col & r) == r:
            return 100000
    return 0


def best_move(board, moves, piece):
    print("My move is {0}".format([*moves][0]))

    for x in [0, 7, 56, 63]:
       if x in moves:
           return x 

    for move in moves:
        if move in CORNER_NEIGHBORS:
            if next_to_corner(board, move, piece):
                return move
            else:
                if len(moves) != 0:
                    moves.remove(move)

    if hamming_weight(bit_not(board[0]|board[1])) == 8:
        return max(moves, key=lambda x: coin_heuristic(board, MOVES[x], piece))
    else:
        return min(moves, key=lambda x: len(possible_moves(place(board, piece, MOVES[x]), not piece)))

    

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
