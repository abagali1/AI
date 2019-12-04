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


def place(pzl, blocks, index):
    print(f"Trying {blocks} at {index}")
    tmp = index[0]*PZL_WIDTH + index[1]
    print(to_string(pzl[:tmp]+"*"+pzl[tmp+1:]))

    if blocks[0]+index[0]-1 > PZL_HEIGHT or blocks[1]+index[1]-1 > PZL_WIDTH:
        print(f"C: Index ({index[0]+blocks[0]-1}, {index[1]+blocks[1]-1}) out of bounds\n")
        return False


    for i in range(index[0], index[0]+blocks[0]):
        for j in range(index[1], index[1]+blocks[1]):

            idx = i*PZL_WIDTH + j
            if idx > PZL_AREA:
                print(f"E: Index {i},{j} out of range\n")
                return False
            if pzl[idx] == '.':
                pzl = pzl[:idx] + blocks[2] + pzl[idx+1:]
            else:
                print(f"E: Index {i},{j} unempty\n")
                return False
    print(f"S: Block {blocks} placed at {index}\n")
    return pzl


def brute_force(pzl, blocks):
    if not blocks:
        return pzl

    print(f"Using {blocks}")
    index = pzl.find('.')
    index = (index // PZL_WIDTH, (index % PZL_WIDTH))


    for pos, block in enumerate(reversed(blocks)): # Take greatest rectangle first
        tmp = place(pzl, block, index) or place(pzl, (block[1], block[0], block[2]), index)
        if tmp:
            blks = blocks.copy()
            blks.remove(block)
            print(f"Placed {block}, Recurring on {blks}\n")
            b_f = brute_force(pzl=tmp, blocks=blks)
            if b_f:
                return b_f
    print(f"Could not place from {blocks}\n")


    
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
    print("IT DECOMPED")
    return to_string(pzl)

def main():
    global LETTERS, PZL_HEIGHT, PZL_WIDTH, PZL_PARITY, PZL_AREA, PZL_LONGEST_SIDE, NUM_BLOCKS 

    args = ' '.join(argv[1:]).lower().replace('x',' ').split(" ")  # standardize format(no more 'x')
    pzl, blocks = '.' * int(args[0])*int(args[1]), sorted([(int(args[i]), int(args[i+1]), ALPHABET[pos]) for pos, i in enumerate(range(2, len(args), 2))],key=lambda x: x[0]*x[1]) # extract blocks
    PZL_HEIGHT, PZL_WIDTH, NUM_BLOCKS = int(args[0]), int(args[1]), len(blocks)
    PZL_PARITY, PZL_AREA = (PZL_HEIGHT + PZL_WIDTH) % 2, len(pzl)
    PZL_LONGEST_SIDE = PZL_HEIGHT if PZL_HEIGHT > PZL_WIDTH else PZL_WIDTH
    LETTERS = {i[2]: (i[0], i[1]) for i in blocks}


    if not can_fit(pzl, blocks):
        return "No solution cant_fit"

    if len(blocks) == 1:
        return "Decomposition: {0}x{1}".format(blocks[0][0], blocks[0][1]) if blocks[0][0] == PZL_HEIGHT \
            else "Decomposition: {0}x{1}".format(blocks[0][1], blocks[0][0])



    sol = brute_force(pzl=pzl, blocks=blocks)
    if sol:
        return "Decomposition:\n{0}".format(decomposition(sol))

    return "No solution EOF"



if __name__ == "__main__":
    print(main())