import sys
from time import time


def degree_list(graph):
    ret = [0] * len(graph)
    for x, y in graph.items():
        ret[len(y)] += 1
    return ret


def create_graph(start, words):
    graph = {}

    for i in words:
        graph[i] = set()
        e = 0
        wl = list(i)
        for j in range(len(i)):
            original = wl[j]
            for letter in "abcdefghijklmnopqrstuvwxyz":
                wl[j] = letter
                nw = ''.join(wl)
                if nw in words:
                    graph[i].add(nw)
                    if nw in graph.keys():
                        graph[nw].add(i)
                    else:
                        graph[nw] = {i}
                    e += 1
                wl[j] = original

    end = time()-start
    print("Word count: {0}".format(str(len(words))))
    print("Edge count: {0}".format(e))
    #print("Edge count: {0}".format(
    #    str(sum([len(graph[i]) for i in graph.keys()]))))
    #print("Degree list: {0}".format(degree_list(graph)))
    print("Construction time: %.2lfs" % end)

    return graph


def main():
    start = time()
    g = create_graph(start,open(sys.argv[1]).read().strip().splitlines())


if __name__ == "__main__":
    main()
