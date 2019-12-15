#!/usr/bin/env python3
from sys import argv
from re import compile, findall

INDICES_2D = {(i,j):i*8 +j for i in range(8) for j in range(8)}
INDICES = {i: (i//8, i%8) for i in range(0,64)}
BOARD_REGEX = compile(r"[.OX]{64}")


def main():
    if len(argv) != 0:
        args = ' '.join(argv[1:]).upper()
        board = findall(BOARD_REGEX,args)
        board = ''.join(board) if board else '.'*27 + 'OX......XO'+'.'*27
        piece = "O" if " O" in args or "O " in args or "O" == argv[1].upper() else "X"
        moves = []

        return board, piece, moves
    else:
        piece = "X"
        moves = []
        board = '.'*27 + 'OX......XO'+'.'*27



if __name__ == "__main__":
    print(main())