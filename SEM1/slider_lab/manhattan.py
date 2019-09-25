from sys import argv
from math import sqrt


def man_dist(puzzle, goal="12345678_"):
    dim = int(sqrt(len(puzzle)))
    start, end = [list(puzzle[i:i + dim]) for i in range(0, len(puzzle), dim)], [list(goal[i:i+dim]) for i in range(0,len(goal), dim)]


if __name__ == '__main__':
    print(man_dist(argv[0],argv[1]) if len(argv) > 2 else man_dist(argv[0]))