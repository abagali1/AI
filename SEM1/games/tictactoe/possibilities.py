#!/usr/bin/env python3
from sys import argv
from math import sqrt
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



def generate_constraints():
    global CONSTRAINTS
    for i in range(0,AREA,WIDTH):
        CONSTRAINTS.append([*range(i,i+WIDTH)])
    for i in range(0, WIDTH):  # populate columns
        tmp = []
        for j in range(i, AREA, WIDTH):
            tmp.append(j)
        CONSTRAINTS.append(tmp)
    diag_len = int(sqrt(HEIGHT*HEIGHT + WIDTH+WIDTH))
    i = 1
    diag = [0]
    while len(diag) < diag_len:
        try:
            diag.append(INDICES_2D[(0+i,0+i)])
            i += 1
        except KeyError:
            break
    CONSTRAINTS.append(diag)
    i = 0
    diag = [WIDTH-1]
    while len(diag) < diag_len:
        try:
            diag.append(INDICES_2D[(WIDTH-1-i,0+i)])
            i += 1
        except KeyError:
            break
    CONSTRAINTS.append(diag)

def finished(pzl):
    for i in CONSTRAINTS:
        con = [pzl[j] for j in i]
        if con.count(X) >= WIN:
            x_boards.add(pzl)
            return True
        if con.count(O) >= WIN:
            o_boards.add(pzl)
            return True
    return False

def possibilities(pzl, piece):
    all_boards.add(pzl)
    if pzl in CACHE:
        return 0
    if '.' not in pzl:
        CACHE.add(pzl)
        tie.add(pzl)
        return 1
    if finished(pzl):
        CACHE.add(pzl)
        return 1
    set_of_choices = [pos for pos,elem in enumerate(pzl) if elem == '.']
    t = 0
    tmp = [*pzl]
    piece = X if piece == O else O
    for index in set_of_choices:
        tmp[index] = piece
        new_pzl = ''.join(tmp)
        if new_pzl not in CACHE:
            t += possibilities(''.join(tmp),piece )
        tmp[index] = '.'
    return t


# @lru_cache(maxsize=None)        
# def possibilities(pzl, piece):
#     global all_boards

#     if finished(pzl):
#         all_boards.add(pzl)
#         return 1

#     boards = []
#     tmp = [*pzl]
#     for pos, elem in enumerate(pzl):
#         if not elem == ".":
#             continue
#         b = place(tmp, pos, piece)
#         boards.append(b)

#     piece = X if piece == O else O
#     t = 0
#     for b in boards:
#         t += possibilities(b, piece)
#     return t



def main():
    global HEIGHT, WIDTH, WIN, INDICES, INDICES_2D, AREA
    WIN, HEIGHT, WIDTH = (int(argv[1]), int(argv[2]), int(argv[3])) if len(argv) == 4 else (3, int(argv[1]), int(argv[2]))
    AREA = HEIGHT * WIDTH
    pzl = '.'*AREA
    INDICES = {index: (index // WIDTH, (index % WIDTH))
               for index in range(AREA)}
    INDICES_2D = {(i, j): i * WIDTH + j for i in range(HEIGHT)
                  for j in range(WIDTH)}
    generate_constraints()
    possibilities(pzl,X)
    x_len = len(x_boards)
    o_len = len(o_boards)
    t_len = len(tie)
    print("Terminal Boards: {0}".format(x_len+o_len+t_len))
    print("All boards: {0}".format(len(all_boards)))
    print("X: {0}".format(len(x_boards)))
    print("O: {0}".format(len(o_boards)))
    print("Tie: {0}".format(len(tie)))
    print("Games: {0}".format(games))


if __name__ == "__main__":
    main()
