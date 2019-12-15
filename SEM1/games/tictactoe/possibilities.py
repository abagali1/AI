#!/usr/bin/env python3
from sys import argv
WIN, HEIGHT, WIDTH = 0, 0, 0
X = 'X'
O = 'O'
SPACE = '.'
CACHE = set()
LOOKUP = {}


def complete(board):
    global WIDTH, HEIGHT, WIN, LOOKUP
    if "." not in board:
        return True

    puzzle = board[::]
    while len(puzzle) > 0:
        row = puzzle[0:WIDTH]
        puzzle = puzzle[WIDTH:]
        if "x" * WIN in row or "o" * WIN in row:
            return True

    for i in range(WIDTH):
        col = ""
        for j in range(HEIGHT):
            col += board[i + (j * WIDTH)]
        if "x" * WIN in col or "o" * WIN in col:
            return True

    for index, item in enumerate(board):
        row = index // WIDTH
        col = index % WIDTH
        diag = item

        count = 1
        while count > 0:
            try:
                diag += board[LOOKUP[(row + count, col + count)]]
                if "x" * WIN in diag or "o" * WIN in diag:
                    return True
                count += 1
            except KeyError:
                count = -1

        diag = item
        count = 1
        while count > 0:
            try:
                diag += board[LOOKUP[(row + count, col - count)]]
                if "x" * WIN in diag or "o" * WIN in diag:
                    return True
                count += 1
            except KeyError:
                count = -1

    return

def possibilities(pzl, move):
    if '.' not in pzl:
        CACHE.add(pzl)
        return 1

    if finished(pzl):
        CACHE.add(pzl)
        return 1
    

    set_of_choices = [pos for pos,elem in enumerate(pzl) if elem == '.']
    t = 0
    for index in set_of_choices:
        pzl = pzl[:index] + move + pzl[index+1:]
        t += possibilities(pzl, X if move == O else X)
        pzl = pzl[:index] + '.' + pzl[index+1:]
    return t


def main():
    global HEIGHT, WIDTH, WIN
    WIN, HEIGHT, WIDTH = (int(argv[1]), int(argv[2]), int(argv[3])) if len(argv) == 4 else (3, int(argv[1]), int(argv[2]))
    pzl = '.'*HEIGHT*WIDTH

    return possibilities(pzl,X)


if __name__ == "__main__":
    print(main())
    print(len(CACHE))
