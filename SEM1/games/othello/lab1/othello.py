#!/usr/bin/env python3
from sys import argv
from re import compile, findall, IGNORECASE

INDICES_2D = {(i,j):i*8 +j for i in range(8) for j in range(8)}
INDICES = {i: (i//8, i%8) for i in range(0,64)}
LETTERS = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
WIDTH = HEIGHT = 8
moves = []
REGEX = {
    "X": compile(r"xo+.", IGNORECASE),
    "O": compile(r"ox+.", IGNORECASE)
}
CONSTRAINTS = {}
rows, cols, rdiags, ldiags = [], [], [], []


def possible_moves(pzl, piece):
    for pos, elem in enumerate(pzl):
        if elem != piece:
            continue
        con = CONSTRAINTS[pos]
        r, c = "".join(pzl[x] for x in con[0]), "".join(pzl[x] for x in con[1])
        ld, rd = "".join(pzl[x] for x in con[2]), "".join(pzl[x] for x in con[3])
        
        

def gen_constraints():
    for i in range(64):
        idx = INDICES[i]
        row = [*range(idx[0],idx[0]+8)]
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
        CONSTRAINTS[i] = (row, col, [*ld], [*rd])


def display(pzl, piece):
    tmp = pzl[:]
    possible = possible_moves(tmp, piece)
    for i in possible:
        tmp[i] = '*'
    print("Possible moves for {0}: {1}".format(piece, ", ".join(list(map(str, possible)))))
    print(to_string("".join(tmp)))


def to_string(pzl):
    return '\n'.join(
        [''.join([pzl[INDICES_2D[(i, j)]][0] for j in range(8)]) for i in range(8)]).strip()


def main():
    global moves
    piece = "X"
    board = [*'.'*27 + 'OX......XO'+'.'*27]
    if len(argv) != 0:
        for arg in argv[1:]:
            if len(arg) == 64:
                board = [*arg]
            elif arg.lower() == 'x' or arg.lower() == 'o':
                piece = arg.upper()
            else:
                moves.append(arg)
    moves = [int(x) if x.isdigit() else LETTERS[x[0]] * WIDTH + int(x[1]) for x in moves]

    display(board, piece)
    for move in moves:
        board[move] = piece
        piece = 'X' if piece == 'O' else 'O'
        display(board, piece)
        

if __name__ == "__main__":
    print(main())