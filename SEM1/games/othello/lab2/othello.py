#!/usr/bin/env python3
from sys import argv
from re import compile, IGNORECASE, finditer

INDICES_2D = {(i,j):i*8 +j for i in range(8) for j in range(8)}
INDICES = {i: (i//8, i%8) for i in range(0,64)}
LETTERS = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
REGEX = {
    "X": {
        0: compile(r"xo+\.", IGNORECASE),
        1: compile(r"\.o+x", IGNORECASE)
    },
    "O": {
        0: compile(r"ox+\.", IGNORECASE),
        1: compile(r"\.x+o", IGNORECASE)
    }
}
CONSTRAINTS = {}
moves = []


def possible_moves(pzl, piece):
    possible = []
    for pos, elem in enumerate(pzl):
        if elem != piece:
            continue
        con = CONSTRAINTS[pos]
        idx = INDICES[pos]
        r, c = "".join(pzl[x] for x in con[0]), "".join(pzl[x] for x in con[1])
        ld, rd = "".join(pzl[x] for x in con[2]), "".join(pzl[x] for x in con[3])

        possible += [con[0][x.end()-1] for x in finditer(REGEX[piece][0], r) if pzl[con[0][x.end()-1]] == '.']
        possible += [con[1][x.end()-1] for x in finditer(REGEX[piece][0], c) if pzl[con[1][x.end()-1]] == '.']
        possible += [con[2][x.end()-1] for x in finditer(REGEX[piece][0], ld) if pzl[con[2][x.end()-1]] == '.']
        possible += [con[3][x.end()-1] for x in finditer(REGEX[piece][0], rd) if pzl[con[3][x.end()-1]] == '.']
        
        possible += [con[0][x.start()] for x in finditer(REGEX[piece][1], r) if pzl[con[0][x.start()]] == '.']
        possible += [con[1][x.start()] for x in finditer(REGEX[piece][1], c) if pzl[con[1][x.start()]] == '.']
        possible += [con[2][x.start()] for x in finditer(REGEX[piece][1], ld) if pzl[con[2][x.start()]] == '.']
        possible += [con[3][x.start()] for x in finditer(REGEX[piece][1], rd) if pzl[con[3][x.start()]] == '.']

    return set(possible)

        

def gen_constraints():
    rows = []
    for i in range(0,64,8):
        rows.append([*range(i,i+8)])
    for i in range(64):
        idx = INDICES[i]
        col = [*range(idx[1],64,8)]
        l_r, l_c = idx[0], idx[1]
        ld = set()
        while 0<=l_r and 0<=l_c:
            ld.add(INDICES_2D[(l_r, l_c)])
            l_r -= 1
            l_c -= 1
        l_r, l_c = idx[0], idx[1]
        while l_r<8 and l_c<8:
            ld.add(INDICES_2D[(l_r,l_c)])
            l_r += 1
            l_c += 1
        r_r, r_c = idx[0], idx[1]
        rd = set()
        while 0<=r_r<8 and 0<=r_c:
            rd.add(INDICES_2D[(r_r, r_c)])
            r_r += 1
            r_c -= 1
        r_r, r_c = idx[0], idx[1]
        while 0<=r_r and r_c<8:
            rd.add(INDICES_2D[(r_r,r_c)])
            r_r -= 1
            r_c += 1
        CONSTRAINTS[i] = (sorted(rows[idx[0]]), sorted(col), sorted([*ld]), sorted([*rd]))

def to_string(pzl):
    return '\n'.join(
        [''.join([pzl[INDICES_2D[(i, j)]][0] for j in range(8)]) for i in range(8)]).strip()


def main():
    global moves
    piece = ''
    board = [*'.'*27 + 'OX......XO'+'.'*27]
    if len(argv) != 0:
        for arg in argv[1:]:
            if len(arg) == 64:
                board = [*arg.upper()]
            elif arg.lower() == 'x' or arg.lower() == 'o':
                piece = arg.upper()
            else:
                moves.append(arg)
    if not piece:
        piece = "O" if board.count("O") < board.count("X") else "X"
    moves = [int(x) if x.isdigit() else LETTERS[x[0]] * 8 + int(x[1]) for x in moves]

    gen_constraints()
    possible = possible_moves(board, piece)
    return possible if len(possible) != 0 else "No moves possible"



if __name__ == "__main__":
    print(main())