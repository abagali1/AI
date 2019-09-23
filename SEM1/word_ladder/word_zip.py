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
    _max = max([len(y) for x,y in graph.items()])
    print("MAX: {0}".format(_max))
    ret = [0] * _max
    for i in range(0,_max):
        for x,y in graph.items():
            if len(y) == i:
                ret[i] += 1
    return ret


def create_graph(start, words):
    graph = {}
    for i in range(len(words)):
        for j in range(i+1, len(words)):
            if is_neighbor(words[i], words[j]):
                if words[i] not in graph.keys():
                    graph[words[i]] = [words[j]]
                else:
                    graph[words[i]].append(words[j])
    end = time()-start
    print("Word count: {0}".format(str(len(words))))
    print("Edge count: {0}".format(
        str(sum([len(graph[i]) for i in graph.keys()]))))
    print("Degree list: {0}".format(degree_list(graph)))
    print("Construction time: %.2lfs" % (end))

    return graph


def main():
    start = time()
    filename = sys.argv[1]
    with open(filename) as f:
        g = create_graph(start, f.read().strip().splitlines())
    print(time()-start)


if __name__ == "__main__":
    main()
