from sys import argv
from math import sqrt


def man_dist(puzzle, goal="12345678_"):
    dim = int(sqrt(len(puzzle)))
    return sum([abs(goal.find(puzzle[x]) - x) // dim for x in range(len(puzzle))])


def manhattan_distance(r, g):
    w = 4
    lr = [*r]
    count = 0
    for i in range(len(lr)):
        indg = g.index(str(lr[i]))
        count += abs(indg - i) // w
    return count


if __name__ == '__main__':
    print("Manhattan distance: {0}".format(manhattan_distance(argv[1], argv[2]) if len(argv) > 2 else manhattan_distance(argv[1])))
