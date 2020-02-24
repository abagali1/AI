#!/usr/bin/env python3
# Anup Bagali Period 2
import sys
from re import compile, IGNORECASE
from time import time

SEED_REGEX = compile(r'([VH])(\d*)x(\d*)(.+)', IGNORECASE)
WORD_START_REGEX = compile(r'^([-$]{1,2})#')
WORD_MIDDLE_REGEX = compile(r'#([-$]{1,2})#')
WORD_END_REGEX = compile(r'#([-$]{1,2})$')
POSSIBLE_REGEX = compile(r"([-\w]+)", IGNORECASE)
HORIZONTAL = 1
VERTICAL = 0

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
ALL_CONSTRAINTS = []  # [[row0], [row1], [col0], col[1]]
SEARCH_CACHE, FIT_CACHE = {}, {}
ALPHABET = {*"abcdefghijklmnopqrstuvxwyz"}
WORDS_BY_LENGTH, COMMON_LETTERS, ALL_INDICES = [], [], []
DICTIONARY = set()
INTERSECTIONS = {}
H_CACHE = {}
ALPHA_START = ord('a')
BEST_DEPTH = 0
# INDEX, LENGTH, ORIENTATION, AFFECTED, LETTERS, TEMPLATE, WORDS = 0, 1, 2, 3, 4, 5, 6


to_string = lambda pzl: "\n".join(["".join([pzl[INDICES_2D[(i, j)]][0] for j in range(WIDTH)]) for i in range(HEIGHT)]).strip()


def search(regex, constraint, **kwargs):
    key = (regex, constraint)
    if key in SEARCH_CACHE:
        return SEARCH_CACHE[key]
    else:
        m = regex.search(constraint, **kwargs)
        SEARCH_CACHE[key] = m
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
    for constraint in ALL_CONSTRAINTS:
        con = "".join(board[x] for x in constraint)
        if BLOCK not in con:
            continue
        for r in [search(WORD_START_REGEX, con), search(WORD_MIDDLE_REGEX, con), search(WORD_END_REGEX, con)]:
            if r:
                if EMPTY not in r.group(1):
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
    if amt > 1:
        amt_cut = 0
        for component in components:
            if component[0] - amt_cut == 0:
                break
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
                amt_cut += component[0]
    return tried, blocks


def create_board(board, num_blocks):
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

    set_of_choices = sorted([pos for pos, elem in enumerate(board) if elem == EMPTY], key=lambda x: h(board, num_blocks, x))
    tried = set()
    for choice in set_of_choices:
        n = place_block(board, choice, num_blocks)
        if n:
            num_blocks, tried = n[0], tried | n[1]
            b_f = create_board(board, num_blocks)
            if b_f:
                return b_f
            for i in tried:
                board[i] = PROTECTED
                num_blocks += 1
            tried = set()
    return None


def bfs_blocks(board, start):
    visited, queue = {start}, [start]
    count = 0
    for index in queue:
        for neighbor in NEIGHBORS[index]:
            if board[neighbor] == BLOCK and neighbor not in visited:
                queue.append(neighbor)
                visited.add(neighbor)
                count += 1
    return visited


def h(board, blocks, x):
    if x in H_CACHE:
        return H_CACHE[x]
    else:
        board = try_block(board, x, blocks)
        if not board:
            H_CACHE[x] = H_CACHE[ROTATIONS[x]] = 1e9
            return 1e9
        else:
            visited, count = set(), 0
            components = []
            for pos, elem in enumerate(board):
                if elem != BLOCK or pos in visited:
                    continue
                comp = bfs_blocks(board, pos)
                visited |= comp
                components.append(comp)
                count += 1
            val = count*.1 + sum(len(x) for x in components)*50
            H_CACHE[x] = H_CACHE[ROTATIONS[x]] = val
            return val


def try_block(board, index, blocks):
    tmp, rotated = board[:], ROTATIONS[index]
    if tmp[index] == tmp[rotated] == PROTECTED:
        return False
    if tmp[index] == EMPTY:
        blocks -= 1
        if blocks < 0:
            return False
        tmp[index] = BLOCK
    if tmp[rotated] == EMPTY:
        blocks -= 1
        if blocks < 0:
            return False
        tmp[index] = BLOCK
    return tmp


def place_block(board, index, blocks):
    tried = set()
    rotated = ROTATIONS[index]
    if board[index] == board[rotated] == PROTECTED:
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


def place_word(board, word, index, horizontal):
    tmp = board.copy()
    if horizontal:
        for i in range(len(word)):
            idx = index + i
            if tmp[idx] != EMPTY and tmp[idx] != word[i]:
                return False
            tmp[idx] = word[i]
    else:
        for i in range(len(word)):
            idx = index + (WIDTH * i)
            if tmp[idx] != EMPTY and tmp[idx] != word[i]:
                return False
            tmp[idx] = word[i]
    return tmp


def can_fit(template, word):
    key = (template, word)
    if key in FIT_CACHE:
        return FIT_CACHE[key]
    else:
        for x, y in zip(template, word):
            if x != y and x != EMPTY:
                FIT_CACHE[key] = False
                return False
        FIT_CACHE[key] = True
        return True


def update_indices(board, indices, removed_index):
    intersections = INTERSECTIONS[(removed_index[0], removed_index[2])]
    new_indices = []
    for i in range(len(indices)):
        old = indices[i]
        template, new_words = old[5], old[6]
        count = old[4]
        if intersections.__contains__((old[0], old[2])):
            template, count = "", 0
            for idx in old[3]:
                template += board[idx]
                if ALPHABET.__contains__(board[idx]):
                    count += 1
            new_words = [word for word in new_words if can_fit(template, word)]
        new_indices.append((*old[:4], count, template, new_words))
    return sorted(new_indices, key=lambda x: x[4] - len(x[6]))


def possible_words(indices):
    return [(*i, sorted([word for word in WORDS_BY_LENGTH[i[1]] if can_fit(i[5], word)], key=lambda x: -word_occurrence(x, COMMON_LETTERS))) for i in indices]


def find_indices(board):
    idxs = []
    for row in ROWS:
        con = "".join(board[x] for x in row)
        if EMPTY not in con:
            continue
        for r in POSSIBLE_REGEX.finditer(con):
            if EMPTY not in r.group(1):
                continue
            s = r.span(1)
            if s[1] - s[0] >= 3:
                template = con[s[0]:s[1]]
                idxs.append((row[s[0]], s[1] - s[0], HORIZONTAL, [row[x] for x in range(s[0], s[1])], sum(template.count(a) for a in ALPHABET), template))
    for col in COLS:
        con = "".join(board[x] for x in col)
        if EMPTY not in con:
            continue
        for r in POSSIBLE_REGEX.finditer(con):
            if EMPTY not in r.group(1):
                continue
            s = r.span(1)
            if s[1] - s[0] >= 3:
                template = con[s[0]:s[1]]
                idxs.append((col[s[0]], s[1] - s[0], VERTICAL, [col[x] for x in range(s[0], s[1])], sum(template.count(a) for a in ALPHABET), template))
    for i in idxs:
        for j in idxs:
            key = (i[0], i[2])
            if {*j[3]} & {*i[3]}:
                if key in INTERSECTIONS:
                    INTERSECTIONS[key].add((j[0], j[2]))
                else:
                    INTERSECTIONS[key] = {(j[0], j[2])}
    return sorted(possible_words(idxs), key=lambda x: x[4])


def is_valid(board):
    tried = set()
    for index in ALL_INDICES:
        con = "".join(board[x] for x in index[3])
        if con not in DICTIONARY or con in tried:
            return False
        tried.add(con)
    return board


def solve(board, indices, tried, depth=0):
    global BEST_DEPTH
    for i in indices:
        if not i[6]:
            return False
    if EMPTY not in board:
        return is_valid(board)
    if depth > BEST_DEPTH:
        print(to_string(board), '\n')
        BEST_DEPTH = depth

    i = indices.pop(-1)
    for word in i[6]:
        if word in tried:
            continue
        new_board = place_word(board, word, i[0], i[2])
        if new_board:
            tried.add(word)
            s = solve(new_board, update_indices(new_board, indices, i), tried, depth + 1)
            if s:
                return s
            tried.remove(word)
    indices.append(i)
    return False


def main():
    global BLOCKS, WORDS_BY_LENGTH, COMMON_LETTERS, ALL_INDICES
    parse_args()

    gen_lookups()
    board, blocks = place_words([*EMPTY * AREA], BLOCKS)

    if BLOCKS == AREA:
        board = [*BLOCK * AREA]
    elif blocks == 0:
        board = finish(board)
    elif AREA % 2 and blocks % 2:
        board[CENTER] = BLOCK
        blocks -= 1
    board = finish(create_board(board, blocks))
    print(to_string(board), '\n\n')

    load_words(FILE)
    indices = find_indices(board)
    ALL_INDICES = indices

    return to_string(solve(board, indices, set()))


def parse_args():
    global HEIGHT, WIDTH, SEEDS, FILE, BLOCKS, INDICES, INDICES_2D, AREA, CENTER
    for arg in sys.argv[1:]:
        if "H" == arg[0].upper() or "V" == arg[0].upper():
            groups = search(SEED_REGEX, arg).groups()
            SEEDS.append((groups[0].upper(), int(groups[1]), int(groups[2]), [*groups[3].lower()]))
        elif ".txt" in arg:
            FILE = arg
        elif arg.isdigit():
            BLOCKS = int(arg)
        else:
            HEIGHT, WIDTH = (int(x) for x in arg.split("x"))
    AREA = HEIGHT * WIDTH
    CENTER = AREA // 2
    INDICES = {index: (index // WIDTH, (index % WIDTH)) for index in range(AREA)}  # idx -> (row, col)
    INDICES_2D = {(i, j): i * WIDTH + j for i in range(HEIGHT) for j in range(WIDTH)}  # (row, col) -> idx


def gen_lookups():
    global NEIGHBORS, ROTATIONS, ROWS, COLS, ALL_CONSTRAINTS
    for index in range(0, AREA):  # saves all possible neighbors for all indices
        row = index // WIDTH
        neighbors = [i for i in [index + WIDTH, index - WIDTH] if 0 <= i < AREA]
        if (index + 1) // WIDTH == row and index + 1 < AREA:
            neighbors.append(index + 1)
        if (index - 1) // WIDTH == row and index - 1 >= 0:
            neighbors.append(index - 1)
        NEIGHBORS[index] = neighbors

    ROTATIONS = {i: INDICES_2D[(HEIGHT - INDICES[i][0] - 1, WIDTH - INDICES[i][1] - 1)] for i in range(AREA)}

    ROWS = [[*range(i, i + WIDTH)] for i in range(0, AREA, WIDTH)]
    COLS = [[*range(i, AREA, WIDTH)] for i in range(0, WIDTH)]
    ALL_CONSTRAINTS = ROWS + COLS


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


def load_words(file):
    global WORDS_BY_LENGTH, COMMON_LETTERS
    DICTIONARY.add(EMPTY * WIDTH)
    DICTIONARY.add(EMPTY * HEIGHT)
    words = open(file).read().splitlines()
    max_length = len(max(words, key=lambda x: len(x))) + 1
    WORDS_BY_LENGTH, COMMON_LETTERS = [[] for _ in range(max_length)], [0 for _ in range(26)]
    for word in words:
        if len(word) <= 2:
            continue
        w = word.lower()
        DICTIONARY.add(w)
        WORDS_BY_LENGTH[len(word)].append(w)
        for pos, letter in enumerate(w):
            if letter not in ALPHABET:
                continue
            COMMON_LETTERS[ord(letter) - ALPHA_START] += 1


def word_occurrence(word, letter_occurrences):
    d = {x: word.count(x) for x in word}
    return sum(letter_occurrences[ord(x) - ALPHA_START] * y for x, y in d.items() if x in ALPHABET)


def finish(board):
    for seed in SEEDS:
        if seed[0] == "H":
            idx = INDICES_2D[(seed[1], seed[2])]
            for i in range(len(seed[3])):
                board[idx + i] = seed[3][i].lower()
        elif seed[0] == "V":
            idx = INDICES_2D[(seed[1], seed[2])]
            for i in range(len(seed[3])):
                board[idx + (WIDTH * i)] = seed[3][i].lower()
    return [x if x != PROTECTED else EMPTY for x in board]


if __name__ == '__main__':
    start = time()
    print(main())
    print(time() - start)
