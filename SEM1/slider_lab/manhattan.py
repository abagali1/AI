from sys import argv
from math import sqrt


def man_dist(puzzle, goal="12345678_"):
    dim = int(sqrt(len(puzzle)))
    return sum([abs(goal.find(puzzle[x]) - x) // dim for x in range(len(puzzle))])


if __name__ == '__main__':
    print("Manhattan distance: {0}".format(man_dist(argv[1], argv[2]) if len(argv) > 2 else man_dist(argv[1])))
