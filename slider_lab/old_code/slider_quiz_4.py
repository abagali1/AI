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
    return path + [goal]


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

    m_path = []
    for x in visited.keys():
        path = find_path_length(visited,x, dim)
        m_path.append((x, len(path), path))
    return m_path[1:]


if __name__ == '__main__':
    corner, edge, middle = bfs("12345678_"), bfs("1234567_8"), bfs("1234_6758")
    d_p = {x:0}
    print(len(corner), len(edge), len(middle))



