from sys import argv
from time import time
from math import sqrt


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


def solve(puzzle, goal):
    start = time()
    dim = int(sqrt(len(puzzle)))
    if puzzle == goal:
        return 0, time() - start

    parent = [puzzle]
    visited = {parent[0]: ''}

    for elem in parent:
        neighbors = get_children(elem, dim)
        for n in neighbors:
            if n == goal:
                visited[n] = elem
                return steps(visited, goal, start)
            elif n not in visited.keys():
                visited[n] = elem
                parent.append(n)
    return -1, time() - start


def pop(arr, i):
    if i >= len(arr):
        return -1, -1
    return arr[i], i + 1


def solveable(puzzle, goal):
    return True


def main():
    start_time = time()
    puzzles = open(argv[1]).read().splitlines()
    i_c = 0
    lengths = 0
    for i in range(len(puzzles)):
        goal = "ABCDEFGHIJKLMNO_" if "eckel" in argv[1].lower() else puzzles[1]
        p = puzzles[i]
        if solveable(p, goal):
            solved = solve(p, goal)
            lengths += len(p)
            print("Pzl {0}: {1} => {2} steps\tin %.2lfs".format(i, p, solved[0]) % solved[1])
        else:
            i_c += 1
    p_l = len(puzzles)
    print("Impossible count: {0}".format(i_c))
    print("Avg len for possibles: {0}".format(lengths / p_l - i_c))
    print("Solved {0} puzzles in %.2lfs".format(p_l) % (time()-start_time))


if __name__ == '__main__':
    main()
