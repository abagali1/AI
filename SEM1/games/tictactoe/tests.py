from functools import lru_cache
from sys import argv, setrecursionlimit

WIDTH = 0
HEIGHT = 0
WIN = 0

all_boards = set()

LOOKUP = dict()

setrecursionlimit(100000)


def parse_args():
    global WIN, HEIGHT, WIDTH

    WIN = int(argv[1])
    HEIGHT = int(argv[2])
    WIDTH = int(argv[3])


def place(board_list, index, c):
    board_list[index] = c
    r = "".join(board_list)
    board_list[index] = "."
    return r


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

    return False


@lru_cache(maxsize=None)
def bfs(board, c):
    global all_boards

    if complete(board):
        all_boards.add(board)
        return

    boards = []
    b_l = list(board)
    for index, item in enumerate(board):
        if not item == ".":
            continue
        b = place(b_l, index, c)
        boards.append(b)

    c = "x" if c == "o" else "o"
    for b in boards:
        bfs(b, c)


if __name__ == "__main__":
    parse_args()

    for index in range(WIDTH * HEIGHT):
        row = index // WIDTH
        col = index % WIDTH
        LOOKUP[(row, col)] = index

    board = "." * (WIDTH * HEIGHT)
    bfs(board, "x")
    print(all_boards)
    print(len(all_boards))