from sys import argv
from time import time
from math import sqrt
from random import shuffle

MAX_PATH = {
    3: 31,
    4: 82
}


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


def manhattan_distance(puzzle, goal, dim) -> int:
    md = 0
    for i in range(len(puzzle)):
        ig = goal.index(puzzle[i])
        md += abs(i//dim - ig//dim) + abs(i % dim - ig % dim)
    return md


def solve(puzzle, goal):
    start = time()
    if puzzle == goal:
        return 0, time() - start
    size = len(puzzle)
    dim = int(sqrt(size))
    if not solveable(puzzle, size, dim):
        return -1, time() - start

    open_set, closed_set = [[] for _ in range(MAX_PATH[dim])], {}
    f = manhattan_distance(puzzle, goal, dim)
    open_set[f].append(object=(puzzle, 0, ''))

    for index in range(len(open_set)):
        elem = open_set[index].pop(0)
        if elem[0] in closed_set:
            continue
        closed_set[elem[0]] = elem[2]
        for nbr in get_children(elem[0], dim):
            if nbr == goal:
                closed_set[nbr] = elem[0]
                return steps(closed_set, goal, start)
            open_set[manhattan_distance(
                nbr, goal, dim) + elem[1] + 1].append(object=(nbr, elem[1]+1, elem[0]) )


def solveable(puzzle, size, dim):
    pzl = puzzle.replace("_", "")
    inversion_count = len([i for i in range(size - 1)
                           for j in range(i + 1, size - 1) if pzl[i] > pzl[j]])
    pos = size - (puzzle.find("_") // dim)
    return not (inversion_count % 2) if size % 2 == 1 else not (inversion_count % 2) if pos % 2 == 1 else bool(
        inversion_count % 2)


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
            if time() - start_time >= 90:
                break
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

