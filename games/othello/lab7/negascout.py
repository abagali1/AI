#!/usr/bin/env python3
from sys import argv
from re import compile, IGNORECASE, match


FULL_BOARD = 0xffffffffffffffff
RIGHT_MASK = 0xfefefefefefefefe
LEFT_MASK = 0x7f7f7f7f7f7f7f7f
CORNER_BOARD = 0x8100000000000081
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
WEIGHT_TABLE = [
        20, -3, 11, 8, 8, 11, -3, 20,
    	-3, -7, -4, 1, 1, -4, -7, -3,
    	11, -4, 2, 2, 2, 2, -4, 11,
    	8, 1, 2, -3, -3, 2, 1, 8,
    	8, 1, 2, -3, -3, 2, 1, 8,
    	11, -4, 2, 2, 2, 2, -4, 11,
    	-3, -7, -4, 1, 1, -4, -7, -3,
    	20, -3, 11, 8, 8, 11, -3, 20
        ]

MOVES = {i: 1 << (63^i) for i in range(64)}
POS = {MOVES[63^i]: 63^i for i in range(64)}
LOG = {MOVES[63^i]:i for i in range(64)}

bit_not = lambda x: FULL_BOARD ^ x
is_on = lambda x, pos: x & MOVES[63^pos]
binary_to_board = lambda board: "".join(['o' if is_on(board[0], 63^i) else 'x' if is_on(board[1],63^i) else '.' for i in range(64)])
binary_to_string = lambda x: '\n'.join([''.join(['{:064b}'.format(x)[i*8 +j][0] for j in range(8)]) for i in range(8)]).strip().lower()

print_binary = lambda x: print(binary_to_string(x))

CORNERS = {0, 7, 56, 63}
CORNER_NEIGHBORS = {1:63, 6:56, 8:63, 9:63, 14:56, 15:56, 48:7, 49:7, 54:0, 55:0, 57:7, 62:0}
COL_EDGES =  {1:{7,15,23,31,39,47,55,63}, 0:{0,8,16,24,32,40,48,56}}
ROW_EDGES = {0: {0,1,2,3,4,5,6,7}, 1:{56,57,58,59,60,61,62,6}}
EDGES = {0: {0,1,2,3,4,5,6,7}, 1:{56,57,58,59,60,61,62,6}, 2:{7,15,23,31,39,47,55,63}, 3:{0,8,16,24,32,40,48,56}}


HAMMING_CACHE = {}
POSSIBLE_CACHE = {(68853694464, 34628173824, 0): ({34, 43, 20, 29},4), (68853694464, 34628173824, 1): ({26, 19, 44, 37},4)}
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


def coin_heuristic(board, move, piece): # MAX: 100 MIN: -100
    placed = place(board,piece,move)
    num_player = hamming_weight(placed[piece])
    num_opp = hamming_weight(placed[1^piece])
    return (num_player-num_opp)*20


def mobility_heuristic(board, move, piece): # MAX: 0 MIN: -340
    placed = place(board, piece, move)
    opp_moves, opp_length = possible_moves(placed, 1^piece)
    h = -opp_length*40
    if any(map(lambda x: x in CORNERS, opp_moves)):
        h -= 100000
    return h


def next_to_corner(board, move, piece): # MAX: 150 MIN: -100000
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


def evaluate_move(board, move, piece):
    actual_move = MOVES[move]
    h = coin_heuristic(board, actual_move, piece)
    h += mobility_heuristic(board, actual_move, piece)
    h += next_to_corner(board, move, piece)
    h += stable_edge(board, move, piece)

    return h


def endgame_negamax(board, current, depth, alpha, beta, possible=[]):
    opponent = 1^current

    if not possible:
        (current_moves, length), (opponent_moves, opponent_length) = possible_moves(board, current), possible_moves(board, opponent)

        if (length|opponent_length)==0 or depth==0:
            return hamming_weight(board[current])-hamming_weight(board[opponent]),0
        if length==0 and opponent_length!=0:
            val = endgame_negamax(board, opponent, depth, -beta, -alpha)
            return -val[0], val[1]
        current_moves = sorted(current_moves, key=lambda x: possible_moves(place(board, current, MOVES[x]), opponent)[1])
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


def endgame(board, moves, piece):
    val = endgame_negamax(board, piece, 11, -1000, 1000, possible=sorted(moves, key=lambda x: possible_moves(place(board, piece, MOVES[x]), 1^piece)[1]))
    print("My move is {0}".format(val[1]))


def heuristic(board, current, opponent, current_moves, current_length, opponent_moves, opponent_length):
    current_board, opponent_board = board[current], board[opponent]
    h = ((current_length-opponent_length)/(current_length+opponent_length+1))

    current_corners = hamming_weight(current_board & CORNER_BOARD)
    opponent_corners = hamming_weight(opponent_board & CORNER_BOARD)*10
    h += ((current_corners-opponent_corners)/(current_corners+opponent_corners+1))*20

    return h


def negascout(board, current, depth, alpha, beta):
    opponent = 1^current

    key = (board[current], board[opponent], depth)
    if key in TREE_CACHE:
        return TREE_CACHE[key]

    (current_moves, length), (opponent_moves, opponent_length) = possible_moves(board, current), possible_moves(board, opponent)

    if (length|opponent_length)==0:
        return hamming_weight(board[current])-hamming_weight(board[opponent])*100,0
    if depth == 0:
        return heuristic(board, current, opponent, current_moves, length, opponent_moves, opponent_length),0

    if length==0 and opponent_length!=0:
        val = negascout(board, opponent, depth, -beta, -alpha)
        return  -val[0], val[1] 
    
    current_moves = sorted(current_moves, key=lambda x: evaluate_move(board, x, current), reverse=True)
    best_score, best_move = -100, 0
    for pos, move in enumerate(current_moves):
        child = place(board, current, MOVES[move])
        if pos == 0:
            score = -negascout(child, opponent, depth-1, -beta, -alpha)[0]
        else:
            score = -negascout(child, opponent, depth-1, -alpha-1, -alpha)[0]
            if alpha < score < beta:
                score = -negascout(child, opponent, depth-1, -beta, -score)[0]
        if score > best_score:
            best_score = score
            best_move = move
            alpha = max(alpha, score)
            if alpha >= beta:
                break
    TREE_CACHE[key] = (alpha, best_move)
    return alpha, best_move


def midgame(board, moves, piece):
    best = (-1000, 0)
    for max_depth in range(3,50):
        val = negascout(board, piece, max_depth, best[0], 1000)
        best = max(val, best)
        print("My move is", best[1])


def main():
    string_board, piece = argv[1].upper(), argv[2].upper()
    board = string_to_board(string_board)
    piece = 0 if piece == 'O' else 1
    possible = possible_moves(board, piece)[0]
    num_empty = hamming_weight(FULL_BOARD ^ (board[0]|board[1]))
    if possible:
        if num_empty >= 14:
            midgame(board, possible, piece)
        else:
            endgame(board, possible, piece)


if __name__ == '__main__':
    main()
