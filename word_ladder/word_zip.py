import sys
from time import time

alpha = [*"abcdefghijklmnopqrstuvwxyz"]


def create_graph(start, words):
    graph, e = {}, 0
    for i in words:
        graph[i] = set()
        w = [*i]
        for j in [0, 1, 2, 3, 4, 5]:
            orig = w[j]
            for a in alpha:
                if a == orig:
                    continue
                else:
                    w[j] = a
                    tmp = ''.join(w)
                    if tmp in graph:
                        graph[i].add(tmp)
                        graph[tmp].add(i)
                        e += 1
                    w[j] = orig

    end = time() - start
    ret = [0] * len(graph)
    for x, y in graph.items():
        ret[len(y)] += 1
    dg = list(ret[0:ret.index(0, 1)])

    print("Word count: {0}".format(len(words)))
    print("Edge count: {0}".format(e))
    print("Degree list: {0}".format(dg))
    print("Construction time: %.2lfs" % end)

    return graph


def second_degree(g):
    sM = sorted(set(len(y) for y in g.values()))[-2]
    for x, y in g.items():
        if len(y) == sM:
            return x


def cc(g):
    ccs, visited, v = set(), set(), []
    for x in g.keys():
        if x not in visited:
            tmp = bfs(g, x)
            visited = visited | tmp
            v.append(tmp)
            ccs.add(len(tmp))
    return len(ccs), max([len(x) for x in v]), v


def ks(g, s):
    k2, k3, k4 = 0, 0, 0
    for x in s:
        if len(x) == 2:
            k2 += 1
        elif len(x) == 3:
            for j in x:
                if len(g[j]) == 2:
                    k3 += 1
        elif len(x) == 4:
            for j in x:
                if len(g[j]) == 3:
                    k4 += 1
    return k2, k3 // 6, k4 // 8 - 1


def backtrack(visited_nodes, goal):
    if len(visited_nodes) == 0:
        return [goal], 0
    path = [visited_nodes[goal]]
    for i in path:
        if i in visited_nodes.keys() and visited_nodes[i] != '':
            tmp = visited_nodes[i]
            path.append(tmp)
    return path[::-1] + [goal]


def bfs(graph, start, end=None):
    if start == end:
        return [start]

    parent = [start]
    visited = set()

    for elem in parent:
        for n in graph[elem]:
            if n not in visited:
                parent.append(n)
                visited.add(n)
    return visited


def path(graph, start, end):
    if start == end:
        return [start]

    parent = [start]
    visited = {parent[0]: ''}

    for elem in parent:
        for n in graph[elem]:
            if n == end:
                visited[n] = elem
                return backtrack(visited, end)
            elif n not in visited.keys():
                visited[n] = elem
                parent.append(n)
    return ['no', 'path']


def farthest(g, ccs, w1):
    paths = []
    for i in ccs:
        if w1 in i:
            for node in i:
                paths.append(path(g, w1, node))

    tmp = [len(x) for x in paths]
    max1 = max(tmp)
    return paths[tmp.index(max1)][-1]


def p2(graph, arg1, arg2):
    print("Second degree word: {0}".format(second_degree(graph)))
    sP = path(graph, arg1, arg2)
    size, largest, stuff = cc(graph)
    k2, k3, k4 = ks(graph, stuff)
    f = farthest(graph, stuff, arg1)
    print("Connected component size count: {0}".format(size))
    print("Largest component size: {0}".format(largest))
    print("K2 count: {0}".format(k2))
    print("K3 count: {0}".format(k3))
    print("K4 count: {0}".format(k4))
    print("Neighbors: {0}".format(" ".join(graph[arg1])))
    print("Farthest: {0}".format(f))
    print("Path: {0}".format(" ".join(sP)))


def main():
    start = time()
    g = create_graph(start, open(sys.argv[1]).read().strip().splitlines())
    if len(sys.argv) > 3:
        p2(g, sys.argv[2], sys.argv[3])

    print("Time used: %.2lfs" % (time() - start))


if __name__ == "__main__":
    main()
