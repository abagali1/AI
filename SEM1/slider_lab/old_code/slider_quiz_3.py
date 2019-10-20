import sys
from math import sqrt


def get_children(parent, d):
    index = parent.find('_')
    row = index // d
    neighbors = [i for i in [index+d, index-d] if 0 <= i < len(parent)]
    if (index + 1) // d == row:
        neighbors.append(index+1)
    if (index - 1) // d == row:
        neighbors.append(index-1)
    return gen_swaps(parent, neighbors, index)


def gen_swaps(p, n, i):
    true_neighbors = []
    for neighbor in n:
        temp = list(p[:])
        temp[i], temp[neighbor] = temp[neighbor], temp[i]
        true_neighbors.append(''.join(temp))
    return true_neighbors


def find_path_length(visited_nodes, goal, d):
    if len(visited_nodes) == 0:
        return [goal], 0, d
    path = [visited_nodes[goal]]
    for i in path:
        if i in visited_nodes.keys() and visited_nodes[i] != '':
            tmp = visited_nodes[i]
            path.append(tmp)
    return path


def bfs(start, end=None):
    dim = int(sqrt(len(start)))
    if start == end:
        return [start]

    parent = [start]
    visited = {start: ''}
    visited_set = set()
    visited_set.add(start)

    for elem in parent:
        for n in get_children(elem, dim):
            if n not in visited:
                parent.append(n)
                visited[n] = elem
                visited_set.add(n)
    m_path = [(x, find_path_length(visited, x, dim)) for x in visited.keys()]
    return m_path[1:]


if __name__ == '__main__':
    pathz = bfs(sys.argv[1])
    m = len([len(x[1]) for x in pathz])
    hardest = [x[0] for x in pathz if len(x[1]) == m]
    d = len([x for x in pathz if len(x[1]) == 10])
    print("MAX: {0}".format(m))
    print("HARDEST: {0}".format(hardest))
    print("NUM_D: {0}".format(d))
    count = 1
    for pos, i in enumerate(pathz):
        if i[0].find("_") == 4:
            continue
        is_valid = True
        for j in i[1]:
            if j.index("_") == 4:
                is_valid = False
                break
        if is_valid:
            count += 1
    print(count)

