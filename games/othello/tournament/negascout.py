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
WEIGHT_MATRIX = {
    'm': 20,
    'tc': 20,
    'cc': 50,
    'se': 75,
    'w': 20
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


CORNERS = {0, 7, 56, 63}
CORNER_NEIGHBORS = {1:63, 6:56, 8:63, 9:63, 14:56, 15:56, 48:7, 49:7, 54:0, 55:0, 57:7, 62:0}
COL_EDGES =  {1:{7,15,23,31,39,47,55,63}, 0:{0,8,16,24,32,40,48,56}}
ROW_EDGES = {0: {0,1,2,3,4,5,6,7}, 1:{56,57,58,59,60,61,62,6}}
EDGES = {0: {0,1,2,3,4,5,6,7}, 1:{56,57,58,59,60,61,62,6}, 2:{7,15,23,31,39,47,55,63}, 3:{0,8,16,24,32,40,48,56}}


HAMMING_CACHE = {}
POSSIBLE_CACHE = {(68853694464, 34628173824, 0): {34, 43, 20, 29}, (68853694464, 34628173824, 1): {26, 19, 44, 37}}
TREE_CACHE = {}
WEIGHT_CACHE = {}
GRADER_MOVE = [11, 12, 13, 14, 15, 16, 17, 18, 21, 22, 23, 24, 25, 26, 27, 28, 31, 32, 33, 34, 35, 36, 37, 38, 41, 42, 43, 44, 45, 46, 47, 48, 51, 52, 53, 54, 55, 56, 57, 58, 61, 62, 63, 64, 65, 66, 67, 68, 71, 72, 73, 74, 75, 76, 77, 78, 81, 82, 83, 84, 85, 86, 87, 88]
PLAYER = {
    'o': 0,
    'O': 0,
    'x': 1,
    'X': 1,
    '@': 1
}
OPENING_BOOK = {('0x8000000', '0x101810000000', 0): 34, ('0x30000000', '0x101808040000', 0): 37, ('0x34000000', '0x1018080c0000', 0): 20, ('0x80024000000', '0x1018181c0000', 0): 53, ('0x80020000400', '0x10181c1e0000', 0): 52, ('0x80028180c00', '0x101c14060000', 0): 26, ('0x82028000c00', '0x101c143e0000', 0): 18, ('0x383028000400', '0xc143e0810', 0): 60, ('0x383028000c08', '0xc143e1010', 0): 58, ('0x383008000c38', '0xc743e1000', 0): 41, ('0x380008400c38', '0x7c743e1000', 0): 24, ('0x388048401c38', '0x7c343e2000', 0): 32, ('0x38c0c8401838', '0x3c343e2402', 0): 57, ('0x30c0c8503878', '0x4083c342e0402', 0): 21, ('0x24c0c8503878', '0xc183c342e0402', 0): 11, ('0x1004d0d8503878', '0xc782c242e0402', 0): 3, ('0x100004d0d8503878', '0x81c782c242e0402', 0): 5, ('0x1c0c14b0d8503878', '0x10e84c242e0402', 0): 30, ('0x1c0c04b6d8583878', '0x30f84824260402', 0): 38, ('0x1c0c04b6c05c3878', '0x30f8483f220402', 0): 49, ('0x1c0c04bcd07c7878', '0x30f9422f020402', 0): 31, ('0x1c0c00b9d07c7878', '0x30ff462f020402', 0): 61, ('0x1c0c00b1c05c3c00', '0x30ff4e3f2240fe', 0): 2, ('0x3c2020b1c05c3c00', '0x1edf4e3f2240fe', 0): 6, ('0x3e2428b1c0580000', '0x1ad74e3f267efe', 0): 47, ('0x3e0408a5c35f0000', '0x7af75a3c207efe', 0): 63, ('0x3e0408a4c25c0001', '0x7af75b3d237ffe', 0): 0, ('0xbe0428b4ca5c0001', '0x407ad74b35237ffe', 0): 8, ('0x80fce8b4ca5c0001', '0x7f02174b35237ffe', 0): 15, ('0x80ffebb5cb1d0101', '0x7f00144a3462fefe', 0): 40}



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
            board[1^piece] &= (FULL_BOARD ^ c)
    return board


def weight_table(board):
    h = 0
    while(board):
        b = board&-board
        h += WEIGHT_TABLE[LOG[b]]
        board ^= b
    return h+1


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
    current_board, opponent_board = board[current], board[opponent]
    m = ((current_length-opponent_length)/(current_length+opponent_length+1))

    current_corners = hamming_weight(current_board & CORNER_BOARD)
    opponent_corners = hamming_weight(opponent_board & CORNER_BOARD)
    cc = ((current_corners - opponent_corners)/(current_corners+opponent_corners+1))

    current_count = hamming_weight(current_board)
    opponent_count = hamming_weight(opponent_board)
    tc= ((current_count-opponent_count)/(current_count+opponent_count))
    
    current_weights = weight_table(current_board)
    opponent_weights = weight_table(opponent_board)
    w = current_weights-opponent_weights
    return m*WEIGHT_MATRIX['m']+cc*WEIGHT_MATRIX['cc']+tc*WEIGHT_MATRIX['tc']+w*WEIGHT_MATRIX['w']


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
    
    #current_moves = sorted(current_moves, key=lambda x: hamming_weight(place(board, current, MOVES[x])[current])-hamming_weight(place(board, current, MOVES[x])[opponent]))
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


class Strategy:
    def __init__(self):
        self.num_empty = -1
        self.ordered_moves = 0

    
    def choose_move(self, board, moves, piece, best_move):
        if self.num_empty >=14:
            best = (-1000, 0)
            for max_depth in range(3,50):
                val = negascout(board, piece, max_depth, best[0], 1000, self.num_empty)
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
            self.ordered_moves = sorted(moves, key=lambda x: evaluate_move(board, x, piece, self.num_empty), reverse=True)

        key = (hex(board[0]), hex(board[1]), piece)
        if key in OPENING_BOOK:
            best_move.value = GRADER_MOVE[OPENING_BOOK[key]]
        else:
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