from sys import argv
from math import sqrt

length, dim, col, row = 0,0,0,0


def string_to_pzl(p):
    pzls = [] # list of all rows, columns, and sub puzzles
    for i in range(0,length,dim): # populate rows
        tmp = []
        for j in range(i,i+dim):
            tmp.append(p[j])
        pzls.append(tmp)
    for i in range(0,dim): # populate columns
        tmp = []
        for j in range(i,length,dim):
            tmp.append(p[j])
        pzls.append(tmp)
    for i in range(0, length, dim*col):
        print(f"I: {i}")
        for j in range(i,i+row):
            print(f"J: {j}")
            tmp = []
            for k in range(j,dim*row,dim):
                print(f"K: {k}")
                tmp.append(p[k])
        pzls.append(tmp)
    return pzls


def is_invalid(p):
    puzzle_list = string_to_pzl(p)
    for pzl in range(len(puzzle_list)):
        for i in range(1, 10):
            if puzzle_list[pzl].count(str(i)) > 1:
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


def brute_force(pzl):
    if is_invalid(pzl):
        return ""
    if is_solved(pzl):
        return pzl

    i = pzl.find(".")
    new_pzls = [pzl[:i] + str(j) + pzl[i + 1:] for j in nums[question]]
    for new_pzl in new_pzls:
        b_f = brute_force(new_pzl, question)
        if b_f:
            return b_f


if __name__ == '__main__':
    filename = 'puzzles.txt' if len(argv) == 1 else argv[1]
    puzzles = open(filename).read().splitlines()
    set_sizes(puzzles[0])
    for index, puzzle in enumerate(puzzles):
        solution = brute_force(puzzle)
        if solution is None:
            print("{0}: {1} => No Solution Possible".format(index, puzzle))
        else:
            print("{0}: {1} => {2}".format(index, puzzle, solution))

