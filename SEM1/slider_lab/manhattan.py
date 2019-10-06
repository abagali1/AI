from sys import argv
from math import sqrt


def man_dist(puzzle, goal="12345678_"):
    dim = int(sqrt(len(puzzle)))
    return sum([abs(goal.find(puzzle[x]) - x) // dim for x in range(len(puzzle))])


def manhattan_distance(r, g):
    w = int(sqrt(len(r)))
    md = 0
    for i in range(len(r)):
        ig = g.index(r[i])
        md += abs(i//w - ig//w) + abs(i%w - ig%w)
    return md


if __name__ == '__main__':
    print("Manhattan distance: {0}".format(manhattan_distance(argv[1], argv[2]) if len(argv) > 2 else manhattan_distance(argv[1])))
