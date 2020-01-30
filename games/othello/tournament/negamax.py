#!/usr/bin/env python3
from sys import argv
from time import time
from random import choice 

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
GRADER_MOVE = [11, 12, 13, 14, 15, 16, 17, 18, 21, 22, 23, 24, 25, 26, 27, 28, 31, 32, 33, 34, 35, 36, 37, 38, 41, 42, 43, 44, 45, 46, 47, 48, 51, 52, 53, 54, 55, 56, 57, 58, 61, 62, 63, 64, 65, 66, 67, 68, 71, 72, 73, 74, 75, 76, 77, 78, 81, 82, 83, 84, 85, 86, 87, 88]

PLAYER = {
    'o': 0,
    'O': 0,
    'x': 1,
    'X': 1,
    '@': 1
}

HAMMING_CACHE = {}
POSSIBLE_CACHE = {(68853694464, 34628173824, 0): {34, 43, 20, 29}, (68853694464, 34628173824, 1): {26, 19, 44, 37}}
TREE_CACHE = {}
WEIGHT_CACHE = {}


def string_to_board(board):
    board = board.replace("?","").replace(".","0")
    return {
        0: int(board.replace("o","1").replace("@","0"), 2),
        1: int(board.replace("o","0").replace("@","1"), 2)
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
    h = 20*current_length - 20*opponent_length

    h += 20*hamming_weight(board[current] & CORNER_BOARD)
    h -= 50*hamming_weight(board[opponent] & CORNER_BOARD)
    
    h += hamming_weight(board[current])-hamming_weight(board[0])

    h += weight_table(board[current])*20
    h -= weight_table(board[opponent])*20
    return h

        

def negascout(board, current, depth, alpha, beta):
    opponent = 1^current

    current_moves, opponent_moves = possible_moves(board, current), possible_moves(board, opponent)
    length, opponent_length = len(current_moves), len(opponent_moves)
    if not (FULL_BOARD ^ (board[current]|board[opponent])) or (length|opponent_length)==0:
        return hamming_weight(board[current])-hamming_weight(board[opponent])*10000,0
    if depth == 0:
        return heuristic(board, current, opponent, current_moves, length, opponent_moves, opponent_length),0

    current_moves = sorted(current_moves, key=lambda x: heuristic(board, current, opponent, current_moves, length, opponent_moves, opponent_length), reverse=True)

    best_score, best_move = -10000000, 0
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
    return alpha, best_move


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


class Strategy:
    def __init__(self):
        self.num_empty = -1
        self.ordered_moves = 0

    
    def choose_move(self, board, moves, piece, best_move):
        if self.num_empty >=14:
            print("a good move")
            best = (-1000, 0)
            for max_depth in range(3,50):
                val = negascout(board, piece, max_depth, -1000, 1000)
                best = max(val, best)
                best_move.value = GRADER_MOVE[best[1]]
        else:
            best_move.value = GRADER_MOVE[endgame_negamax(board, piece, 12, -1000, 1000, possible=self.ordered_moves)[1]]
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

        best_move.value = GRADER_MOVE[self.ordered_moves[0]]
        self.choose_move(board, moves, piece, best_move)
        self.ordered_moves = 0

if __name__ == '__main__':
    start = time()
    from multiprocessing import Value
    m = Value('d',0.0)
    s = Strategy()
    b = '???????????.@@@@@..??.ooooo..??ooo@oooo??o@@@oooo??o@@o@ooo??oo@@@ooo??ooo@@o..??..@@@@..???????????'
    s.best_strategy(b, 'o', m, 1)
    print(time()-start)