import sys
from time import time
from math import sqrt


def get_children(parent):
    index = [(index, row.index('_')) for index, row in enumerate(parent) if '_' in row][0]
    neighbors = [(x, y) for x, y in [(index[0], index[1] - 1), (index[0], index[1] + 1), (index[0] + 1, index[1]), (index[0] - 1, index[1])] if 0 <= x < len(parent) and 0 <= y < len(parent[0])]
    return [(''.join(str(item) for inList in m for item in inList)) for m in gen_swaps(parent, neighbors, index)]


def gen_swaps(p, n, i):
    true_neighbors = []
    for neighbor in n:
        temp = [row[:] for row in p]
        temp[i[0]][i[1]], temp[neighbor[0]][neighbor[1]] = temp[neighbor[0]][neighbor[1]], temp[i[0]][i[1]]
        true_neighbors.append(temp)
    return true_neighbors


def backtrack(visited_nodes, goal, d):
    if len(visited_nodes) == 0:
        return [goal], 0, d
    path = [visited_nodes[goal]]
    for i in path:
        if i in visited_nodes.keys() and visited_nodes[i] != '':
            tmp = visited_nodes[i]
            path.append(tmp)
    return path[::-1] + [goal], len(path), d


def solve(puzzle, goal="12345678_"):
    dim = int(sqrt(len(puzzle)))
    if puzzle == goal:
        return backtrack({}, goal, dim)
    parent = [puzzle]
    visited = {parent[0]: ''}
    index = 0

    while parent:
        elem, index = pop(parent, index)
        if elem == -1:
            break
        neighbors = get_children([list(elem[i:i + 6]) for i in range(0, len(elem), dim)])
        for n in neighbors:
            key = ''.join([str(item) for i in n for item in i])
            if n == goal:
                visited[key] = elem
                return backtrack(visited, goal, dim)
            elif n not in visited.keys():
                visited[key] = elem
                parent.append(n)
    return ['NULL'], -1, dim


def print_formatted(solved, dimensions):
    for i in range(dimensions):
        for s in solved:
            print(s[dimensions * i:dimensions + (dimensions * i)], end="\t")
        print("")


def pop(arr, i):
    if i >= len(arr):
        return -1, -1
    return arr[i], i + 1


def main():
    puzzle = sys.argv[1]
    goal = sys.argv[2] if len(sys.argv) > 2 else None

    start_time = time()
    if not goal:
        solved = solve(puzzle)
        if solved[1] != -1:
            arr = [solved[0][i:i + 12] for i in range(0, len(solved[0]), 12)]
            for i in arr:
                print_formatted(i, solved[2])
        else:
            print_formatted([puzzle], solved[2])
        print("Steps: {0}".format(solved[1]))
    else:
        solved = solve(puzzle, goal)
        if solved[1] != -1:
            arr = [solved[0][i:i + 12] for i in range(0, len(solved[0]), 12)]
            for i in arr:
                print_formatted(i, solved[2])
        else:
            print_formatted([puzzle], solved[2])
        print("Steps: {0}".format(solved[1]))
    print("Time: %.2lfs" % (time() - start_time))


if __name__ == '__main__':
    main()
