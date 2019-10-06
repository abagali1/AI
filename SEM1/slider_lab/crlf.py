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


def manhattan_distance(puzzle, goal, dim):
    return sum([abs(goal.find(puzzle[x]) - x) // dim for x in range(len(puzzle))])


def solve(root, goal):
    width = len(root)**.5
    if root == goal:
        return [root]
    if impossible(root, goal):
        return []
    openSet = [(h(root, goal, width), 0, root, "")]
    closedSet = {}
    while openSet:
        openSet.sort()
        g, h, pzl, parent = openSet.pop()
        if pzl in closedSet:
            continue
        closedSet[pzl] = parent
        for nbr in neighbor(pzl):
            print("here")
            if nbr == goal:
                print(closedSet)
            if nbr in closedSet:
                continue
            openSet.append((h(nbr, goal, width), h+1, nbr, pzl))


def solveable(puzzle, size, dim):
    pzl = puzzle.replace("_", "")
    inversion_count = len([i for i in range(size - 1)
                           for j in range(i + 1, size - 1) if pzl[i] > pzl[j]])
    pos = size - (puzzle.find("_") // dim)
    return not (inversion_count % 2) if size % 2 == 1 else not (inversion_count % 2) if pos % 2 == 1 else bool(
        inversion_count % 2)


def main():
    start_time = time()
    puzzles = open(argv[1]).read().splitlines()
    impossible_count, lengths, goal = 0, 0, puzzles[0]
    for i in range(len(puzzles)):
        p = puzzles[i]
        solved = solve(p, goal)
        print(solved)


if __name__ == '__main__':
    main()
