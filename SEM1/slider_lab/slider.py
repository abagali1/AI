import sys
import time


def backtrack(visited_nodes, goal):
    if len(visited_nodes) == 0:
        return [goal], 0
    path = [visited_nodes[goal]]
    for i in path:
        if i in visited_nodes.keys() and visited_nodes[i] != '':
            tmp = visited_nodes[i]
            path.append(tmp)
    return path[::-1], len(path)


def gen_swaps(p, n, i):
    true_neighbors = []
    for neighbor in n:
        temp = [row[:] for row in p]
        temp[i[0]][i[1]], temp[neighbor[0]][neighbor[1]] = temp[neighbor[0]][neighbor[1]], temp[i[0]][i[1]]
        true_neighbors.append(temp)
    return true_neighbors


def get_children(parent):
    index = [(index, row.index('_')) for index, row in enumerate(parent) if '_' in row][0]
    neighbors = [(x, y) for x, y in [(index[0], index[1] - 1), (index[0], index[1] + 1), (index[0] + 1, index[1]),
                                     (index[0] - 1, index[1])] if
                 0 <= x < len(parent) and 0 <= y < len(parent[0])]
    return [(''.join(str(item) for inList in m for item in inList)) for m in gen_swaps(parent, neighbors, index)]


def solve(puzzle, goal="12345678_"):
    if puzzle == goal:
        return backtrack({}, goal)
    parent = [puzzle]
    visited = {parent[0]: ''}

    while parent:
        elem = parent.pop(0)
        neighbors = get_children([list(elem[0:3]), list(elem[3:6]), list(elem[6:9])])
        for n in neighbors:
            if n == goal:
                visited[''.join([str(item) for i in n for item in i])] = elem
                return backtrack(visited, goal)
            elif n not in visited.keys():
                visited[''.join([str(item) for i in n for item in i])] = elem
                parent.append(n)
    return ['NULL'], -1


def main():
    try:
        puzzle = sys.argv[1]
    except IndexError:
        print("Usage: \"python3 slider.py <puzzle> <goal(optional)>\"")
        print("Missing Puzzle Parameter")
        return

    try:
        goal = sys.argv[2]
    except IndexError:
        goal = None

    start_time = time.time()
    if not goal:
        solved = solve(puzzle)
        print("Steps: %d" % solved[1])
    else:
        solved = solve(puzzle, goal)
        print("Steps: %d" % solved[1])
    print("Time: %ds" % (time.time() - start_time))


if __name__ == '__main__':
    main()
