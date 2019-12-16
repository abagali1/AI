#!/usr/bin/env python3
from sys import argv
from math import sqrt
from time import process_time as time
WIN, HEIGHT, WIDTH, AREA = 0, 0, 0, 0
X = 'X'
O = 'O'
SPACE = '.'
CACHE = set()
LOOKUP = {}
INDICES, INDICES_2D ={}, {}
CONSTRAINTS = []
all_boards = set()
x_boards, o_boards, tie = set(), set(), set()
terminal_board = set()
GAMES = {}
game = 0
PZL_CACHE  = {}



def generate_constraints():
    global CONSTRAINTS
    for i in range(WIDTH):
        row = []
        for j in range(HEIGHT):
            row.append(INDICES_2D[(j,i)])
        CONSTRAINTS.append(row)
    for i in range(HEIGHT):
        col = []
        for j in range(WIDTH):
            col.append(INDICES_2D[(i,j)])
        CONSTRAINTS.append(col)
    for a in range(WIDTH - WIN + 1):
        for b in range(HEIGHT - WIN + 1):
            diag = []
            for k in range(WIN):
                diag.append(INDICES_2D[(b+k,a+k)])
            CONSTRAINTS.append(diag)
    for a in range(WIDTH-WIN+1):
        for b in range(HEIGHT - WIN +1):
            diag = []
            for k in range(WIN):
                diag.append(INDICES_2D[(b+k,WIDTH-k-1-a)])
            CONSTRAINTS.append(diag)
    print(CONSTRAINTS)

def finished(pzl):
    for i in CONSTRAINTS:
        con = [pzl[j] for j in i]
        if con.count(X) >= WIN:
            return X
        if con.count(O) >= WIN:
            return O
    if '.' not in pzl:
        return 'T'
    return False


def possibilities(pzl, piece):
    global game
    all_boards.add(pzl)
    if pzl not in CACHE:
        b = [*pzl]
        f = finished(pzl)
        if f:
            terminal_board.add(pzl)
            if f == 'X':
                x_boards.add(pzl)
            if f == 'O':
                o_boards.add(pzl)
            if f == 'T':
                tie.add(pzl)
            return 1
        set_of_choices = [i for i in range(AREA) if pzl[i] == '.']
        CACHE.add(pzl)
        GAMES[pzl] = len(set_of_choices)        
        t = 0
        new_piece = X if piece == O else O
        for choice in set_of_choices:
            b[choice] = piece
            new_pzl = ''.join(b)
            b[choice] = '.'
            t += possibilities(new_pzl,new_piece)
        return t
    else:
        game += GAMES[pzl]
        return 0


def main():
    global HEIGHT, WIDTH, WIN, INDICES, INDICES_2D, AREA
    start = time()
    WIN, WIDTH, HEIGHT = (int(argv[1]), int(argv[2]), int(argv[3])) if len(argv) == 4 else (3, int(argv[1]), int(argv[2]))
    AREA = HEIGHT * WIDTH
    pzl = '.'*AREA
    INDICES = {index: (index // WIDTH, (index % WIDTH))
               for index in range(AREA)}
    INDICES_2D = {(i, j): i * WIDTH + j for i in range(HEIGHT)
                  for j in range(WIDTH)}
    generate_constraints()
    x = possibilities(pzl,X)
    print("Terminal Boards: {0}".format(len(terminal_board)))
    print("All boards: {0}".format(len(all_boards)))
    print("X: {0}".format(len(x_boards)))
    print("O: {0}".format(len(o_boards)))
    print("Tie: {0}".format(len(tie)))
    print("Games: {0}".format(game))
    print("Time %.2lfs" % (time()-start))

if __name__ == "__main__":
    main()
