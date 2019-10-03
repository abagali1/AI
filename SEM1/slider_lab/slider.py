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
    orig, dest = {puzzle[x]: (x // dim, x) for x in range(len(puzzle))
                  }, {goal[x]: (x // dim, x) for x in range(len(goal))}
    return sum([abs((y[1]-dest[x][1])) + abs((y[0]-dest[x][0])) for x, y in orig.items()])


def solve(puzzle, goal):
    size = len(puzzle)
    start, dim = time(), int(sqrt(size))
    if not solveable(puzzle, size, dim):
        return -1, time()-start
    if puzzle == goal:
        return 0, time() - start
    parent, visited = [(mD(puzzle, goal, dim),puzzle)], {puzzle: ''}

    while parent:
        elem = parent.pop(0)
        for n in get_children(elem[1], dim):
            if n in visited:
                continue
            visited[n] = elem[1]
            parent += [(mD(n, goal, dim),n)]
            if n == goal:
                return steps(visited, goal, start)
        parent.sort()
    return -1, time() - start


def solveable(puzzle, size, dim):
    inversion_count = len([i for i in range(size) for j in range(i + 1, size) if puzzle[i] > puzzle[j]])
    pos = puzzle.index('_') // dim
    return inversion_count % 2 == 0 if size % 2 == 1 else inversion_count % 2 != pos % 2


def main():
    start_time = time()
    if len(argv) < 2:
        impossible_count, lengths, count, puzzle, goal = 0, 0, 0, [*"12345678_"], "12345678_"
        for i in range(500):
            if time()-start_time >= 90:
                break
            shuffle(puzzle)
            p = ''.join(puzzle)
            solved = solve(p, goal)
            if solved[0] == -1:
                impossible_count += 1
                print("Pzl {0}: {1} => unsolvable\tin %.2lfs".format(i, p) % solved[1])
            else:
                lengths += 9
                print("Pzl {0}: {1} => {2} steps\tin %.2lfs".format(i, p, solved[0]) % solved[1])
            count += 1
        print("Impossible count: {0}".format(impossible_count))
        print("Avg len for possibles: {0}".format(lengths / count - impossible_count))
        print("Solved {0} puzzles in %.2lfs".format(count) % (time() - start_time))
    elif len(argv) == 2:
        puzzles = open(argv[1]).read().splitlines()
        impossible_count, lengths, goal = 0, 0, puzzles[0]
        for i in range(len(puzzles)):
            p = puzzles[i]
            solved = solve(p, goal)
            if solved[0] == -1:
                impossible_count += 1
                print("Pzl {0}: {1} => unsolvable\tin %.2lfs".format(i, p) % solved[1])
            else:
                lengths += 9
                print("Pzl {0}: {1} => {2} steps\tin %.2lfs".format(i, p, solved[0]) % solved[1])
        p_l = len(puzzles)
        print("Impossible count: {0}".format(impossible_count))
        print("Avg len for possibles: {0}".format(lengths / p_l - impossible_count))
        print("Solved {0} puzzles in %.2lfs".format(p_l) % (time() - start_time))


if __name__ == '__main__':
    main()
