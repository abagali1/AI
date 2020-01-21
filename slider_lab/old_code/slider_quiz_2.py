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
    return len(path)


def bfs(start, end=None):
    dim = int(sqrt(len(start)))
    if start == end:
        return [start]

    parent = [start]
    visited = {start: ''}

    for elem in parent:
        for n in get_children(elem, dim):
            if n not in visited:
                parent.append(n)
                visited[n] = elem
    m_path = [(x, find_path_length(visited, x, dim)) for x in visited.keys()]
    return m_path


if __name__ == '__main__':
    pathz = bfs(sys.argv[1])
    m = max([x[1] for x in pathz])
    hardest = [x[0] for x in pathz if x[1] == m]
    print(f"{m}\n{hardest}")
