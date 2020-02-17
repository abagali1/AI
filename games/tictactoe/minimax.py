#!/usr/bin/env python3
from sys import argv
from functools import lru_cache 
from math import sqrt

ALL_CONSTRAINTS = {}
ALL_CONSTRAINTS = []
INDICES_2D = {}
INDICES = {}
LENGTH, WIDTH, HEIGHT = 0,0,0
WIN = 3
MAXIMIZER, MINIMIZER = '',''


def complete(board, player, opponent):
    for i in ALL_CONSTRAINTS:
        con = "".join([board[x] for x in i])
        if len(con) < 3:
            continue
        else:
            if player*WIN in con:
                return 10
            elif opponent*WIN in con:
                return  -10
    return 0
    
    
    

def gen_constraints(board):
    rows = []
    for i in range(0,LENGTH,WIDTH):
        rows.append([*range(i,i+WIDTH)])
    for i in range(LENGTH):
        idx = INDICES[i]
        col = [*range(idx[1],LENGTH,HEIGHT)]
        
        l_r, l_c = idx[0], idx[1]
        ld = set()
        while 0<=l_r and 0<=l_c:
            ld.add(INDICES_2D[(l_r, l_c)])
            l_r -= 1
            l_c -= 1
        l_r, l_c = idx[0], idx[1]
        while l_r<WIDTH and l_c<HEIGHT:
            ld.add(INDICES_2D[(l_r,l_c)])
            l_r += 1
            l_c += 1
        r_r, r_c = idx[0], idx[1]
        rd = set()
        while 0<=r_r<WIDTH and 0<=r_c:
            rd.add(INDICES_2D[(r_r, r_c)])
            r_r += 1
            r_c -= 1
        r_r, r_c = idx[0], idx[1]
        while 0<=r_r and r_c<HEIGHT:
            rd.add(INDICES_2D[(r_r,r_c)])
            r_r -= 1
            r_c += 1
        r = sorted(rows[idx[0]])
        c = sorted(col)
        ld = sorted([*ld])
        rd = sorted([*rd])
        ALL_CONSTRAINTS[i] = (r, c, ld, rd)
        ALL_CONSTRAINTS.append(r)
        ALL_CONSTRAINTS.append(c)
        ALL_CONSTRAINTS.append(ld)
        ALL_CONSTRAINTS.append(rd)  

def to_string(pzl):
    return '\n'.join(
        [''.join([pzl[INDICES_2D[(i, j)]][0] for j in range(HEIGHT)]) for i in range(WIDTH)]).strip()

def minimax(board, depth, is_max):
    score = complete(board, MAXIMIZER, MINIMIZER)
    print(to_string(board))
    print(score)
    print()
    if depth == 0:
        return score
    if score == 10 or score == -10:
        return score
    if '.' not in board:
        return 0

    if is_max:
        maxx = -200000
        for i in range(LENGTH):
            if board[i] == '.':
                board[i] = MAXIMIZER
                maxx = max(maxx, minimax(board, depth-1, False))
                board[i] = '.'
        return maxx
    else:
        minn = 200000
        for i in range(LENGTH):
            if board[i] == '.':
                board[i] = MINIMIZER
                minn = min(minn, minimax(board, depth-1, True))
                board[i] = '.'
        return minn
                    


def classify(board, piece):
    moves = {}
    for i in range(LENGTH):
        if board[i] == '.':
            board[i] = piece
            moves[i] = minimax(board, 7, False)
            board[i] = '.'
    return moves



def main():
    global LENGTH, HEIGHT, WIDTH, INDICES, INDICES_2D, MAXIMIZER, MINIMIZER
    board, WIDTH = ([*argv[1].upper()], argv[2]) if len(argv) == 3 else ([*argv[1].upper()], int(sqrt(len(argv[1]))))

    LENGTH = len(board)
    HEIGHT = LENGTH // WIDTH

    INDICES = {index: (index // WIDTH, (index % WIDTH))
               for index in range(LENGTH)}
    INDICES_2D = {(i, j): i * WIDTH + j for i in range(HEIGHT)
                  for j in range(WIDTH)}

    MAXIMIZER = 'X' if board.count('X') == board.count('O') else 'O' if board.count('X')>board.count('O') else 'X'
    MINIMIZER = 'O' if MAXIMIZER=='X' else 'X'


    gen_constraints(board)

    print(classify(board, MAXIMIZER))




if __name__ == '__main__':
    main()