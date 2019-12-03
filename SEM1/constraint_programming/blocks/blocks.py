#!/usr/bin/env python3
# Anup Bagali Period 2
from sys import argv

BLOCKS_TOTAL_AREA = 0
PZL_HEIGHT = 0
PZL_WIDTH = 0
PZL_AREA = 0
PZL_PARITY = 0
PZL_LONGEST_SIDE = 0
ALPHABET = {i-ord('A'): chr(i) for i in range(ord('A'),ord('Z')+1)}
LETTERS = {}


def place(pzl, blocks, index):
    if index+blocks[0] > PZL_HEIGHT or index+blocks[1] < PZL_WIDTH:
        return False
    for i in range(index+blocks[0]):
        for j in range(index+blocks[1]):
            if not pzl[i*PZL_WIDTH +j]:
                pzl[i*PZL_WIDTH+j] = blocks[2]
            else:
                return False
    return pzl


def brute_force(pzl, blocks):
    if not blocks:
        return pzl

    
    while blocks:
        block = blocks.pop(-1)

        index = pzl.find('.')
        pzl = place(pzl, block, index)
        if pzl:
            sol = brute_force(pzl, blocks)
            if sol:
                return sol
        else:
            pzl = place(pzl, (blocks[1], blocks[0], blocks[2]), index)
            if pzl:
                sol = brute_force(pzl, blocks)
                if sol:
                    return sol



    
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
    return ""

def main():
    global LETTERS, PZL_HEIGHT, PZL_WIDTH, PZL_PARITY, PZL_AREA, PZL_LONGEST_SIDE 

    args = ' '.join(argv[1:]).lower().replace('x',' ').split(" ")  # standardize format(no more 'x')
    pzl, blocks = '.' * int(args[0])*int(args[1]), sorted([(int(args[i]), int(args[i+1]), ALPHABET[pos]) for pos, i in enumerate(range(2, len(args), 2))],key=lambda x: x[0]*x[1]) # extract blocks
    PZL_HEIGHT, PZL_WIDTH = int(args[0]), int(args[1])
    PZL_PARITY, PZL_AREA = (PZL_HEIGHT + PZL_WIDTH) % 2, len(pzl)
    PZL_LONGEST_SIDE = PZL_HEIGHT if PZL_HEIGHT > PZL_WIDTH else PZL_WIDTH
    LETTERS = {i[2]: (i[0], i[1]) for i in blocks}


    if not can_fit(pzl, blocks):
        return "No solution"

    if len(blocks) == 1:
        return "Decomposition: {0}x{1}".format(blocks[0][0], blocks[0][1]) if blocks[0][0] == PZL_HEIGHT \
            else "Decomposition: {0}x{1}".format(blocks[0][1], blocks[0][0])



    sol = brute_force(pzl=pzl, blocks=blocks)
    if sol:
        return "Decomposition: {0}".format(decomposition(pzl))

    return "No solution"



if __name__ == "__main__":
    print(main())