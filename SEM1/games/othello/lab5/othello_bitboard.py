#!/usr/bin/env python3
from sys import argv
from time import time as time
from re import compile, IGNORECASE, match

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
STABLE_EDGE_REGEX = {
    1: compile(r"\.|\.$|^x+o*\.|\.o*x+", IGNORECASE),
    0: compile(r"\.|\.$|^o+x*\.|\.x*o+", IGNORECASE)
}
MOVES = {i:1<<(63-i) for i in range(64)}
LOG = {MOVES[63-i]:i for i in range(64)}
FULL_BOARD = 0xffffffffffffffff

CORNERS = {0, 7, 56, 63}
CORNER_NEIGHBORS = {1:63, 6:56, 8:63, 9:63, 14:56, 15:56, 48:7, 49:7, 54:0, 55:0, 57:7, 62:0}
COL_EDGES =  {1:{7,15,23,31,39,47,55,63}, 0:{0,8,16,24,32,40,48,56}}
ROW_EDGES = {0: {0,1,2,3,4,5,6,7}, 1:{56,57,58,59,60,61,62,6}}


EDGES = {0: {0,1,2,3,4,5,6,7}, 1:{56,57,58,59,60,61,62,6}, 2:{7,15,23,31,39,47,55,63}, 3:{0,8,16,24,32,40,48,56}}

FUNC_CACHE = {}
HAMMING_CACHE = {}
PLAYER, OPPONENT = 0,0


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


def game_state(board):
    num_player = hamming_weight(board[PLAYER])
    num_opp = hamming_weight(board[OPPONENT])
    if num_player > num_opp:
        return 10
    elif num_player == num_opp:
        return 0
    else:
        return -10


def minimax(board, piece, depth, is_max):
    state = game_state(board)
    if state == 10 or state == -10:
        return state
    if hamming_weight(board[0]|board[1]) == 64:
        return 0
    
    if is_max:
        maxx = -100
        for i in possible(board, piece):
            placed = place(board, piece, i)
            maxx = max(maxx, minimax(placed, not piece, depth+1, False))
        return maxx
    else:
        minn = 100
        for i in possible_moves(board, piece):
            placed = place(board, piece, i)
            minn = min(minn, minimax(placed, not piece, depth+1, True))
        return minn


def actual_best_move(board, moves, piece):
    best = (-10000, move[0])
    for move in moves[1:]:
        placed = place(board, piece, move)
        val = minimax(placed, not piece, 0, False)
        best = max(best, (val, move))
    




def main():
    global PLAYER, OPPONENT
    string_board, piece = argv[1].upper(), argv[2].upper()
    board = {
        0: int(string_board.replace('.','0').replace('O','1').replace('X','0'),2),
        1: int(string_board.replace('.','0').replace('O','0').replace('X','1'),2)
    }
    piece = 0 if piece == 'O' else 1
    PLAYER = piece
    OPPONENT = not piece
    possible = possible_moves(board, piece)
    num_empty = hamming_weight(bit_not(board[0]|board[1]))
    if len(possible) > 0:
        print(actual_best_move(board, [*possible], piece))
    
    
if __name__ == "__main__":
    start = time() 
    main()
    #print("{0}".format(time()-start))
