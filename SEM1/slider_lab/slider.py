from sys import argv
from time import time
from math import sqrt
from random import shuffle


def get_children(parent, d):
    index = parent.find('_')
    row = index // d
    neighbors = [i for i in [index + d, index - d] if 0 <= i < len(parent)]
    if (index + 1) // d == row:
        neighbors.append(index + 1)
    if (index - 1) // d == row:
        neighbors.append(index - 1)
    return gen_swaps(parent, neighbors, index)


def gen_swaps(p, n, i):
    true_neighbors = []
    for neighbor in n:
        temp = list(p[:])
        temp[i], temp[neighbor] = temp[neighbor], temp[i]
        true_neighbors.append(''.join(temp))
    return true_neighbors


def steps(visited_nodes, goal, s):
    path = [visited_nodes[goal]]
    for i in path:
        if i in visited_nodes.keys() and visited_nodes[i] != '':
            tmp = visited_nodes[i]
            path.append(tmp)
    return len(path), time() - s


def mD(puzzle, goal, dim):
    return sum([abs(goal.find(puzzle[x]) - x) // dim for x in range(len(puzzle))])


def solve(puzzle, goal):
    start = time()
    if puzzle == goal:
        return 0, time() - start
    size = len(puzzle)
    dim = int(sqrt(size))
    if not solveable(puzzle, size, dim):
        return -1, time() - start

    open_set, closed_set = [(0 + mD(puzzle, goal, dim), puzzle, '')], {puzzle: ('', 0)}

    while open_set:
        elem = open_set.pop(0)
        if elem[1] in closed_set:
            continue
        closed_set[elem[1]] = ()
        for nbr in get_children(elem[1], dim):
            if nbr == goal:
                return steps(closed_set, goal, start)
            open_set.append((mD(nbr, goal, dim) + 1, nbr, elem))  # add distances
            open_set.sort(key=lambda x: x[0])


def solveable(puzzle, size, dim):
    inversion_count = len([i for i in range(size)
                           for j in range(i + 1, size) if puzzle[i] > puzzle[j]])
    pos = puzzle.index('_') // dim
    return inversion_count % 2 == 0 if size % 2 == 1 else inversion_count % 2 != pos % 2


def main():
    start_time = time()
    if len(argv) < 2:
        impossible_count, lengths, count, puzzle, goal = 0, 0, 0, [
            *"12345678_"], "12345678_"
        for i in range(500):
            if time() - start_time >= 90:
                break
            shuffle(puzzle)
            p = ''.join(puzzle)
            solved = solve(p, goal)
            if solved[0] == -1:
                impossible_count += 1
                print("Pzl {0}: {1} => unsolvable\tin %.2lfs".format(
                    i, p) % solved[1])
            else:
                lengths += 9
                print("Pzl {0}: {1} => {2} steps\tin %.2lfs".format(
                    i, p, solved[0]) % solved[1])
            count += 1
        print("Impossible count: {0}".format(impossible_count))
        print("Avg len for possibles: {0}".format(
            lengths / count - impossible_count))
        print("Solved {0} puzzles in %.2lfs".format(count) %
              (time() - start_time))
    elif len(argv) == 2:
        puzzles = open(argv[1]).read().splitlines()
        impossible_count, lengths, goal = 0, 0, puzzles[0]
        for i in range(len(puzzles)):
            p = puzzles[i]
            solved = solve(p, goal)
            if solved[0] == -1:
                impossible_count += 1
                print("Pzl {0}: {1} => unsolvable\tin %.2lfs".format(
                    i, p) % solved[1])
            else:
                lengths += 9
                print("Pzl {0}: {1} => {2} steps\tin %.2lfs".format(
                    i, p, solved[0]) % solved[1])
        p_l = len(puzzles)
        print("Impossible count: {0}".format(impossible_count))
        print("Avg len for possibles: {0}".format(
            lengths / p_l - impossible_count))
        print("Solved {0} puzzles in %.2lfs".format(p_l) %
              (time() - start_time))


if __name__ == '__main__':
    main()
