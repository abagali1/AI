#!/usr/bin/env python3
from time import time
from math import sqrt
from sys import argv


size_table = {
    9:  ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
    12: ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C'],
    16: ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G']
}
size, dim, sub_pzl_row, sub_pzl_col = 0, 0, 0, 0
constraint_table = {}
rows, cols, sub_pzls = [], [], []


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
            s = (int(index // (dim * sub_pzl_row) *
                sub_pzl_row + (index % dim) // sub_pzl_col))            constraint_table[index] = (r,c,s)
            rows[r].append(index)
            cols[c].append(index)
            sub_pzls[s].append(index)


def checksum(pzl):
    return sum([ord(x) for x in pzl]) - 48*dim*dim


def string_to_pzls(pos, pzl):
    constraint_indexes = constraint_table[pos]
    row_tmp = [pzl[i] for i in rows[constraint_indexes[0]]]
    col_tmp = [pzl[j] for j in cols[constraint_indexes[1]]]
    sub_tmp = [pzl[k] for k in sub_pzls[constraint_indexes[2]]]
    return [row_tmp] + [col_tmp] + [sub_tmp]


def is_invalid(pzl, changed=None):
    if changed is None:
        for pos, char in enumerate(pzl):
            if char != '.':
                pzls_list = string_to_pzls(pos, pzl)
                for p in pzls_list:
                    for i in range(1, 10):
                        if p.count(str(i)) > 1:
                            return True
        return False
    else:
        pzls_list = string_to_pzls(changed, pzl)
        for p in pzls_list:
            for i in range(1, 10):
                if p.count(str(i)) > 1:
                    return True
        return False


def brute_force(pzl, changed=None):
    if is_invalid(pzl, changed=None):
        return ""
    i = pzl.find('.')
    if i == -1:
        return pzl

    new_pzls = [(pzl[:i] + j + pzl[i + 1:], pos) for pos, j in enumerate(size_table[dim])]
    for new_pzl in new_pzls:
        b_f = brute_force(new_pzl[0], changed=new_pzl[1])
        if b_f:
            return b_f


if __name__ == '__main__':
    pzls = open('puzzles.txt' if len(argv) <
                2 else argv[1]).read().splitlines()
    start_all = time()
    for pos, pzl in enumerate(pzls):
        set_globals(pzl)
        start = time()
        sol = brute_force(pzl)
        check = checksum(sol)
        end = time() - start
        if sol:
            print("Pzl {0}: {1} => {2} Checksum: {3} Solved in %.2lfs".format(
                pos, pzl, sol, check) % end)
        else:
            print("Pzl {0}: {1} => Unsolvable Solved in %.2lfs".format(
                pos, pzl) % end)
    print("Total Time: %.2lfs" % (time()-start_all))
