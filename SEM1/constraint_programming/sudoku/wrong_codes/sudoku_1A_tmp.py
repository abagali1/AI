#!/usr/bin/env python3
from sys import argv
from math import sqrt
from time import time


length, dim, col, row = 0, 0, 0, 0
size_table = {
    9:  ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
    12: ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C'],
    16: ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G']
}
sub_pzls = {0: 0, 1: 0, 2: 0, 9: 0, 10: 0, 11: 0, 18: 0, 19: 0, 20: 0, 3: 3, 4: 3, 5: 3, 12: 3, 13: 3, 14: 3, 21: 3, 22: 3, 23: 3, 6: 6, 7: 6, 8: 6, 15: 6, 16: 6, 17: 6, 24: 6, 25: 6, 26: 6, 27: 27, 28: 27, 29: 27, 36: 27, 37: 27, 38: 27, 45: 27, 46: 27, 47: 27, 30: 30, 31: 30, 32: 30, 39: 30, 40: 30, 41: 30, 48: 30, 49: 30, 50: 30, 51: 33, 33: 33, 34: 33, 35: 33, 42: 33, 43: 33, 44: 33, 52: 33, 53: 33, 54: 54, 55: 54, 56: 54, 63: 54, 64: 54, 65: 54, 72: 54, 73: 54, 74: 54, 57: 57, 58: 57, 59: 57, 66: 57, 67: 57, 68: 57, 75: 57, 76: 57, 77: 57, 60: 60, 61: 60, 62: 60, 69: 60, 70: 60, 71: 60, 78: 60, 79: 60, 80: 60}


def string_to_pzl(p):
    global length, dim, col, row
    # list of all rows, columns, and sub puzzles
    pzls = {'rows': [], 'columns': [], 'sub_puzzles': []}
    for i in range(0, length, dim):  # populate rows
        tmp = []
        for j in range(i, i+dim):
            tmp.append(p[j])
        pzls['rows'].append(tmp)
    for i in range(0, dim):  # populate columns
        tmp = []
        for j in range(i, length, dim):
            tmp.append(p[j])
        pzls['columns'].append(tmp)
    sub_puzzles = []
    for i in range(0, dim, row):  # populate sub puzzles
        tmp = []
        for x in pzls['rows']:
            tmp.append(x[i:i+row])
        sub_puzzles.append(tmp)
    for i in sub_puzzles:
        for j in range(0, len(i), col):
            tmp = []
            for k in i[j:j+col]:
                tmp += k
            pzls['sub_puzzles'].append(tmp)
    pzls = list(pzls.values())
    return pzls[0] + pzls[1] + pzls[2]


def gen_constraints(pzl, index):
    global dim, length
    row_num = index // dim
    col_num = index % dim
    sub_num = sub_pzls[index]
    tmp = [*pzl[sub_num:sub_num+3]] + [*pzl[sub_num+9:sub_num+12]] + [*pzl[sub_num+18:sub_num+21]] 

    return [ [pzl[i] for i in range(row_num, row_num+dim)], [pzl[i] for i in range(col_num, length, dim)  ], tmp]



def is_invalid(p):
    for pos, elem in enumerate(p):
        if elem != '.':
            p_l = gen_constraints(p,pos)
            for pzl in p_l:
                for j in size_table[dim]:
                    if pzl.count(str(j)) > 1:
                        return True
    return False

def set_sizes(pzl):
    global length, dim, col, row
    length = len(pzl)
    dim = int(sqrt(length))
    row = int(sqrt(dim))
    col = dim // row


def is_solved(pzl):
    return False if pzl.find(".") != -1 else True


def check_sum(pzl):
    return sum([ord(x) for x in pzl]) - 48*dim*dim


def brute_force(pzl):
    if is_invalid(pzl):
        return ""
    if is_solved(pzl):
        return pzl

    i = pzl.find(".")
    new_pzls = [pzl[:i] + j + pzl[i + 1:] for j in size_table[dim]]
    for new_pzl in new_pzls:
        b_f = brute_force(new_pzl)
        if b_f:
            return b_f


if __name__ == '__main__':
    filename = 'puzzles.txt' if len(argv) == 1 else argv[1]
    puzzles = open(filename).read().splitlines()
    set_sizes(puzzles[0])
    start = time()
    for index, puzzle in enumerate(puzzles):
        solution = brute_force(puzzle)
        if index == 50:
            print(time() - start)
            break
        if solution is None:
            print("{0}: {1} => No Solution Possible".format(index, puzzle))
        else:
            print("{0}: {1} => {2}".format(index, puzzle, solution))
            print(check_sum(solution))
