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
        graph[i] = []
        for j in range(len(i)):
            for a in "abcdefghijklmnopqrstuvwxyz":
                new_word = i[:j] + a + i[j + 1:]
                if new_word in words and new_word != i:
                    graph[i].append(new_word)
                    if new_word in graph.keys():
                        graph[new_word].append(i)
                    else:
                        graph[new_word] = [i]

    end = time()-start
    print("Word count: {0}".format(str(len(words))))
    print("Edge count: {0}".format(
        str(sum([len(graph[i]) for i in graph.keys()]))))
    print("Degree list: {0}".format(degree_list(graph)))
    print("Construction time: %.2lfs" % end)

    return graph


def main():
    start = time()
    g = create_graph(start,open(sys.argv[1]).read().strip().splitlines())


if __name__ == "__main__":
    main()
