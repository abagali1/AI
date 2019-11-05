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


def set_globals(pzl):
    global size, dim, sub_pzl_row, sub_pzl_col, constraint_table
    size = len(pzl)
    dim = int(sqrt(size))
    sub_pzl_row = int(sqrt(dim))
    sub_pzl_col = dim // sub_pzl_row
    gen_constraints()


def gen_constraints():
    global rows, cols, sub_pzls, constraint_table
    rows = [[] for i in range(dim)]
    cols = [[] for i in range(dim)]
    sub_pzls = [[] for i in range(dim)]
    constraint_table = {}
    for i in range(dim):
        for j in range(dim):
            index = i*dim + j
            r = index // dim
            c = index % dim
            s = (int(index // (dim * sub_pzl_col) *
                 sub_pzl_col + (index % dim) // sub_pzl_row))
            constraint_table[index] = (r, c, s)
            rows[r].append(index)
            cols[c].append(index)
            sub_pzls[s].append(index)

    for i in range(0, size):
        constraint_indexes = constraint_table[i]
        NEIGHBORS[i] = set(i for i in rows[constraint_indexes[0]] + cols[constraint_indexes[1]] + sub_pzls[constraint_indexes[2]])


def checksum(pzl):
    return sum([ord(x) for x in pzl]) - 48*dim*dim


def is_invalid(pzl, changed=None, neighbors=None):
    if neighbors is not None:
        sets = neighbors
    elif changed is not None:
        sets = set(pzl[i] for i in NEIGHBORS[changed])
    else:
        sets = set(pzl[i] for pos in range(len(pzl)) for i in rows[constraint_table[pos][0]]
               + cols[constraint_table[pos][1]] + sub_pzls[constraint_table[pos][1]])

    return len([j for i in sets for j in size_table[dim] if i.count(j) > 1]) != 0


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


def brute_force(pzl, changed=None, con_sets=None):
    if is_invalid(pzl, changed, con_sets):
        return ""
    if '.' not in pzl:
        return pzl

    index, c_s = find_best_index(pzl)
    new_pzls = [(pzl[:index] + j + pzl[index + 1:], index, c_s) for j in size_table[dim]-c_s]
    for new_pzl in new_pzls:
        b_f = brute_force(new_pzl[0], changed=new_pzl[1], con_sets=new_pzl[2])
        if b_f:
            return b_f


if __name__ == '__main__':

    VERBOSE = False  # manually unset this variable for verbose output
    pzls = open('puzzles.txt' if len(argv) <
                2 else argv[1]).read().splitlines()
    start_all = time()
    for pos, pzl in enumerate(pzls):
        set_globals(pzl)
        start = time()
        sol = brute_force(pzl)
        end = time() - start
        if VERBOSE:
            if sol:
                check = checksum(sol)
                print("Pzl {0}: {1} => {2} Checksum: {3} Solved in %.2lfs".format(
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
