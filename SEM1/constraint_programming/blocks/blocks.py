#!/usr/bin/env python3
# Anup Bagali Period 2
from sys import argv

BLOCKS_TOTAL_AREA = 0
PZL_HEIGHT = 0
PZL_WIDTH = 0
PZL_AREA = 0
PZL_PARITY = 0
PZL_LONGEST_SIDE = 0
NUM_BLOCKS = 0
ALPHABET = {i - ord('A'): chr(i) for i in range(ord('A'), ord('Z') + 1)}
LETTERS = {}
INDICES = {}
INDICES_2D = {}


def place(pzl, blocks, index):
    if blocks[0] + index[0] > PZL_HEIGHT or blocks[1] + index[1] > PZL_WIDTH:  # block does not fit
        return False

    tmp = [*pzl]
    for i in range(index[0], index[0] + blocks[0]):
        # start = i*PZL_WIDTH
        # end = i*PZL_WIDTH+blocks[1]
        # row = set(pzl[start:end])
        # if len(row) != 1:
        #     return False
        # else:
        #     pzl = pzl[:start] + blocks[2]*blocks[1] + pzl[end:]
        for j in range(index[1], index[1] + blocks[1]):
            idx = INDICES_2D[(i, j)]
            if tmp[idx] == '.':  # index empty
                tmp[idx] = blocks[2]
            else:
                return False  # index already occupied by another block
    return ''.join(tmp)



def find_corners(pzl, block):
    corners = []
    for i in range(PZL_AREA):
        if pzl[i] != '.':
            continue
        x,y = INDICES[i]
        neighbors = [pzl[INDICES_2D[(i)]] for i in [(x-1, y), (x+1,y), (x,y+1), (x,y-1)] if i in INDICES_2D]
        if neighbors.count('.') <= 2:
            corners.append(i) # adjust for left corners and right corners
    return False


def brute_force(pzl, blocks):
    if not blocks:
        return pzl

    block = blocks[-1]
    # possible_places = find_corners(pzl, block)

    # if possible_places:
    #     set_of_choices = [place(pzl, block, INDICES[index]) or place(pzl, (block[1], block[0], block[2]),
    #                                                                 INDICES[index]) for index in possible_places]
    # else:
    set_of_choices = [place(pzl, block, INDICES[index]) or place(pzl, (block[1], block[0], block[2]),
                                                                 INDICES[index]) for index, elem in enumerate(pzl) if elem == '.']


    for choice in set_of_choices:
        if choice:
            b_f = brute_force(pzl=choice, blocks=blocks[:-1])
            if b_f:
                return b_f


def to_string(pzl):
    return '\n'.join(
        [''.join([pzl[INDICES_2D[(i, j)]][0] for j in range(PZL_WIDTH)]) for i in range(PZL_HEIGHT)]).strip()


def decomposition(pzl):
    print(to_string(pzl))
    decomp = []
    visited = set()
    for i in range(PZL_HEIGHT):
        row = pzl[i*PZL_WIDTH:i*PZL_WIDTH+PZL_WIDTH]
        for j in range(PZL_WIDTH):
            if row[j] == '.':
                decomp.append('1x1')
            else:
                block = LETTERS[row[j]]
                if row[j] not in visited:
                    width = row.rfind(row[j]) - row.find(row[j])
                    if width+1 == block[1]:
                        decomp.append("{0}x{1}".format(block[0], block[1]))
                    else:
                        decomp.append("{0}x{1}".format(block[1], block[0]))
                visited.add(row[j])

    return ' '.join(decomp)


def main():
    global LETTERS, PZL_HEIGHT, PZL_WIDTH, PZL_PARITY, PZL_AREA, PZL_LONGEST_SIDE, NUM_BLOCKS, INDICES, INDICES_2D, BLOCKS_TOTAL_AREA

    # PARSE ARGUMENTS
    args = ' '.join(argv[1:]).lower().replace('x', ' ').split(" ")  # standardize format(no more 'x')
    pzl, blocks = '.' * int(args[0]) * int(args[1]), sorted([(int(args[i]), int(args[i + 1]), ALPHABET[pos]) for pos, i in enumerate(range(2, len(args), 2))], key=lambda x: x[0] * x[1])  # extract blocks
    
    # GLOBALS
    PZL_HEIGHT, PZL_WIDTH, NUM_BLOCKS = int(args[0]), int(args[1]), len(blocks)
    PZL_AREA =  PZL_HEIGHT*PZL_WIDTH
    PZL_LONGEST_SIDE = max(PZL_HEIGHT, PZL_WIDTH)
    BLOCKS_TOTAL_AREA = sum(x[0] * x[1] for x in blocks)

    # Bail out
    if PZL_AREA < BLOCKS_TOTAL_AREA or PZL_LONGEST_SIDE < max([max(x) for x in blocks]):
        return "No solution"

    # EASY CASE
    if len(blocks) == 1:
        return "Decomposition: {0}x{1}".format(blocks[0][0], blocks[0][1]) if blocks[0][0] == PZL_HEIGHT \
            else "Decomposition: {0}x{1}".format(blocks[0][1], blocks[0][0])
    
    LETTERS = {i[2]: (i[0], i[1]) for i in blocks}
    INDICES = {index: (index // PZL_WIDTH, (index % PZL_WIDTH))
               for index in range(PZL_AREA)}
    INDICES_2D = {(i, j): i * PZL_WIDTH + j for i in range(PZL_HEIGHT)
                  for j in range(PZL_WIDTH)}




    sol = brute_force(pzl=pzl, blocks=blocks)
    if sol:
        return "Decomposition: {0}".format(decomposition(sol))

    return "No solution"


if __name__ == "__main__":
    print(main())
