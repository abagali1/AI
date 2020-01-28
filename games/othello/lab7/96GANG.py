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
            board[1^piece] &= (FULL_BOARD ^ c)
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
    opp_moves = possible_moves(placed, not piece)
    h = -len(opp_moves)*40
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
    strat = coin_heuristic if empty <= 8 else mobility_heuristic

    actual_move = MOVES[move]
    h = strat(board, actual_move, piece)
    h += next_to_corner(board, move, piece)
    h += stable_edge(board, move, piece)

    return h



def endgame_negamax(board, current, depth, alpha, beta, possible=[]):
    opponent = 1^current


    if not possible:
        current_moves, opponent_moves = possible_moves(board, current), possible_moves(board, opponent)
        length, opponent_length = len(current_moves), len(opponent_moves)
        if not (FULL_BOARD ^ (board[current]|board[opponent])) or (length|opponent_length)==0 or depth==0:
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
    val = endgame_negamax(board, piece, 11, -1000, 1000, possible=sorted_moves)
    print("My move is {0}".format(val[1]))


def heuristic(board, current, opponent, current_moves, current_length, opponent_moves, opponent_length):
    h = 20*current_length - 20*opponent_length

    h += 20*hamming_weight(board[current] & CORNER_BOARD)
    h -= 50*hamming_weight(board[opponent] & CORNER_BOARD)
    
    h += hamming_weight(board[current])-hamming_weight(board[0])

    h += weight_table(board[current])*20
    h -= weight_table(board[opponent])*20
    return h


def negascout(board, current, depth, alpha, beta, empty):
    opponent = 1^current

    current_moves, opponent_moves = possible_moves(board, current), possible_moves(board, opponent)
    length, opponent_length = len(current_moves), len(opponent_moves)
    if not (FULL_BOARD ^ (board[current]|board[opponent])) or (length|opponent_length)==0:
        return hamming_weight(board[current])-hamming_weight(board[opponent])*100,0
    if depth == 0:
        return heuristic(board, current, opponent, current_moves, length, opponent_moves, opponent_length),0

    if length==0 and opponent_length!=0:
        val = negascout(board, opponent, depth, -beta, -alpha, empty)
        return  -val[0], val[1] 
    
    current_moves = sorted(current_moves, key=lambda x: evaluate_move(board, x, current, empty), reverse=True)
    best_score, best_move = -10000000, 0
    for pos, move in enumerate(current_moves):
        child = place(board, current, MOVES[move])
        if pos == 0:
            score = -negascout(child, opponent, depth-1, -beta, -alpha, empty-1)[0]
        else:
            score = -negascout(child, opponent, depth-1, -alpha-1, -alpha, empty-1)[0]
            if alpha < score < beta:
                score = -negascout(child, opponent, depth-1, -beta, -score, empty-1)[0]
        if score > best_score:
            best_score = score
            best_move = move
        alpha = max(alpha, score)
        if alpha >= beta:
            break
    return alpha, best_move


def midgame(board, moves, piece, empty):
    best = (-1000, 0)
    for max_depth in range(3,50):
        val = negascout(board, piece, max_depth, best[0], 1000, empty)
        best = max(val, best)
        print("My move is", best[1])


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