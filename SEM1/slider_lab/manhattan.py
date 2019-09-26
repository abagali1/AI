from sys import argv
from math import sqrt


def man_dist(puzzle, goal="12345678_"):
    dim = int(sqrt(len(puzzle)))
    orig, dest = {puzzle[x]: (x // dim, x) for x in range(len(puzzle))}, {goal[x]: (x // dim, x) for x in range(len(goal))}
    return sum([abs((y[1]-dest[x][1])) + abs((y[0]-dest[x][0])) for x,y in orig.items()])


if __name__ == '__main__':
    print("Manhattan distance: {0}".format(man_dist(argv[1], argv[2]) if len(argv) > 2 else man_dist(argv[1])))
