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
    return ret[0:ret.index(0,1)]


def create_graph(start, words):
    graph = {}
    for i in range(len(words)):
        graph[words[i]] = []
        for j in range(len(words)):
            if is_neighbor(words[i], words[j]):
                graph[words[i]].append(words[j])
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


def shortest_path(g,s,e, p=[]):
    p = p + [s]
    if s == e:
        return p

    shortest = []
    for elem in g[s]:
        if elem not in p:
            nP = shortest_path(g,elem,e,p)
            if nP:
                if not shortest or len(nP) < len(shortest):
                    shortest = nP
    return shortest


def cc(g):
    ccs = 0
    visited = []
    for i in g.keys():
        if i not in visited:
            visited.extend(bfs(g,i))
            ccs += 1
    return ccs, -1


def ks(g):
    k2 = 0
    for i in g.keys():
        for j in g[i]:
            if len(g[i]) == 1 and len(g[j]) == 1:
                k2+=1
    return k2,-1,-1


def backtrack(visited_nodes, goal):
    if len(visited_nodes) == 0:
        return [goal], 0
    path = [visited_nodes[goal]]
    for i in path:
        if i in visited_nodes.keys() and visited_nodes[i] != '':
            tmp = visited_nodes[i]
            path.append(tmp)
    return path[::-1] + [goal]


def bfs(graph,start,end=None):
    if start == end:
        return [start]

    parent = [start]
    visited = set()

    for elem in parent:
         for n in graph[elem]:
             if n not in visited:
                parent.append(n)
                visited.add(n)
    return list(visited)


def path(graph,start,end):
    if start == end:
        return [start]

    parent = [start]
    visited = {parent[0]: ''}

    for elem in parent:
        for n in graph[elem]:
            if n == elem:
                visited[n] = elem
                return backtrack(visited, end)
            elif n not in visited.keys():
                visited[n] = elem
                parent.append(n)
    return False


def p2(graph, arg1, arg2):
    print("Second degree word: {0}".format(second_degree(graph)))
    size, largest = cc(graph)
    k2,k3,k4 = ks(graph)
    print("Connected component size count: {0}".format(size))
    print("Largest component size: {0}".format(largest))
    print("K2 count: {0}".format(k2))
    print("K3 count: {0}".format(k3))
    print("K4 count: {0}".format(k4))
    print("Neighbors: {0}".format(" ".join(graph[arg1])))
    print("Shortest path: {0}".format(" ".join(path(graph,arg1,arg2))))


def main():
    start = time()
    g = create_graph(start, open(sys.argv[1]).read().strip().splitlines())
    if len(sys.argv) >3:
        p2(g, sys.argv[2], sys.argv[3])

    print(time()-start)


if __name__ == "__main__":
    main()
