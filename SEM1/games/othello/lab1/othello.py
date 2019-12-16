#!/usr/bin/env python3
from sys import argv
from re import compile, findall

INDICES_2D = {(i,j):i*8 +j for i in range(8) for j in range(8)}
INDICES = {i: (i//8, i%8) for i in range(0,64)}
LETTERS = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
WIDTH = HEIGHT = 8
moves = []


def possible_moves(pzl):
    pass


def display(pzl, piece):
    tmp = pzl[:]
    possible = possible_moves(tmp)
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