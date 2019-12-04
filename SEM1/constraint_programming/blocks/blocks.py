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
ALPHABET = {i-ord('A'): chr(i) for i in range(ord('A'),ord('Z')+1)}
LETTERS = {}
INDICES = {}


def place(pzl, blocks, index):
    if blocks[0]+index[0] > PZL_HEIGHT or blocks[1]+index[1] > PZL_WIDTH:
        return False


    for i in range(index[0], index[0]+blocks[0]):
        for j in range(index[1], index[1]+blocks[1]):

            idx = i*PZL_WIDTH + j
            if idx > PZL_AREA:
                return False
            if pzl[idx] == '.':
                pzl = pzl[:idx] + blocks[2] + pzl[idx+1:]
            else:
                return False
    return pzl


def brute_force(pzl, blocks):
    if not blocks:
        return pzl

    block = blocks[-1]
    set_of_choices = [
        place(pzl, block, INDICES[index]) or place(pzl, (block[1], block[0], block[2]), INDICES[index]) \
        for index in [pos for pos, elem in enumerate(pzl) if elem == '.']
        ]
    
    tmp = [x for x in blocks if x != block]

    for choice in set_of_choices: # Take greatest rectangle first
        if choice:
            b_f = brute_force(pzl=choice, blocks=tmp)
            if b_f:
                return b_f


    
def can_fit(pzl, blocks):
    global BLOCKS_TOTAL_AREA, PZL_HEIGHT, PZL_WIDTH, PZL_PARITY, PZL_LONGEST_SIDE, PZL_AREA
    BLOCKS_TOTAL_AREA = sum(x[0]*x[1] for x in blocks)
    if PZL_AREA < BLOCKS_TOTAL_AREA or PZL_LONGEST_SIDE < max([x[0] if x[0] > x[1] else x[1] for x in blocks]):
        return False
    if PZL_AREA== BLOCKS_TOTAL_AREA and sum(x[0]+x[1] for x in blocks) % 2 != PZL_PARITY:
        return False
    return True


def to_string(pzl):
    return '\n'.join([''.join([pzl[i*PZL_WIDTH +j][0] for j in range(PZL_WIDTH)]) for i in range(PZL_HEIGHT)]).strip()


def decomposition(pzl):
    return to_string(pzl)



def main():
    global LETTERS, PZL_HEIGHT, PZL_WIDTH, PZL_PARITY, PZL_AREA, PZL_LONGEST_SIDE, NUM_BLOCKS, INDICES 

    args = ' '.join(argv[1:]).lower().replace('x',' ').split(" ")  # standardize format(no more 'x')
    pzl, blocks = '.' * int(args[0])*int(args[1]), sorted([(int(args[i]), int(args[i+1]), ALPHABET[pos]) for pos, i in enumerate(range(2, len(args), 2))],key=lambda x: x[0]*x[1]) # extract blocks
    PZL_HEIGHT, PZL_WIDTH, NUM_BLOCKS = int(args[0]), int(args[1]), len(blocks)
    PZL_PARITY, PZL_AREA = (PZL_HEIGHT + PZL_WIDTH) % 2, len(pzl)
    PZL_LONGEST_SIDE = PZL_HEIGHT if PZL_HEIGHT > PZL_WIDTH else PZL_WIDTH
    LETTERS = {i[2]: (i[0], i[1]) for i in blocks}
    INDICES = {index: (index // PZL_WIDTH, (index % PZL_WIDTH)) for index in range(PZL_AREA)}


    if not can_fit(pzl, blocks):
        return "No solution"

    if len(blocks) == 1:
        return "Decomposition: {0}x{1}".format(blocks[0][0], blocks[0][1]) if blocks[0][0] == PZL_HEIGHT \
            else "Decomposition: {0}x{1}".format(blocks[0][1], blocks[0][0])



    sol = brute_force(pzl=pzl, blocks=blocks)
    if sol:
        return "Decomposition:\n{0}".format(decomposition(sol))

    return "No solution"



if __name__ == "__main__":
    print(main())