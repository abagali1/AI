#!/usr/bin/env python3
# Anup Bagali Period 2
import sys
from re import compile, IGNORECASE, match
from time import time as time

sys.setrecursionlimit(100000)
SEED_REGEX = compile(r'([VH])(\d*)x(\d*)(.+)', IGNORECASE)
WORD_START_REGEX = compile(r'^([-$]{1,2})#')
WORD_MIDDLE_REGEX = compile(r'#([-$]{1,2})#')
WORD_END_REGEX = compile(r'#([-$]{1,2})$')
POSSIBLE_REGEX = compile(r"([-\w]+)", IGNORECASE)


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
CONSTRAINTS = {}
SEARCH_CACHE = {}
FIND_CACHE = {}
ALPHABET = "abcdefghijklmnopqrstuvxwyz"
WORDS_BY_ALPHA, WORDS_BY_LENGTH, COMMON_LETTERS, STARTS_WITH = [], [], [], {}
DICTIONARY = set()

to_string = lambda pzl: "\n".join(
    ["".join([pzl[INDICES_2D[(i, j)]][0] for j in range(WIDTH)]) for i in range(HEIGHT)]
).strip()


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
    if num_blocks == 1:
        print('b')
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


def place_word(board, word, index, horizontal):
    tmp = board.copy()
    if horizontal:
        for i in range(len(word)):
            idx = index+i
            if tmp[idx] != EMPTY and tmp[idx] != word[i]:
                return False
            tmp[index+i] = word[i]
    else:
        for i in range(len(word)):
            idx = index + (WIDTH*i)
            if tmp[idx] != EMPTY and tmp[idx] != word[i]:
                return False
            tmp[index + (WIDTH * i)] = word[i]
    return tmp


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
            if s[1]-s[0] >= 3:
                idxs.append((row[s[0]], s[1]-s[0], 1, con))
    for col in COLS:
        con = "".join(board[x] for x in col)
        if EMPTY not in con:
            continue
        for r in POSSIBLE_REGEX.finditer(con):
            if EMPTY not in r.group(1):
                continue
            s = r.span(1)
            if s[1]-s[0] >= 3:
                idxs.append((col[s[0]], s[1]-s[0], 0, con))
    return idxs


def is_invalid(board):
    for pos, elem in enumerate(board):
        if elem == BLOCK:
            continue
        h = "".join(board[x] for x in CONSTRAINTS[pos][0]).replace(BLOCK, "")
        if EMPTY not in h and h not in DICTIONARY:
            return True
        v = "".join(board[x] for x in CONSTRAINTS[pos][1]).replace(BLOCK, "")
        if EMPTY not in v and v not in DICTIONARY:
            return True
    return False


def solve(board, words, prev=1):
    print(to_string(board), '\n'*3)
    # if is_invalid(board):
    #     return False
    if EMPTY not in board:
        return board

    indices = find_indices(board)
    for index in indices:
        if prev == index[2]:
            continue
        for word in words[index[1]][::-1]:
            new_board = place_word(board, word, index[0], index[2])
            if new_board:
                if words[index[1]]:
                    del words[index[1]][-1]
                s = solve(new_board, words, 1)
                if s:
                    return s
                words[index[2]].append(word)


def main():
    global BLOCKS, WORDS_BY_ALPHA, WORDS_BY_LENGTH, COMMON_LETTERS
    parse_args()

    gen_lookups()
    board, blocks = place_words([*EMPTY*AREA], BLOCKS)

    if BLOCKS == AREA:
        board = [*BLOCK * AREA]
    elif blocks == 0:
         board = finish(board)
    else:
        if AREA % 2 and blocks % 2:
            board[CENTER] = BLOCK
            blocks -= 1
        board = finish(create_board(board, blocks))

    print(to_string(board))

    words = load_words(FILE)
    WORDS_BY_ALPHA, WORDS_BY_LENGTH, COMMON_LETTERS, STARTS_WITH = words
    sol = solve(board, words[1])
    if sol:
        return to_string(sol)


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
    global NEIGHBORS, ROTATIONS, ROWS, COLS, ALL_CONSTRAINTS, CONSTRAINTS
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
    ALL_CONSTRAINTS = ROWS + COLS
    CONSTRAINTS = {i: (ROWS[i//WIDTH], COLS[i%WIDTH], set(ROWS[i//WIDTH]+COLS[i%WIDTH])) for i in range(AREA)}


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
    start = ord('a')
    DICTIONARY.add(EMPTY*WIDTH)
    DICTIONARY.add(EMPTY*HEIGHT)
    max_length = len(max(open(file).read().splitlines(), key=lambda x: len(x)))+1
    words_by_alpha, words_by_length = [[] for i in range(26)], [[] for i in range(max_length)]
    starts_with = {}
    letters = [[0, chr(i+start)] for i in range(26)]
    for word in open(file).read().splitlines():
        if len(word) <= 2:
            continue
        w = word.lower()
        DICTIONARY.add(w)
        words_by_alpha[ord(w[0])-start].append(w)
        words_by_length[len(word)].append(w)
        for pos, letter in enumerate(w):
            if pos != 0 and pos != len(w):
                key = w[:pos]
                if key in starts_with:
                    starts_with[key].append(w)
                else:
                    starts_with[key] = [w]
            if letter not in ALPHABET:
                continue
            letters[ord(letter)-start][0] += 1
    letters = [x[0] for x in letters]
    return [sorted(word_list, key=lambda x: len(x)) for word_list in words_by_alpha], [sorted(x, key=lambda y: word_occurrence(y, letters)) for x in words_by_length], letters, starts_with


def word_occurrence(word, letter_occurrences):
    d = {x: word.count(x) for x in word}
    return sum(letter_occurrences[ord(x)-ord('a')]*y for x, y in d.items() if x in ALPHABET)


def finish(board):
    for seed in SEEDS:
        if seed[0] == "H":
            idx = INDICES_2D[(seed[1], seed[2])]
            for i in range(len(seed[3])):
                board[idx+i] = seed[3][i].lower()
        elif seed[0] == "V":
            idx = INDICES_2D[(seed[1], seed[2])]
            for i in range(len(seed[3])):
                board[idx + (WIDTH * i)] = seed[3][i].lower()
    return [x if x != PROTECTED else EMPTY for x in board]


if __name__ == '__main__':
    start = time()
    print(main())
    print(time()-start)