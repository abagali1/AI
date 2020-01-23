#!/usr/bin/env python3
from sys import argv
from time import time 

FULL_BOARD = 0xffffffffffffffff
RIGHT_MASK = 0xfefefefefefefefe
LEFT_MASK =0x7f7f7f7f7f7f7f7f
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


MOVES = {i: 1 << (63 - i) for i in range(64)}
POS = {MOVES[63 - i]: 63 - i for i in range(64)}


HAMMING_CACHE = {}
POSSIBLE_CACHE = {(68853694464, 34628173824, 0): {34, 43, 20, 29}, (68853694464, 34628173824, 1): {26, 19, 44, 37}}
TREE_CACHE = {}


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
        possible = set()
        for d in MASKS:
            final |= fill(board[piece], board[not piece], d) & (FULL_BOARD ^ (board[piece] | board[not piece]))
        while final:
            b = final & -final
            possible.add(POS[b])
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
            board[not piece] &= (FULL_BOARD - c)
    return board


def game_over(board, current):
    if not (FULL_BOARD ^ (board[current]|board[not current])):
        return True
    player_moves = possible_moves(board, current)
    opponent_moves = possible_moves(board, not current)
    pm = len(player_moves)
    return True if (pm|len(opponent_moves))==0 else (player_moves, pm)


def minimax(board, piece, depth, alpha, beta, possible=[]):
    """
    Returns the best value, [sequence of the previous best moves]
    """
    key = (board[0], board[1], piece, alpha, beta)
    if key in TREE_CACHE:
        return TREE_CACHE[key]

    if not possible:
        state = game_over(board, piece)
        if (board[piece]|board[1^piece]) == FULL_BOARD:
            return hamming_weight(board[1]) - hamming_weight(board[0]), []
        else:
            current_moves, length = state

        if length == 0:
            val = minimax(board, 1^piece, depth, alpha, beta)
            TREE_CACHE[key] = (val[0], val[1]+[-1])
            return TREE_CACHE[key]
    else:
        current_moves = sorted(possible, key=lambda x: len(possible_moves(place(board, piece, MOVES[x]), 1^piece)))
    
    best_opp_moves = []
    if piece:
        max_move, best_move = -100, 0
        for i in current_moves:
            placed = place(board, piece, MOVES[i])
            tmp, opp_moves = minimax(placed, 1^piece, depth - 1, alpha, beta)
            if tmp > max_move:
                max_move, best_move, best_opp_moves = tmp, i, opp_moves
            alpha = max(max_move, alpha)
            if beta <= alpha:
                break
        TREE_CACHE[key] = (max_move, best_opp_moves + [best_move])
        return TREE_CACHE[key]
    else:
        min_move, best_move = 100, 0
        for i in current_moves:
            placed = place(board, piece, MOVES[i])
            tmp, opp_moves = minimax(placed, 1^piece, depth - 1, alpha, beta)
            if tmp < min_move:
                min_move, best_move, best_opp_moves = tmp, i, opp_moves
            beta = min(min_move, beta)
            if beta <= alpha:
                break
        TREE_CACHE[key] = (min_move, best_opp_moves + [best_move])
        return TREE_CACHE[key]


def actual_best_move(board, moves, piece):
    val = minimax(board, piece, 12, -10000, 10000, possible=sorted(moves, key=lambda x: len(possible_moves(place(board, piece, MOVES[x]), not piece))))
    print("Min score: {0}; move sequence: {1}".format(val[0], val[1]) if piece else "Min score: {0}; move sequence: {1}".format(val[0]*-1, val[1]))

def main():
    string_board, piece = argv[1].upper(), argv[2].upper()
    board = string_to_board(string_board)
    piece = 0 if piece == 'O' else 1
    possible = possible_moves(board, piece)
    if possible:
        actual_best_move(board, possible, piece)


if __name__ == "__main__":
    start = time()
    main()
    print("{0}".format(time() - start))
