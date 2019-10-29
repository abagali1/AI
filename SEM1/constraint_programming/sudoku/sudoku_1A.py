from time import time
from math import sqrt
from sys import argv


size_table = {
    9:  ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
    12: ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C'],
    16: ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G']
}
size, dim, sub_pzl_row, sub_pzl_col = 0, 0, 0, 0
constraint_table = []


def set_globals(pzl):
    global size, dim, sub_pzl_row, sub_pzl_col, constraint_table
    size = len(pzl)
    dim = int(sqrt(size))
    sub_pzl_row = int(sqrt(dim))
    sub_pzl_col = dim // sub_pzl_row
    constraint_table = gen_constraints()


def gen_constraints():
    rows = []
    for i in range(0, size, dim):  # populate rows
        rows.append(list(range(i, i+dim)))

    cols = []
    for i in range(0, dim):  # populate columns
        cols.append(list(range(i, size, dim)))

    tmp = []
    for i in range(0, size, sub_pzl_row):
        tmp.append(list(range(i, i+sub_pzl_row)))

    for i in range(0, , )


    return sub_pzls



def checksum(pzl):
    return sum([ord(x) for x in pzl]) - 48*dim*dim


def is_invalid(pzl):
    pass


def brute_force(pzl):
    if is_invalid(pzl):
        return ""
    i = pzl.find('.')
    if i == -1:
        return pzl

    new_pzls = [pzl[:i] + j + pzl[i + 1:] for j in size_table[dim]]
    for new_pzl in new_pzls:
        b_f = brute_force(new_pzl)
        if b_f:
            return b_f


if __name__ == '__main__':
    pzls = open('puzzles.txt' if len(argv) <
                2 else argv[1]).read().splitlines()
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
