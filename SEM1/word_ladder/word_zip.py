import sys
from time import time


def is_neighbor(word1, word2):
    count = 0
    for x, y in zip(word1, word2):
        if x != y:
            count += 1
        if count > 1:
            return False
    return count == 1


def degree_list(graph):
    ret = [0] * len(graph)
    for x, y in graph.items():
        ret[len(y)] += 1
    return list(ret[0:ret.index(0, 1)])


def create_graph(start, words):
    graph = {}
    for i in range(len(words)):
        graph[words[i]] = set()
        for j in range(len(words)):
            if is_neighbor(words[i], words[j]):
                graph[words[i]].add(words[j])

    end = time()-start
    print("Word count: {0}".format(str(len(words))))
    print("Edge count: {0}".format(
        str(sum([len(graph[i]) for i in graph.keys()])//2)))
    print("Degree list: {0}".format(degree_list(graph)))
    print("Construction time: %.2lfs" % end)

    return graph


def second_degree(g):
    sM = sorted(set(len(y) for y in g.values()))[-2]
    for x, y in g.items():
        if len(y) == sM:
            return x


def cc(g):
    ccs = set()
    visited = set()
    v = []
    for x in g.keys():
        if x not in visited:
            tmp = bfs(g, x)
            visited = visited.union(tmp)
            v.append(tmp)
            ccs.add(len(tmp))
    return len(ccs), max([len(x) for x in v]), v


def ks(g, s):
    k2 = len([x for x in s if len(x) == 2])
    ccs_3 = [x for x in s if len(x) == 3]
    ccs_4 = [x for x in s if len(x) == 4]
    k3 = 0
    k4 = 0
    for i in ccs_3:
        for j in i:
            if len(g[j]) == 2:
                k3 += 1
    for i in ccs_4:
        for j in i:
            if len(g[j]) == 3:
                k4 += 1

    return k2, k3//6, k4//8


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
    return ['no path']


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
