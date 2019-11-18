#!/usr/bin/env python3
from time import process_time as time
from math import sqrt
from sys import argv


size_table = {
    9:  {'1', '2', '3', '4', '5', '6', '7', '8', '9'},
    12: {'1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C'},
    16: {'1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G'}
}
size, dim, sub_pzl_row, sub_pzl_col = 0, 0, 0, 0
constraint_table = {}
rows, cols, sub_pzls = [], [], []
NEIGHBORS = {}
ALL_CONSTRAINTS = []


def set_globals(pzl, l ):
    global size, dim, sub_pzl_row, sub_pzl_col, constraint_table
    size = l
    dim = int(sqrt(size))
    sub_pzl_row = int(sqrt(dim))
    sub_pzl_col = dim // sub_pzl_row
    gen_constraints()


def gen_constraints():
    global rows, cols, sub_pzls, constraint_table, NEIGHBORS, ALL_CONSTRAINTS
    rows = [[] for i in range(dim)]
    cols = [[] for i in range(dim)]
    sub_pzls = [[] for i in range(dim)]
    constraint_table = {}
    for i in range(dim):
        for j in range(dim):
            index = i*dim + j
            r = index // dim
            c = index % dim
            s = (int(index // (dim * sub_pzl_row) *
                sub_pzl_row + (index % dim) // sub_pzl_col))
            constraint_table[index] = (r, c, s)
            rows[r].append(index)
            cols[c].append(index)
            sub_pzls[s].append(index)
    ALL_CONSTRAINTS = rows + cols + sub_pzls
    NEIGHBORS = {i: set(rows[constraint_table[i][0]] + cols[constraint_table[i][1]]
                        + sub_pzls[constraint_table[i][2]]) - set(str(i)) for i in range(0, size)}

def checksum(pzl):
    return sum([ord(x) for x in pzl]) - 48*dim*dim


def find_best_index(pzl):
    max_pos = (-1,-1,set())
    for pos, elem in enumerate(pzl):
        if elem == '.':
            possibilities = set(pzl[j] for j in NEIGHBORS[pos] if pzl[j] != '.')
            length = len(possibilities)
            if length == len(size_table[dim])-1:
                return pos, possibilities
            elif length > max_pos[0]:
                max_pos = (length, pos, possibilities)
    return max_pos[1], max_pos[2]



def find_best_symbol(pzl, possibilities):
    for constraint in ALL_CONSTRAINTS:
        for symbol in size_table[dim] - {pzl[i] for i in constraint if i != '.'}:
            valid_positions = {index for index in constraint if pzl[index]=='.' \
                              and symbol not in {pzl[i] for i in NEIGHBORS[index] if i != '.'}}
            length = len(valid_positions)
            if length == 1 or length < len(possibilities):
                return symbol, valid_positions
    return None, None
          

def brute_force(pzl, changed=None, con_sets=None):
    if '.' not in pzl:
        return pzl

    index, c_s = find_best_index(pzl)
    set_of_choices = size_table[dim] - c_s 
    symbol, positions = find_best_symbol(pzl, set_of_choices)

    if symbol and positions:
        set_of_choices = positions
    
    
    if symbol and positions:
        new_pzls = [(pzl[:index] + symbol + pzl[index + 1:], index, c_s) for index in set_of_choices]
    else:
        new_pzls = [(pzl[:index] + symbol + pzl[index + 1:], index, c_s) for symbol in set_of_choices]


    for new_pzl in new_pzls:
        b_f = brute_force(new_pzl[0], changed=new_pzl[1], con_sets=new_pzl[2])
        if b_f:
            return b_f


if __name__ == '__main__':

    VERBOSE = False  # manually unset this variable for verbose output
    pzls = open('puzzles.txt' if len(argv) <
                2 else argv[1]).read().splitlines()
    start_all = time()
    prev_len = -1
    for pos, pzl in enumerate(pzls):
        pzl_len = len(pzl)
        if prev_len != pzl_len: # only reset tables if size changes
            set_globals(pzl, pzl_len)
            prev_len = pzl_len
        start = time()
        sol = brute_force(pzl)
        end = time() - start
        if VERBOSE:
            if sol:
                check = checksum(sol)
                print("Pzl {0}: {1}\n        {2} Checksum: {3} Solved in %.2lfs".format(
                    pos, pzl, sol, check) % end)
            else:
                print("Pzl {0}: {1} => Unsolvable Solved in %.2lfs".format(
                    pos, pzl) % end)
        else:
            if sol:
                check = checksum(sol)
                print("Pzl {0} Checksum {1} Solved in %.2lfs".format(pos, check) % end)
            else:
                print("Pzl {0} Unsolvable Solved in %.2lfs".format(pos) % end)
    print("Total Time: %.2lfs" % (time()-start_all))
