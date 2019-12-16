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


def generate_constraints():
    global CONSTRAINTS 
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
    if "." not in pzl:
        return True
    if X*WIN in pzl or O*WIN in pzl:
        return True

    for i in CONSTRAINTS:
        con = [pzl[j] for j in i]
        if con.count(X) == WIN or con.count(O) == WIN:
            return True


def place(board_list, index, c):
    board_list[index] = c
    r = "".join(board_list)
    board_list[index] = "."
    return r

def possibilities(pzl, piece):
    if pzl in CACHE:
        return 0
    if '.' not in pzl:
        CACHE.add(pzl)
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
    print(possibilities(pzl,X)-230)


if __name__ == "__main__":
    print(main())
