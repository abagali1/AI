#!/usr/bin/env python3
from sys import argv
from time import time 
from re import compile, IGNORECASE, match
from functools import lru_cache
import random


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
STABLE_EDGE_REGEX = {
    1: compile(r"^x+[o.]*x+$", IGNORECASE),
    0: compile(r"^o+[x.]*o+", IGNORECASE)
}
PLAYER = {
    'o': 0,
    'O': 0,
    'x': 1,
    'X': 1,
    '@': 1
}


MOVES = {i: 1 << (63 - i) for i in range(64)}
POS = {MOVES[63 - i]: 63 - i for i in range(64)}

bit_not = lambda x: FULL_BOARD ^ x
is_on = lambda x, pos: x & MOVES[63-pos]
binary_to_board = lambda board: "".join(['o' if is_on(board[0], 63-i) else 'x' if is_on(board[1],63-i) else '.' for i in range(64)])


CORNERS = {0, 7, 56, 63}
CORNER_NEIGHBORS = {1:63, 6:56, 8:63, 9:63, 14:56, 15:56, 48:7, 49:7, 54:0, 55:0, 57:7, 62:0}
COL_EDGES =  {1:{7,15,23,31,39,47,55,63}, 0:{0,8,16,24,32,40,48,56}}
ROW_EDGES = {0: {0,1,2,3,4,5,6,7}, 1:{56,57,58,59,60,61,62,6}}
EDGES = {0: {0,1,2,3,4,5,6,7}, 1:{56,57,58,59,60,61,62,6}, 2:{7,15,23,31,39,47,55,63}, 3:{0,8,16,24,32,40,48,56}}


HAMMING_CACHE = {}
POSSIBLE_CACHE = {(68853694464, 34628173824, 0): {34, 43, 20, 29}, (68853694464, 34628173824, 1): {26, 19, 44, 37}}
TREE_CACHE = {}
GRADER_MOVE = [11, 12, 13, 14, 15, 16, 17, 18, 21, 22, 23, 24, 25, 26, 27, 28, 31, 32, 33, 34, 35, 36, 37, 38, 41, 42, 43, 44, 45, 46, 47, 48, 51, 52, 53, 54, 55, 56, 57, 58, 61, 62, 63, 64, 65, 66, 67, 68, 71, 72, 73, 74, 75, 76, 77, 78, 81, 82, 83, 84, 85, 86, 87, 88]



def string_to_board(board):
    b = board.replace(".","0").replace("?","")
    return {
        0: int(b.replace("o","1").replace("@","0"),2),
        1: int(b.replace("o","0").replace("@","1"),2)
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
            board[1^piece] &= (FULL_BOARD - c)
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
        if state is True or depth == 0:
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


def a_good_move(board, moves, piece, empty):
    for i in CORNERS:
        if i in moves:
            return i
    
    strat = coin_heuristic if empty <= 8 else mobility_heuristic
    best = (-FULL_BOARD, 0)

    for move in moves:
        actual_move = MOVES[move]
        h = strat(board, actual_move, piece)
        h += next_to_corner(board, move, piece)
        h += stable_edge(board, move, piece)

        if h > best[0]:
            best = (h, move)
        elif h==best[0]:
            tiebreaker = coin_heuristic if strat == mobility_heuristic else mobility_heuristic
            move += tiebreaker(board, actual_move, piece) 
            if h>best[0]:
                best = (h, move)
    return best[1]

class Strategy:
    def __init__(self):
        self.num_empty = -1
        self.ordered_moves = 0

    
    def choose_move(self, board, moves, piece, best_move):
        # best_move.value = GRADER_MOVE[a_good_move(board, moves, piece, self.num_empty)]
        # for depth in range(3, 24):
        #     best_move.value = GRADER_MOVE[minimax(board, piece, depth, -1000, 1000, self.ordered_moves)[1][-1]]
        #     print(best_move.value)
        if self.num_empty > 12:
            print("a good move")
            best_move.value = GRADER_MOVE[a_good_move(board, moves, piece, self.num_empty)]
        else:
            print("min max")
            best_move.value = GRADER_MOVE[minimax(board, piece, 12, -1000, 1000, self.ordered_moves)[1][-1]]
        print(best_move.value)



    def best_strategy(self, board, player, best_move, running):
        board, piece = string_to_board(board), PLAYER[player]
        moves = possible_moves(board, piece)
        if self.num_empty != -1:
            self.num_empty -= 1
        else:
            self.num_empty = hamming_weight(FULL_BOARD ^ (board[0]|board[1]) )

        if 1^self.ordered_moves:
            self.ordered_moves = sorted(moves, key= lambda x: len(possible_moves(place(board, piece, MOVES[x]), 1^piece)))

        
        self.choose_move(board, moves, piece, best_move)
        self.ordered_moves = 0

if __name__ == '__main__':
    from multiprocessing import Value
    m = Value('d',0.0)
    s = Strategy()
    b = '???????????o@@@@@..??o@@@o@..??@@o@o@@.??@@o@o@@.??@@oo@@o.??@@@@@ooo??..@@@oo.??...@oooo???????????'
    s.best_strategy(b, 'o', m, 1)