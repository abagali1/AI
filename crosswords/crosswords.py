#!/usr/bin/env python3
import sys
from re import compile, IGNORECASE, match
from time import time as time

SEED_REGEX = compile(r'([VH])(\d*)x(\d*)(.+)', IGNORECASE)
WORD_REGEX = compile(r'#([-$]{1,2})#|^([-$]{1,2})#|#([-$]{1,2})$')
WORD_START_REGEX = compile(r'^([-$]{1,2})#')
WORD_MIDDLE_REGEX = compile(r'#([-$]{1,2})#')
WORD_END_REGEX = compile(r'#([-$]{1,2})$')

BLOCK = "#"
EMPTY = "-"
PROTECTED = "$"
FILE = ""

SEEDS = []
HEIGHT, WIDTH, AREA, BLOCKS, CENTER = 0, 0, 0, 0, 0
PLACED = set()
INDICES = {}  # idx -> (row, col)
INDICES_2D = {}  # (row, col) -> idx
ROTATIONS = {}  # idx -> rotated 180 idx
NEIGHBORS = {}  # idx -> [neighbors]
ROWS = []  # [ [idxs in row 0], [idxs in row 1]]
COLS = []  # [ [idxs in col 0], [idxs in col 1]]
CONSTRAINTS = []  # [[row0], [row1], [col0], col[1]]
SEARCH_CACHE = {}

to_string = lambda pzl: "\n".join(
    ["".join([pzl[INDICES_2D[(i, j)]][0] for j in range(WIDTH)]) for i in range(HEIGHT)]
).strip()


def search(regex, constraint, **kwargs):
    key = (regex, constraint)
    if key in SEARCH_CACHE:
        return SEARCH_CACHE[key]
    else:
        m = regex.search(constraint, **kwargs)
        SEARCH_CACHE[key] = regex.search(constraint, **kwargs)
        return m


def bfs(board, starting_index, blocking_token=BLOCK):
    visited = {starting_index}
    queue = [starting_index]
    count = 0

    for index in queue:
        for neighbor in NEIGHBORS[index]:
            if board[neighbor] != blocking_token and neighbor not in visited:
                queue.append(neighbor)
                visited.add(neighbor)
                count += 1

    return count, visited


def connected_components(board):
    visited, components, count = set(), [], 0
    for pos, elem in enumerate(board):
        if elem == BLOCK or pos in visited:
            continue
        tmp = bfs(board, pos)
        visited |= tmp[1]
        components.append(tmp)
        count += 1
    return sorted(components), count


def implicit_blocks(board, blocks):
    tried = set()
    for constraint in CONSTRAINTS:
        con = "".join(board[x] for x in constraint)
        if BLOCK not in con:
            continue
        for r in [search(WORD_START_REGEX, con), search(WORD_MIDDLE_REGEX, con), search(WORD_END_REGEX, con)]:
            if r:
                if '-' not in r.group(1):
                    return False
                indices = [constraint[x] for x in range(*r.span(1))]
                for i in indices:
                    n = place_block(board, i, blocks)
                    if not n:
                        for t in tried:
                            board[t] = PROTECTED
                        return False
                    blocks, tried = n[0], tried | n[1]
    components, amt = connected_components(board)
    for component in components:
        cut = False
        for i in component[1]:
            if ROTATIONS[i] not in component[1]:
                cut = True
                break
        if cut:
            for i in component[1]:
                if i not in tried:
                    n = place_block(board, i, blocks)
                    if not n:
                        for t in tried:
                            board[t] = PROTECTED
                        return False
                    blocks, tried = n[0], tried | n[1]

    return tried, blocks


def brute_force(board, num_blocks):
    implicit = implicit_blocks(board, num_blocks)
    if not implicit:
        return False
    else:
        tried, num_blocks = implicit

    if num_blocks == 1:
        board[CENTER] = BLOCK
        return board
    elif num_blocks <= 0:
        return board

    set_of_choices = [pos for pos, elem in enumerate(board) if elem == EMPTY]
    tried = set()
    for choice in set_of_choices:
        if choice in tried:
            continue
        else:
            n = place_block(board, choice, num_blocks)
            if n:
                num_blocks, tried = n[0], tried | n[1]
                b_f = brute_force(board, num_blocks)
                if b_f:
                    return b_f
                for i in tried:
                    board[i] = PROTECTED
                    num_blocks += 1
                tried = set()
    return None


def place_block(board, index, blocks):
    tried = set()
    rotated = ROTATIONS[index]
    if board[index] == PROTECTED and board[rotated] == PROTECTED:
        return False
    if board[index] == EMPTY:
        blocks -= 1
        if blocks < 0:
            return False
        board[index] = BLOCK
        tried.add(index)
    if board[rotated] == EMPTY:
        blocks -= 1
        if blocks < 0:
            board[index] = EMPTY
            return False
        board[rotated] = BLOCK
        tried.add(rotated)
    return blocks, tried


def place_protected(board, index):
    rotated = ROTATIONS[index]
    if board[index] != BLOCK and board[rotated] != BLOCK:
        board[index] = board[rotated] = PROTECTED
        return True
    return False


def main():
    global BLOCKS
    parse_args()
    if BLOCKS == AREA:
        return to_string(BLOCK * AREA)

    gen_lookups()
    board, blocks = place_words([*EMPTY*AREA], BLOCKS)

    if blocks == 0:
        return to_string(finish(board))

    sol = brute_force(board, blocks)
    if sol:
        print(sol.count(BLOCK), BLOCKS)
        return to_string(finish(sol))


def parse_args():
    global HEIGHT, WIDTH, SEEDS, FILE, BLOCKS, INDICES, INDICES_2D, AREA, CENTER
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
    CENTER = AREA//2
    INDICES = {
        index: (index // WIDTH, (index % WIDTH)) for index in range(AREA)
    }  # idx -> (row, col)
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


def place_words(board, num_blocks):
    for seed in SEEDS:
        if seed[0] == "H":
            idx = INDICES_2D[(seed[1], seed[2])]
            for i in range(len(seed[3])):
                index = idx + i
                if seed[3][i] == BLOCK:
                    num_blocks = place_block(board, index, num_blocks)[0]
                else:
                    place_protected(board, index)
        elif seed[0] == "V":
            idx = INDICES_2D[(seed[1], seed[2])]
            for i in range(len(seed[3])):
                index = idx + (WIDTH * i)
                if seed[3][i] == BLOCK:
                    num_blocks = place_block(board, index, num_blocks)[0]
                else:
                    place_protected(board, index)
    return board, num_blocks


def finish(board):
    for seed in SEEDS:
        if seed[0] == "H":
            idx = INDICES_2D[(seed[1], seed[2])]
            for i in range(len(seed[3])):
                board[idx+i] = seed[3][i]
        elif seed[0] == "V":
            idx = INDICES_2D[(seed[1], seed[2])]
            for i in range(len(seed[3])):
                board[idx + (WIDTH * i)] = seed[3][i]
    return "".join(board).replace(PROTECTED, EMPTY)


if __name__ == '__main__':
    start = time()
    print(main())
    print(time()-start)
