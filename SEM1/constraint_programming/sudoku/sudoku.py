from sys import argv
from math import sqrt


def string_to_pzl(p, dim, size):
    pzls = []
    for i in range(0,size,dim):
        for j in range(i,i+dim):
            tmp = []
            tmp.append(p[j])
        pzls.append(tmp)
    for i in range(0,dim):
        for j in range(i,size,dim):
            tmp = []
            tmp.append(p[j])
        pzls.append(tmp)
    return pzls



def is_invalid(p, q):
    puzzle_list = string_to_pzl(p, int(sqrt(len(p)), len(p))
    for pzl in range(len(puzzle_list)):
        for i in range(1, 10):
            if puzzle_list[pzl].count(str(i)) > 1:
                return True
    return False


def is_solved(pzl, question):
    return False if pzl.find(".") != -1 else True


def brute_force(pzl, question):
    if is_invalid(pzl, question):
        return ""
    if is_solved(pzl, question):
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
    for index, puzzle in enumerate(puzzles):
        solution = brute_force(puzzle)
        if solution is None:
            print("{0}: {1} => No Solution Possible".format(index, puzzle)
        else:
            print("{0}: {1} => {2}".format(index, puzzle, solution)

