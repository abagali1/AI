#!/usr/bin/env python3
from sys import argv
from time import time 

FULL_BOARD = 0xffffffffffffffff
RIGHT_MASK = 0xfefefefefefefefe
LEFT_MASK = 0x7f7f7f7f7f7f7f7f
CORNER_BOARD = 0x8100000000000081
CORNER_NEIGHBORS = 0x42c300000000c342
CORNERS = {0, 7, 56, 63}
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
          4, -3, -3, 2, 2, 2, 2, -3, 4
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
        possible, count = [], 0
        for d in MASKS:
            final |= fill(board[piece], board[1^piece], d) & (FULL_BOARD ^ (board[piece] | board[not piece]))
        while final:
            b = final & -final
            possible.append(POS[b])
            final ^= b
            count += 1
        POSSIBLE_CACHE[key] = (possible, count)
        return possible, count


def place(b, piece, move):
    board = {0: b[0], 1: b[1]}
    board[piece] |= move

    for i in MASKS:
        c = fill(move, board[not piece], i)
        if c & board[piece] != 0:
            c = (c & MASKS[i * -1]) << i * -1 if i < 0 else (c & MASKS[i * -1]) >> i
            board[piece] |= c
            board[1^piece] &= (FULL_BOARD ^ c)
    return board


def weight_table(board):
    h = 0
    while(board):
        b = board&-board
        h += WEIGHT_TABLE[LOG[b]]
        board ^= b
    return h


def heuristic(board, current, opponent):
    c = hamming_weight(board[current])
    o = hamming_weight(board[opponent])
    return 100*((c-o)/(c+o))


def endgame_negamax(board, current, depth, alpha, beta, possible=[]):
    opponent = 1^current
    if not possible:
        (current_moves, length), (opponent_moves, opponent_length) = possible_moves(board, current), possible_moves(board, opponent)
        if not (FULL_BOARD ^ (board[1]|board[0])) or (length|opponent_length)==0 or depth==0:
            return hamming_weight(board[current])-hamming_weight(board[opponent]),0
        if length==0 and opponent_length!=0:
            val = endgame_negamax(board, opponent, depth, -beta, -alpha)
            return -val[0], val[1]
        current_moves = sorted(current_moves, key=lambda x: len(possible_moves(place(board, current, MOVES[x]), opponent)))
    else:
        current_moves = possible

    best_score, best_move = -100, current_moves[0]
    for move in current_moves:
        score = -endgame_negamax(place(board, current, MOVES[move]), opponent, depth-1, -beta, -alpha)[0]
        if score > best_score:
            best_score = score
            best_move = move
        alpha = max(alpha, score)
        if beta <= alpha:
            break
    return best_score, best_move


def endgame(board, moves, piece, empty):
    sorted_moves = sorted(moves, key=lambda x: len(possible_moves(place(board, piece, MOVES[x]), 1^piece)))
    val = endgame_negamax(board, piece, 12, -1000, 1000, possible=sorted_moves)
    print("My move is {0}".format(val[1]))


def minimax_with_memory(board, current, alpha, beta, depth):
    opponent = 1^current
    key = (board[1], board[0], current)
    if key in TREE_CACHE:
        cached_score, cached_depth, lower_bound, upper_bound = TREE_CACHE[key]
        if cached_depth >= depth:
            if lower_bound >= beta:
                return lower_bound
            if upper_bound <= alpha:
                return upper_bound
            alpha, beta = max(alpha, lower_bound), min(beta, upper_bound)
    
    (current_moves, length), (opponent_moves, opponent_length) = possible_moves(board, current), possible_moves(board, opponent)


    if not (FULL_BOARD ^ (board[0]|board[1])) or (length|opponent_length)==0 or depth==0:
        return hamming_weight(board[1])-hamming_weight(board[0])
    
    if length==0 and opponent_length!=0:
        return minimax_with_memory(board, opponent, depth, alpha, beta)
    
    if current:
        g, a = -float('inf'), alpha
        for move in current_moves:
            if g<=beta:
                break
            g = max(g, minimax_with_memory(place(board, current, MOVES[move]), opponent, a, beta, depth-1))
            a = max(a, g)

    else:
        g, b = float('inf'), beta
        for move in current_moves:
            if g>=alpha:
                break
            g = min(g, minimax_with_memory(place(board, current, MOVES[move]), opponent, alpha, b, depth-1))
            b = min(b, g)

    if g <= alpha:
        TREE_CACHE[key] = (g, depth, alpha, g)
    elif alpha < g < beta:
        TREE_CACHE[key] = (g, depth, g, g)
    elif g >= beta:
        TREE_CACHE[key] = (g, depth, g, beta)
    return g


def mtdf(board, piece, first_guess, depth):
    g = first_guess
    upper_bound = 100000000
    lower_bound = -upper_bound
    while True:
        if g == lower_bound:
            beta = g+1
        else:
            beta = g
        g = minimax_with_memory(board, piece, beta-1, beta, depth)
        if g < beta:
            upper_bound = g
        else:
            lower_bound = g
        if lower_bound >= upper_bound:
            break
    return g



def midgame(board, moves, piece, empty):
    first_guess = 0
    for move in moves:
        first_guess = mtdf(place(board, piece, MOVES[move]), 1^piece, first_guess, 12)
        print(first_guess, move)



def main():
    string_board, piece = argv[1].upper(), argv[2].upper()
    board = string_to_board(string_board)
    piece = 0 if piece == 'O' else 1
    possible = possible_moves(board, piece)
    num_empty = hamming_weight(FULL_BOARD ^ (board[0]|board[1]))
    print(possible)
    if possible:
        if num_empty >= 14:
            midgame(board, possible, piece, num_empty)
        else:
            endgame(board, possible, piece, num_empty)

if __name__ == "__main__":
    start = time()
    main()
    print(time()-start)