#!/usr/bin/env python3
from sys import argv
from time import time as time
from re import compile, IGNORECASE, match

MASKS = {
    -1: 0xfefefefefefefefe,
    1: 0x7f7f7f7f7f7f7f7f,
    8: 0xffffffffffffffff,
    -8: 0xffffffffffffffff,
    7: 0xfefefefefefefefe,
    9: 0x7f7f7f7f7f7f7f7f,
    -7: 0x7f7f7f7f7f7f7f7f,
    -9: 0xfefefefefefefefe
}
STABLE_EDGE_REGEX = {
    1: compile(r"\.|\.$|^x+o*\.|\.o*x+", IGNORECASE),
    0: compile(r"\.|\.$|^o+x*\.|\.x*o+", IGNORECASE)
}

bit_not = lambda x: 0xffffffffffffffff - x
is_on = lambda x, pos: x & MOVES[63-pos]

binary_to_board = lambda board: "".join(['o' if is_on(board[0], 63-i) else 'x' if is_on(board[1],63-i) else '.' for i in range(64)])
board_to_string = lambda x: '\n'.join([''.join([x[i*8+j]][0] for j in range(8)) for i in range(8)]).strip().lower()
binary_to_string = lambda x: '\n'.join([''.join(['{:064b}'.format(x)[i*8 +j][0] for j in range(8)]) for i in range(8)]).strip().lower()

print_binary = lambda x: print(binary_to_string(x))
print_board = lambda x: print(board_to_string(x))
print_board_binary = lambda x: print(board_to_string(binary_to_board(x)))


MOVES = {i: 1 << (63 - i) for i in range(64)}
POS = {MOVES[63 - i]: 63 - i for i in range(64)}
FULL_BOARD = 0xffffffffffffffff

CORNERS = {0, 7, 56, 63}
CORNER_NEIGHBORS = {1:63, 6:56, 8:63, 9:63, 14:56, 15:56, 48:7, 49:7, 54:0, 55:0, 57:7, 62:0}
COL_EDGES =  {1:{7,15,23,31,39,47,55,63}, 0:{0,8,16,24,32,40,48,56}}
ROW_EDGES = {0: {0,1,2,3,4,5,6,7}, 1:{56,57,58,59,60,61,62,6}}
EDGES = {0: {0,1,2,3,4,5,6,7}, 1:{56,57,58,59,60,61,62,6}, 2:{7,15,23,31,39,47,55,63}, 3:{0,8,16,24,32,40,48,56}}


HAMMING_CACHE = {}
POSSIBLE_CACHE = {}
TREE_CACHE = {}


def hamming_weight(n):
    if n in HAMMING_CACHE:
        return HAMMING_CACHE[n]
    else:
        orig = n
        c = 0
        while n:
            c += 1
            n ^= n & -n
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
    else:
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
            final |= fill(board[piece], board[not piece], d) & (FULL_BOARD - (board[piece] | board[not piece]))
        while final:
            b = final & -final
            possible.add(POS[b])
            final -= b
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
    if board[current] | board[not current] == FULL_BOARD:
        return True
    player_moves = possible_moves(board, current)
    opponent_moves = possible_moves(board, not current)
    return True if len(player_moves) + len(opponent_moves) == 0 else player_moves


def minimax(board, piece, depth):
    """
    Returns the best value, [sequence of the previous best moves]
    """
    key = (board[0],board[1],piece)
    if key in TREE_CACHE:
        return TREE_CACHE[key]

    state = game_over(board, piece)
    if state is True or depth == 0:
        return hamming_weight(board[1]) - hamming_weight(board[0]), []
    else:
        current_moves = state

    if len(current_moves) == 0:
        val = minimax(board, not piece, depth)
        TREE_CACHE[key] = (val[0, val[1]+[-1]])
        return TREE_CACHE[key]

    best_opp_moves = []
    if piece:
        max_move, best_move = -100, 0
        for i in current_moves:
            placed = place(board, piece, MOVES[i])
            tmp, opp_moves = minimax(placed, not piece, depth - 1)
            if tmp > max_move:
                max_move, best_move, best_opp_moves = tmp, i, opp_moves
        TREE_CACHE[key] = (max_move, best_opp_moves + [best_move])
        return TREE_CACHE[key]
    else:
        min_move, best_move = 100, 0
        for i in current_moves:
            placed = place(board, piece, MOVES[i])
            tmp, opp_moves = minimax(placed, not piece, depth - 1)
            if tmp < min_move:
                min_move, best_move, best_opp_moves = tmp, i, opp_moves
        TREE_CACHE[key] = (min_move, best_opp_moves + [best_move])
        return TREE_CACHE[key]



def coin_heuristic(board, move, piece): # MAX: 100 MIN: -100
    placed = place(board,piece,move)
    num_player = hamming_weight(placed[piece])
    num_opp = hamming_weight(placed[not piece])
    return (num_player-num_opp)*10


def mobility_heuristic(board, move, piece): # MAX: 0 MIN: -340
    placed = place(board, piece, move)
    opp_moves = possible_moves(placed, not piece)
    h = -len(opp_moves)*10
    if any(map(lambda x: x in CORNERS, opp_moves)):
        h -= 1000
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
        return 150
    return -100000


def stable_edge(board, move, piece):
    bs = binary_to_board(place(board, piece, move))
    token = 'X' if piece else 'O'
    for edge in EDGES:
        if move not in EDGES[edge]:
            continue
        con = "".join([bs[x] for x in EDGES[edge]])
        if con == token*8 or STABLE_EDGE_REGEX[piece].match(con):
            return 750
    return 0


def best_move(board, moves, piece):
    for i in CORNERS:
        if i in moves:
            print("My move is {0}".format(i))
            return
    moves = [*moves]
    init = moves[0]

    print("My move is {0}".format(init))
    actual_move = MOVES[init]
    strat = coin_heuristic if hamming_weight(bit_not(board[0]|board[1])) <= 8 else mobility_heuristic

    h = strat(board, actual_move, piece) + next_to_corner(board, actual_move, piece) + stable_edge(board, actual_move, piece)
    best = (h, init)
    
    for move in moves:
        actual_move = MOVES[move]
        h = strat(board, actual_move, piece)
        h += next_to_corner(board, move, piece)
        h += stable_edge(board, move, piece)
        tiebreaker = coin_heuristic if strat == mobility_heuristic else mobility_heuristic
        best = (h,move) if h>best[0] else (h,move) if (h==best[0] and tiebreaker(board, MOVES[move], piece) > tiebreaker(board, MOVES[best[1]], piece)) else best
    print("My move is {0}".format(best[1]))


def actual_best_move(board, moves, piece):
    final = (-1000, 0, 0) if piece else (1000, 0, 0)
    for move in sorted(moves, key=lambda x: mobility_heuristic(board, MOVES[x], piece))[::-1]:
        placed = place(board, piece, MOVES[move])
        val = minimax(placed, not piece, 12)
        final = max(final,(val[0], move, val[1]+[move])) if piece else min(final,(val[0], move, val[1]+[move]))
        print("Min score: {0}; move sequence: {1}".format(final[0], final[2]) if piece else "Min score: {0}; move sequence: {1}".format(final[0]*-1, final[2]))


def main():
    string_board, piece = argv[1].upper(), argv[2].upper()
    board = {
        0: int(string_board.replace('.', '0').replace('O', '1').replace('X', '0'), 2),
        1: int(string_board.replace('.', '0').replace('O', '0').replace('X', '1'), 2)
    }
    piece = 0 if piece == 'O' else 1
    possible = possible_moves(board, piece)
    num_empty = hamming_weight(FULL_BOARD - (board[0]|board[1]))

    if possible:
        print_board_binary(board)
        print()
        print(binary_to_board(board), "{0}/{1}".format(hamming_weight(board[1]), hamming_weight(board[0])))
        print(possible)
        best_move(board, possible, piece)
        if num_empty <= 12:
            actual_best_move(board, possible, piece)


if __name__ == "__main__":
    start = time()
    main()
    print("{0}".format(time() - start))
