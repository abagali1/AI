import sys
from time import time
from math import sqrt


def get_children(parent, d):
    index = parent[0].find('_')
    row = index // d
    neighbors = [i for i in [index+d, index-d] if 0 <= i < len(parent[0])]
    if (index + 1) // d == row:
        neighbors.append(index+1)
    if (index -1) //d  == row:
        neighbors.append(index-1)
    ret = gen_swaps(parent[0], neighbors, index, parent[1])
    return ret


def gen_swaps(p, n, i,l):
    true_neighbors = []
    for neighbor in n:
        temp = list(p[:])
        temp[i], temp[neighbor] = temp[neighbor], temp[i]
        true_neighbors.append((''.join(temp),l+1))
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
        return [goal], 0, dim

    parent = [(puzzle,0)]
    visited = {parent[0]: ''}
    distro = [0] * 100

    for elem in parent:
        neighbors = get_children(elem, dim)

        for n in neighbors:
            if n[0] == goal:
                visited[n] = elem
                return backtrack(visited, goal, dim)
            elif n[0] not in visited.keys():
                visited[n[0]] = elem
                parent.append(n)
            distro[n[1]] += 1

    distro[0] = 1
    distro = str(distro)
    distro = distro[:distro.find(", 0, 0")] + "]"

    print(f"DISTRO: {(distro)}")
    return ['NULL'], -1, dim


def print_formatted(solved, dimensions):
    for i in range(dimensions):
        for s in solved:
            print(s[dimensions * i:dimensions + (dimensions * i)], end="\t")
        print("")


def pop(arr,i):
    if i >= len(arr):
        return -1,-1
    return arr[i], i+1


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