#!/usr/bin/env python3
from sys import argv
from time import time
from re import compile, IGNORECASE, match


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
STABLE_EDGE_REGEX = {
    1: compile(r"^x+[o.]*x+$", IGNORECASE),
    0: compile(r"^o+[x.]*o+", IGNORECASE)
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

bit_not = lambda x: FULL_BOARD ^ x
is_on = lambda x, pos: x & MOVES[63^pos]
binary_to_board = lambda board: "".join(['o' if is_on(board[0], 63^i) else 'x' if is_on(board[1],63^i) else '.' for i in range(64)])


CORNERS = {0, 7, 56, 63}
CORNER_NEIGHBORS = {1:63, 6:56, 8:63, 9:63, 14:56, 15:56, 48:7, 49:7, 54:0, 55:0, 57:7, 62:0}
COL_EDGES =  {1:{7,15,23,31,39,47,55,63}, 0:{0,8,16,24,32,40,48,56}}
ROW_EDGES = {0: {0,1,2,3,4,5,6,7}, 1:{56,57,58,59,60,61,62,6}}
EDGES = {0: {0,1,2,3,4,5,6,7}, 1:{56,57,58,59,60,61,62,6}, 2:{7,15,23,31,39,47,55,63}, 3:{0,8,16,24,32,40,48,56}}


HAMMING_CACHE = {}
POSSIBLE_CACHE = {(68853694464, 34628173824, 0): ({34, 43, 20, 29},4), (68853694464, 34628173824, 1): ({26, 19, 44, 37},4)}
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
            final |= fill(board[piece], board[not piece], d) & (FULL_BOARD ^ (board[piece] | board[not piece]))
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
            board[not piece] &= (FULL_BOARD ^ c)
    return board


def weight_table(board):
    h = 0
    while(board):
        b = board&-board
        h += WEIGHT_TABLE[LOG[b]]
        board ^= b
    return h

def coin_heuristic(board, move, piece): # MAX: 100 MIN: -100
    placed = place(board,piece,move)
    num_player = hamming_weight(placed[piece])
    num_opp = hamming_weight(placed[1^piece])
    return (num_player-num_opp)*20


def mobility_heuristic(board, move, piece): # MAX: 0 MIN: -340
    placed = place(board, piece, move)
    opp_moves, opp_length = possible_moves(placed, not piece)
    h = -opp_length*40
    if any(map(lambda x: x in CORNERS, opp_moves)):
        h -= 100000
    return h


def next_to_corner(board, move, piece): # MAX: 150 MIN: -100000
    """
    Return 10 if next to a captured(own) corner
    Return 0 if not next to a corner
    Return -10 if next to an empty/taken(opponent) corner
    """
    if move not in CORNER_NEIGHBORS:
        return 0
    elif is_on(board[piece], CORNER_NEIGHBORS[move]):
        return 600
    return -1000000


def stable_edge(board, move, piece):
    h = 0
    bs = binary_to_board(place(board, piece, move))
    token = 'X' if piece else 'O'
    for edge in EDGES:
        if move not in EDGES[edge]:
            continue
        con = "".join([bs[x] for x in EDGES[edge]])
        if con == token*8:
            h =  3200
        if STABLE_EDGE_REGEX[piece].match(con) is not None:
            h =  2400
    return h


def evaluate_move(board, move, piece, empty):
    actual_move = MOVES[move]
    h = mobility_heuristic(board, actual_move, piece)
    h += coin_heuristic(board, actual_move, piece)
    h += next_to_corner(board, move, piece)
    h += stable_edge(board, move, piece)

    return h


def heuristic(board, current, x_moves, x_length, o_moves, o_length):
    h = 20*x_length - 20*o_length

    h += 20*hamming_weight(board[1] & CORNER_BOARD)
    h -= 20*hamming_weight(board[0] & CORNER_BOARD)

    h += hamming_weight(board[1])-hamming_weight(board[0])
    
    h += weight_table(board[1])*20
    h -= weight_table(board[0])*20
    return h


def midgame_minimax(board, piece, depth, alpha, beta, empty, possible=[]):
    """
    Returns the best value, [sequence of the previous best moves]
    """

    opponent = 1^piece
    if not possible:
        (current_moves, length), (opponent_moves, opponent_length) = possible_moves(board, piece), possible_moves(board, opponent)
        
        if (length|opponent_length)==0:
            return hamming_weight(board[1]) - hamming_weight(board[0])*100, []
        if depth == 0:
            x_moves, x_length = (current_moves, length) if piece else (opponent_moves, opponent_length)
            o_moves, o_length = (opponent_moves, opponent_length) if piece else (current_moves, length)
            return heuristic(board, piece, x_moves, x_length, o_moves, o_length), []
        if length == 0:
            val = midgame_minimax(board, opponent, depth, alpha, beta, empty-1)
            return (val[0], val[1]+[-1])
        current_moves = sorted(current_moves, key=lambda x: evaluate_move(board, x, piece,empty ))
    else:
        current_moves = possible
    
    best_opp_moves = []
    
    if piece:
        max_move, best_move = -100, 0
        for i in current_moves:
            tmp, opp_moves = midgame_minimax(place(board, piece, MOVES[i]), opponent, depth - 1, alpha, beta, empty-1)
            if tmp > max_move:
                max_move, best_move, best_opp_moves = tmp, i, opp_moves
                alpha = max(max_move, alpha)
            if beta <= alpha:
                break
        return (max_move, best_opp_moves + [best_move])
    else:
        min_move, best_move = 100, 0
        for i in current_moves:
            tmp, opp_moves = midgame_minimax(place(board, piece, MOVES[i]), opponent, depth - 1, alpha, beta, empty-1)
            if tmp < min_move:
                min_move, best_move, best_opp_moves = tmp, i, opp_moves
                beta = min(min_move, beta)
            if beta <= alpha:
                break
        return (min_move, best_opp_moves + [best_move])


def midgame(board, moves, piece, empty):
    best = (-1000, 0) if piece else (1000, 0)
    sorted_moves = sorted(moves, key=lambda x: possible_moves(place(board, piece, MOVES[x]), not piece)[1])
    for depth in range(3, 40):
        alpha, beta = (best[0], 10000) if piece else (-10000, best[0])

        val = midgame_minimax(board, piece, depth, alpha, beta, empty, possible=sorted_moves)
        best = max(val, best) if piece else min(val, best)
        print("Min score: {0}; move sequence: {1}".format(best[0], best[1]) if piece else "Min score: {0}; move sequence: {1}".format(best[0]*-1, best[1]))


def endgame_minimax(board, piece, depth, alpha, beta, possible=[]):
    """
    Returns the best value, [sequence of the previous best moves]
    """
    key, opponent = (board[0], board[1], piece, depth, alpha, beta), 1^piece
    if key in TREE_CACHE:
        return TREE_CACHE[key]

    if not possible:
        (current_moves, length), (opponent_moves, opponent_length) = possible_moves(board, piece), possible_moves(board, opponent)
        if (length|opponent_length)==0 or depth==0:
            return hamming_weight(board[1]) - hamming_weight(board[0]), []
        if length == 0:
            val = endgame_minimax(board, opponent, depth, alpha, beta)
            TREE_CACHE[key] = (val[0], val[1]+[-1])
            return TREE_CACHE[key]
        current_moves = sorted(current_moves, key=lambda x: possible_moves(place(board, piece, MOVES[x]), 1^piece)[1])
    else:
        current_moves = possible
    
    best_opp_moves = []
    if piece:
        max_move, best_move = -100, 0
        for i in current_moves:
            tmp, opp_moves = endgame_minimax(place(board, piece, MOVES[i]), opponent, depth - 1, alpha, beta)
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
            tmp, opp_moves = endgame_minimax(place(board, piece, MOVES[i]), opponent, depth - 1, alpha, beta)
            if tmp < min_move:
                min_move, best_move, best_opp_moves = tmp, i, opp_moves
                beta = min(min_move, beta)
            if beta <= alpha:
                break
        TREE_CACHE[key] = (min_move, best_opp_moves + [best_move])
        return TREE_CACHE[key]


def endgame(board, moves, piece):
    val = endgame_minimax(board, piece, 9, -10000, 10000, possible=sorted(moves, key=lambda x: possible_moves(place(board, piece, MOVES[x]), not piece)[1]))
    print("Min score: {0}; move sequence: {1}".format(val[0], val[1]) if piece else "Min score: {0}; move sequence: {1}".format(val[0]*-1, val[1]))

def main():
    string_board, piece = argv[1].upper(), argv[2].upper()
    board = string_to_board(string_board)
    piece = 0 if piece == 'O' else 1
    possible, _ = possible_moves(board, piece)
    num_empty = hamming_weight(FULL_BOARD ^ (board[0]|board[1]))
    if possible:
        if num_empty >= 14:
            midgame(board, possible, piece, num_empty)
        else:
            endgame(board, possible, piece)


if __name__ == "__main__":
    start = time()
    main()
