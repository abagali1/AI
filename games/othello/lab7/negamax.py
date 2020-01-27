#!/usr/bin/env python3
from sys import argv
from time import time 

FULL_BOARD = 0xffffffffffffffff
RIGHT_MASK = 0xfefefefefefefefe
LEFT_MASK = 0x7f7f7f7f7f7f7f7f
CORNER_BOARD = 0x8100000000000081
CORNER_NEIGHBORS = 0x42c300000000c342
MASKS = {
    -1: RIGHT_MASK,
    1: LEFT_MASK,
    8: FULL_BOARD,
    -8: FULL_BOARD,
    7: RIGHT_MASK,
    9: LEFT_MASK,
    -7: LEFT_MASK,
    -9: RIGHT_MASK
}

WEIGHT_TABLE = [4, -3, 2, 2, 2, 2, -3, 4,
          -3, -4, -1, -1, -1, -1, -4, -3,
           2, -1, 1, 0, 0, 1, -1, 2,
           2, -1, 0, 1, 1, 0, -1, 2,
           2, -1, 0, 1, 1, 0, -1, 2,
           2, -1, 1, 0, 0, 1, -1, 2,
          -3, -4, -1, -1, -1, -1, -4,
          -3, 4, -3, 2, 2, 2, 2, -3, 4
          ]

MOVES = {i: 1 << (63^i) for i in range(64)}
POS = {MOVES[63^i]: 63^i for i in range(64)}
LOG = {MOVES[63^i]:i for i in range(64)}


HAMMING_CACHE = {}
POSSIBLE_CACHE = {(68853694464, 34628173824, 0): {34, 43, 20, 29}, (68853694464, 34628173824, 1): {26, 19, 44, 37}}
TREE_CACHE = {}
WEIGHT_CACHE = {}


def string_to_board(board):
    return {
        0: int(board.replace(".","0").replace("O","1").replace("X","0"),2),
        1: int(board.replace(".","0").replace("O","0").replace("X","1"),2)
    }

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
    direction *= -1
    w = ((current & mask) >> direction) & opponent
    w |= ((w & mask) >> direction) & opponent
    w |= ((w & mask) >> direction) & opponent
    w |= ((w & mask) >> direction) & opponent
    w |= ((w & mask) >> direction) & opponent
    w |= ((w & mask) >> direction) & opponent
    return (w & mask) >> direction


def possible_moves(board, piece):
    key = (board[0], board[1], piece)
    if key in POSSIBLE_CACHE:
        return POSSIBLE_CACHE[key]
    else:
        final = 0b0
        possible = []
        for d in MASKS:
            final |= fill(board[piece], board[1^piece], d) & (FULL_BOARD ^ (board[piece] | board[not piece]))
        while final:
            b = final & -final
            possible.append(POS[b])
            final ^= b
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
            board[1^piece] &= (FULL_BOARD - c)
    return board


def weight_table(board):
    h = 0
    while(board):
        b = board&-board
        h += WEIGHT_TABLE[LOG[b]]
        board ^= b
    return h


def heuristic(board, current, opponent, current_moves, current_length, opponent_moves, opponent_length):
    h = -20*board[opponent]
    
    current_corners = board[current] & CORNER_BOARD
    opponent_corners = board[opponent] & CORNER_BOARD
    if current_corners:
        h += 30*hamming_weight(current_corners)
    if opponent_corners: 
        h -= 50*hamming_weight(opponent_corners)
    

    current_corner_neighbors = board[current] & CORNER_NEIGHBORS
    opponent_corner_neighbors = board[opponent] & CORNER_NEIGHBORS

    if current_corner_neighbors:
        h -= 30*hamming_weight(current_corner_neighbors)
    if opponent_corner_neighbors:
        h += 30*hamming_weight(opponent_corner_neighbors)

    h += hamming_weight(board[current])-hamming_weight(board[opponent])
    
    
    h += weight_table(board[current])*20
    h -= weight_table(board[opponent])*20
    return h


def negamax(board, current, depth, alpha, beta, empty, possible=[]):
    opponent = 1^current

    if not possible:
        current_moves, opponent_moves = possible_moves(board, current), possible_moves(board, opponent)
        length, opponent_length = len(current_moves), len(opponent_moves)
        if not (FULL_BOARD ^ (board[current]|board[opponent])) or (length|opponent_length)==0:
            return hamming_weight(board[current])-hamming_weight(board[opponent])*100,0
        if length==0 and opponent_length!=0:
            val = negamax(board, opponent, depth, -beta, -alpha, empty)
            return -val[0], val[1]
        if depth==0:
            return heuristic(board, current, opponent, current_moves, length, opponent_moves, opponent_length), 0
    else:
        current_moves = possible


    best_score, best_move = -100, current_moves[0]
    for move in current_moves:
        score = -negamax(place(board, current, MOVES[move]), opponent, depth-1, -beta, -alpha, empty-1)[0]
        if score > best_score:
            best_score = score
            best_move = move
        alpha = max(alpha, score)
        if beta <= alpha:
            break
    return best_score, best_move


def endgame(board, moves, piece, empty):
    sorted_moves = sorted(moves, key=lambda x: len(possible_moves(place(board, piece, MOVES[x]), 1^piece)))
    val = negamax(board, piece, 12, -1000, 1000, empty, possible=sorted_moves)
    print("My move is {0}".format(val[1]))

def midgame(board, moves, piece, empty):
    print(moves)
    sorted_moves = sorted(moves, key=lambda x: len(possible_moves(place(board, piece, MOVES[x]), 1^piece)))
    best = (-1000, 0)
    for max_depth in range(3,50):
        val = negamax(board, piece, max_depth, -1000, 1000, empty, possible=sorted_moves)
        best = max(val, best)
        print("My move is {0}".format(best[1]))


def main():
    string_board, piece = argv[1].upper(), argv[2].upper()
    board = string_to_board(string_board)
    piece = 0 if piece == 'O' else 1
    possible = possible_moves(board, piece)
    num_empty = hamming_weight(FULL_BOARD ^ (board[0]|board[1]))
    if possible:
        if num_empty >= 14:
            midgame(board, possible, piece, num_empty)
        else:
            endgame(board, possible, piece, num_empty)

if __name__ == "__main__":
    start = time()
    main()
    print(time()-start)