#!/usr/bin/env python3
import sys
from re import compile, IGNORECASE, match, sub
from time import time as time

SEED_REGEX = compile(r"(V|H)(\d*)x(\d*)(.+)", IGNORECASE)
WORD_REGEX = compile(r"#([-\w]{1,2})#|^([-\w]{1,2})#|#([-\w]{1,2})$")
WORD_START_REGEX = compile(r"^([-\w]{1,2})#")
WORD_MIDDLE_REGEX = compile(r"#([-\w]{1,2})#")
WORD_END_REGEX = compile(r"#([-\w]{1,2})$")
ALPHABET = "abcdefghijklmnopqrstuvwxyz"

BLOCK = "#"
EMPTY = "-"
FILE = ""

BOARD, SEEDS = [], []
HEIGHT, WIDTH, AREA, BLOCKS = 0, 0, 0, 0
ALL_INDICES = set()  # set of all indices
PLACED = set()
INDICES = {}  # idx -> (row, col)
INDICES_2D = {}  # (row, col) -> idx
ROTATIONS = {}  # idx -> rotated 180 idx
NEIGHBORS = {}  # idx -> [neighbors]
ROWS = []  # [ [idxs in row 0], [idxs in row 1]]
COLS = []  # [ [idxs in col 0], [idxs in col 1]]
CONSTRAINTS = []  # [[row0], [row1], [col0], col[1]]
FULL_WALL = []  # [*'#'*WIDTH]
SEARCH_CACHE = {}

# print 2d board
to_string = lambda pzl: "\n".join(
    ["".join([pzl[INDICES_2D[(i, j)]][0] for j in range(WIDTH)]) for i in range(HEIGHT)]
).strip()


def bfs(board, starting_index):
    visited = {starting_index}
    queue = [starting_index]

    for index in queue:
        for neighbor in NEIGHBORS[index]:
            if board[neighbor] != BLOCK:
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.add(neighbor)

    return visited


def search(regex, constraint, **kwargs):
    key = (regex, constraint)
    if key in SEARCH_CACHE:
        return SEARCH_CACHE[key]
    else:
        m = regex.search(constraint, **kwargs)
        SEARCH_CACHE[key] = m
        return m


def can_place(board, index):
    return board[index] == BLOCK or board[index] == EMPTY


def implicit_blocks(board, blocks):
    tried = set()
    for constraint in CONSTRAINTS:
        con = "".join(board[x] for x in constraint)
        for r in [search(WORD_START_REGEX, con), search(WORD_MIDDLE_REGEX, con), search(WORD_END_REGEX, con)]:
            if r:
                if '-' not in r.group(1):
                    return False
                indices = [constraint[x] for x in range(*r.span(1))]
                for i in indices:
                    rotated = ROTATIONS[i]
                    if board[i] in ALPHABET or board[rotated] in ALPHABET or blocks <= 0:
                        for t in tried:
                            board[t] = EMPTY
                        return False
                    if board[i] == EMPTY:
                        board[i] = BLOCK
                        tried.add(i)
                        blocks -= 1
                    if board[rotated] == EMPTY:
                        board[rotated] = BLOCK
                        tried.add(rotated)
                        blocks -= 1
    return tried, blocks


def is_invalid(board):
    for constraint in CONSTRAINTS:
        con = "".join(board[x] for x in constraint)
        m = search(WORD_REGEX, con)
        if m:
            return True
    return False


def brute_force(board, num_blocks):
    implicit = implicit_blocks(board, num_blocks)
    if not implicit:
        return False
    else:
        tried, num_blocks = implicit

    if num_blocks == 1:
        board[AREA // 2] = BLOCK
        return board if not is_invalid(board) else False
    elif num_blocks <= 0:
        return board

    set_of_choices = [pos for pos, elem in enumerate(board) if elem == EMPTY]
    for choice in set_of_choices:
        rotated = ROTATIONS[choice]
        if board[rotated] != EMPTY or choice in tried:
            continue
        else:
            board[rotated] = board[choice] = BLOCK
            tried.add(choice)
            tried.add(rotated)
            if choice == rotated:
                b_f = brute_force(board, num_blocks - 1)
            else:
                b_f = brute_force(board, num_blocks - 2)
            if b_f:
                return b_f
            for i in tried:
                BOARD[i] = EMPTY

    return None


def main():
    global BOARD, BLOCKS
    parse_args()

    # bailouts
    if BLOCKS == AREA:
        return to_string(BLOCK * AREA)

    BOARD = [*EMPTY * AREA]
    gen_lookups()
    place_words()

    if BLOCKS == 0:
        return to_string(BOARD)

    sol = brute_force(BOARD,BLOCKS-BOARD.count('#'))
    if sol:
        print(sol.count(BLOCK))
        return to_string("".join(sol).replace('~','-'))


def place_words():
    global BOARD, BLOCKS
    for seed in SEEDS:
        if seed[0] == "H":
            idx = INDICES_2D[(seed[1], seed[2])]
            for i in range(len(seed[3])):
                index = idx + i
                if seed[3][i] == BLOCK:
                    BOARD[ROTATIONS[index]] = BLOCK
                BOARD[index] = seed[3][i]
            BOARD[idx : idx + len(seed[3])] = seed[3]
        if seed[0] == "V":
            idx = INDICES_2D[(seed[1], seed[2])]
            for i in range(len(seed[3])):
                index = idx + (WIDTH * i)
                if seed[3][i] == BLOCK:
                    BOARD[ROTATIONS[index]] = BLOCK
                BOARD[index] = seed[3][i]


def parse_args():
    global HEIGHT, WIDTH, SEEDS, FILE, BOARD, BLOCKS, INDICES, INDICES_2D, ROTATIONS, NEIGHBORS, AREA, FULL_WALL, ALL_INDICES
    for arg in sys.argv[1:]:
        if "H" == arg[0].upper() or "V" == arg[0].upper():
            groups = match(SEED_REGEX, arg).groups()
            SEEDS.append(
                (
                    groups[0].upper(),
                    int(groups[1]),
                    int(groups[2]),
                    [*groups[3].lower()],
                )
            )
        elif ".txt" in arg:
            FILE = arg
        elif arg.isdigit():
            BLOCKS = int(arg)
        else:
            HEIGHT, WIDTH = (int(x) for x in arg.split("x"))
    AREA = HEIGHT * WIDTH
    FULL_WALL = [*BLOCK * WIDTH]
    INDICES = {
        index: (index // WIDTH, (index % WIDTH)) for index in range(AREA)
    }  # idx -> (row, col)
    ALL_INDICES = {*INDICES}
    INDICES_2D = {
        (i, j): i * WIDTH + j for i in range(HEIGHT) for j in range(WIDTH)
    }  # (row, col) -> idx


def gen_lookups():
    global NEIGHBORS, ROTATIONS, ROWS, COLS, CONSTRAINTS
    for index in range(0, AREA):  # saves all possible neighbors for all indices
        row = index // WIDTH
        neighbors = [i for i in [index + WIDTH, index - WIDTH] if 0 <= i < AREA]
        if (index + 1) // WIDTH == row and index + 1 < AREA:
            neighbors.append(index + 1)
        if (index - 1) // WIDTH == row and index - 1 >= 0:
            neighbors.append(index - 1)
        NEIGHBORS[index] = neighbors

    ROTATIONS = {
        i: INDICES_2D[(HEIGHT - INDICES[i][0] - 1, WIDTH - INDICES[i][1] - 1)]
        for i in range(AREA)
    }

    ROWS = [[*range(i, i + WIDTH)] for i in range(0, AREA, WIDTH)]
    COLS = [[*range(i, AREA, WIDTH)] for i in range(0, WIDTH)]
    CONSTRAINTS = ROWS + COLS


if __name__ == "__main__":
    start = time()
    print(main())
    print(time()-start)

