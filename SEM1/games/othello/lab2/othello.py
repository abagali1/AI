#!/usr/bin/env python3
from sys import argv
from re import compile, IGNORECASE, finditer

INDICES_2D = {(i,j):i*8 +j for i in range(8) for j in range(8)}
INDICES = {i: (i//8, i%8) for i in range(0,64)}
LETTERS = {'a1': 0, 'b1': 1, 'c1': 2, 'd1': 3, 'e1': 4, 'f1': 5, 'g1': 6, 'h1': 7, 'A1': 0, 'B1': 1, 'C1': 2, 'D1': 3, 'E1': 4, 'F1': 5, 'G1': 6, 'H1': 7, 'a2': 8, 'b2': 9, 'c2': 10, 'd2': 11, 'e2': 12, 'f2': 13, 'g2': 14, 'h2': 15, 'A2': 8, 'B2': 9, 'C2': 10, 'D2': 11, 'E2': 12, 'F2': 13, 'G2': 14, 'H2': 15, 'a3': 16, 'b3': 17, 'c3': 18, 'd3': 19, 'e3': 20, 'f3': 21, 'g3': 22, 'h3': 23, 'A3': 16, 'B3': 17, 'C3': 18, 'D3': 19, 'E3': 20, 'F3': 21, 'G3': 22, 'H3': 23, 'a4': 24, 'b4': 25, 'c4': 26, 'd4': 27, 'e4': 28, 'f4': 29, 'g4': 30, 'h4': 31, 'A4': 24, 'B4': 25, 'C4': 26, 'D4': 27, 'E4': 28, 'F4': 29, 'G4': 30, 'H4': 31, 'a5': 32, 'b5': 33, 'c5': 34, 'd5': 35, 'e5': 36, 'f5': 37, 'g5': 38, 'h5': 39, 'A5': 32, 'B5': 33, 'C5': 34, 'D5': 35, 'E5': 36, 'F5': 37, 'G5': 38, 'H5': 39, 'a6': 40, 'b6': 41, 'c6': 42, 'd6': 43, 'e6': 44, 'f6': 45, 'g6': 46, 'h6': 47, 'A6': 40, 'B6': 41, 'C6': 42, 'D6': 43, 'E6': 44, 'F6': 45, 'G6': 46, 'H6': 47, 'a7': 48, 'b7': 49, 'c7': 50, 'd7': 51, 'e7': 52, 'f7': 53, 'g7': 54, 'h7': 55, 'A7': 48, 'B7': 49, 'C7': 50, 'D7': 51, 'E7': 52, 'F7': 53, 'G7': 54, 'H7': 55, 'a8': 56, 'b8': 57, 'c8': 58, 'd8': 59, 'e8': 60, 'f8': 61, 'g8': 62, 'h8': 63, 'A8': 56, 'B8': 57, 'C8': 58, 'D8': 59, 'E8': 60, 'F8': 61, 'G8': 62, 'H8': 63}
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
ALL_CONSTRAINTS = []
moves = []


def possible_moves(pzl, piece):
    possible = []
    p = {}
    for constraint in ALL_CONSTRAINTS:
        con = "".join(pzl[x] for x in constraint)

        possible += [(constraint[x.end()-1],[constraint[i] for i in range(x.span()[0], x.span()[1])]) for x in finditer(REGEX[piece][0], con) if pzl[constraint[x.end()-1]] == '.']
        possible += [(constraint[x.start()],[constraint[i] for i in range(x.span()[0], x.span()[1])]) for x in finditer(REGEX[piece][1], con) if pzl[constraint[x.start()]] == '.']
    for i in possible:
        if i[0] in p:
            p[i[0]].update(i[1])
        else:
            p[i[0]] = {*i[1]}
    return p


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
        r = sorted(rows[idx[0]])
        c = sorted(col)
        ld = sorted([*ld])
        rd = sorted([*rd])
        CONSTRAINTS[i] = (r,c,ld,rd)
        ALL_CONSTRAINTS.append(r)
        ALL_CONSTRAINTS.append(c)
        ALL_CONSTRAINTS.append(ld)
        ALL_CONSTRAINTS.append(rd)       

def to_string(pzl):
    return '\n'.join(
        [''.join([pzl[INDICES_2D[(i, j)]][0] for j in range(8)]) for i in range(8)]).strip().lower()


def place(pzl, piece, index):
    print(index)
    for i in index: 
        pzl[i] = piece
    return pzl

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
        piece = "O" if board.count(".") % 2 != 0 else "X"
    moves = [int(x) if x.isdigit() else LETTERS[x] for x in moves]

    gen_constraints()
    print("{0} {1}/{2}".format("".join(board).lower(), board.count("X"), board.count("O")))
    possible = possible_moves(board, piece)
    for i in possible:
        board[i] = '*'
    print(to_string(board))
    for i in possible:
        board[i] = '.'
    print("Possible moves for {0}: {1}".format(piece, ", ".join(list(map(str,[x for x in possible])))))

    for move in moves:
        print("{0} moves to {1}".format(piece, move))
        board = place(board, piece, possible[move])
        print("{0} {1}/{2}".format("".join(board).lower(), board.count("X"), board.count("O")))
        piece = "X" if piece == "O" else "O"
        possible = possible_moves(board, piece)
        for i in possible:
            board[i] = '*'
        print(to_string(board))
        for i in possible:
            board[i] = '.'
        print("Possible moves for {0}: {1}".format(piece, ", ".join(list(map(str,[x for x in possible])))))




if __name__ == "__main__":
    main()