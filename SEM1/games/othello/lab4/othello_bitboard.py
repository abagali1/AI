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

CORNER_NEIGHBORS = {1:0, 6:7, 8:0, 9:0, 14:7, 15:7, 48:56, 49:56, 54:63, 55:63, 57:56, 62:63}
COL_EDGES =  {1:{7,15,23,31,39,47,55,63}, 0:{0,8,16,24,32,40,48,56}}
ROW_EDGES = {0: {0,1,2,3,4,5,6,7}, 1:{56,57,58,59,60,61,62,6}}


EDGES = {0: {0,1,2,3,4,5,6,7}, 1:{56,57,58,59,60,61,62,6}, 2:{7,15,23,31,39,47,55,63}, 3:{0,8,16,24,32,40,48,56}}

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
    return ((num_player-num_opp)/(num_player+num_opp)) * 100


def mobility_heuristic(board, move, piece):
    return -len(possible_moves(place(board, piece, move), not piece))*10


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
    return -100


# def stable_edge(b, move, piece):
#     """
#     Return 10 if connected to a stable edge
#     Return 0 otherwise
#     """
#     placed = place(b,piece,move)

#     if move in ROW_EDGES[0]:
#         num_tokens = move
#         l = int("1"*num_tokens,2)
#         r = (l << 8-num_tokens)
#         row = get_row(placed[piece],0)
#         if (row & l) == l or (row & r)==r:
#             return 10
#     elif move in ROW_EDGES[1]:
#         num_tokens = 64-move
#         l = int("1"*(64-move),2)
#         r = (l << (8-num_tokens))
#         row = get_row(placed[piece],7)
#         if (row & l) == l or (row & r)==r:
#             return 10
#     elif move in COL_EDGES[0]:
#         num_tokens = (56-move)//8
#         l = int("1"*(num_tokens), 2)
#         r = (l << (8-num_tokens))
#         col = get_col(placed[piece], 0)
#         if (col & l) == l or (col & r) == r:
#             return 10
#     elif move in COL_EDGES[1]:
#         num_tokens = (63-move)//8
#         l = int("1"*(num_tokens), 2)
#         r = (1 << (8-num_tokens))
#         col = get_col(placed[piece], 0)
#         if (col & l) == 1 or (col & r) == r:
#             return 10
#     return 0


def stable_edge(board, move, piece):
    bs = binary_to_board(place(board, piece, move))
    token = 'X' if piece else 'O'
    for edge in EDGES:
        if move not in EDGES[edge]:
            continue
        con = "".join([bs[x] for x in EDGES[edge]])
        if con == token*8:
            return 100
        if STABLE_EDGE_REGEX[piece].match(con):
            return 100
    return 0
        

def best_move(board, moves, piece):
    init = [*moves][0]
    print("My move is {0}".format(init))
    actual_move = MOVES[init]
    moves.remove(init)

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


    strat = coin_heuristic if hamming_weight(bit_not(board[0]|board[1])) <= 8 else mobility_heuristic
    h = strat(board, actual_move, piece) + next_to_corner(board, actual_move, piece) + stable_edge(board, actual_move, piece)
    best = (h, init)
    for move in moves:
        actual_move = MOVES[move]
        h = strat(board, actual_move, piece)
        h += next_to_corner(board, actual_move, piece)
        h += stable_edge(board, actual_move, piece)
        best = max((h, move), best)
    print("My move is {0}".format(best[1]))
    

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
