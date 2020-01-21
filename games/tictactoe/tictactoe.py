#!/usr/bin/env python3
from functools import lru_cache
from sys import argv, setrecursionlimit

WIDTH = 0
HEIGHT = 0
WIN = 0

terminal_boards = set()
x_boards = set()
o_boards = set()
tie_boards = set()
all_boards = set()

INDICES_2D = dict()

setrecursionlimit(100000)


def place(board_list, index, c):
    board_list[index] = c
    r = "".join(board_list)
    board_list[index] = "."
    return r


def complete(board):
    global WIDTH, HEIGHT, WIN, INDICES_2D


    puzzle = board[::]
    while len(puzzle) > 0:
        row = puzzle[0:WIDTH]
        puzzle = puzzle[WIDTH:]
        if "x" * WIN in row:
            x_boards.add(board)
            return True
        if "o" * WIN in row:
            o_boards.add(board)
            return True

    for i in range(WIDTH):
        col = ""
        for j in range(HEIGHT):
            col += board[i + (j * WIDTH)]
        if "x" * WIN in col:
            x_boards.add(board)
            return True
        if  "o" * WIN in col:
            o_boards.add(board)
            return True

    for index, item in enumerate(board):
        row = index // WIDTH
        col = index % WIDTH
        diag = item

        count = 1
        while count > 0:
            try:
                diag += board[INDICES_2D[(row + count, col + count)]]
                if "x" * WIN in diag:
                    x_boards.add(board)
                    return True
                if "o" * WIN in diag:
                    o_boards.add(board)
                    return True
                count += 1
            except KeyError:
                count = -1

        diag = item
        count = 1
        while count > 0:
            try:
                diag += board[INDICES_2D[(row + count, col - count)]]
                if "x" * WIN in diag:
                    x_boards.add(board)
                    return True
                if "o" * WIN in diag:
                    o_boards.add(board)
                    return True
                count += 1
            except KeyError:
                count = -1

    if "." not in board:
        tie_boards.add(board)
        return True
    return False


@lru_cache(maxsize=None)
def brute_force(board, c):
    global all_boards, games
    all_boards.add(board)
    if complete(board):
        terminal_boards.add(board)
        return 1

    boards = []
    b_l = list(board)
    t = 0
    for index, item in enumerate(board):
        if not item == ".":
            continue
        b = place(b_l, index, c)
        boards.append(b)
    c = "x" if c == "o" else "o"
    for b in boards:
        t += brute_force(b, c)
    return t


if __name__ == "__main__":
    WIN, WIDTH, HEIGHT = (int(argv[1]), int(argv[2]), int(argv[3])) if len(argv) == 4 else (3, int(argv[1]), int(argv[2]))

    INDICES_2D = {(index // WIDTH, index % WIDTH):index for index in range(WIDTH*HEIGHT)}


    board = "." * (WIDTH * HEIGHT)
    games = brute_force(board, "x")
    print("Terminal Boards: {0}".format(len(terminal_boards)))
    print("X Win: {0}".format(len(x_boards)))
    print("O Win: {0}".format(len(o_boards)))
    print("Tie: {0}".format(len(tie_boards)))
    print("All boards: {0}".format(len(all_boards)))
    print("Games: {0}".format(games))
