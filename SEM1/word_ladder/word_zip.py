import sys
from time import time


def is_neighbor(word1,word2):
    return len([x for x,y in zip(word1,word2) if x != y]) == 1


def create_graph(start, words):
    graph = {}
    for i in range(len(words)):
        for j in range(i+1, len(words)):
            if is_neighbor(words[i],words[j]):
                if words[i] not in graph.keys():
                    graph[words[i]] = [words[j]]
                else:
                    graph[words[i]].append(words[j])
    # print("Word count: {0}".format(str(len(words))))
    # print("Edge count: {0}".format(str(sum([len(graph[i]) for i in graph.keys()]))))
    # print("Construction time: %.2lfs" % (time()-start))

    return graph


def main():
    start = time()
    filename = sys.argv[1]
    with open(filename) as f:
        g = create_graph(start, f.read().strip().splitlines())
    print(time()-start)


if __name__ == "__main__":
    main()
