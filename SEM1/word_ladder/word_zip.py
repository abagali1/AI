import sys
import time

alphabet = [*"abcdefghijklmnopqrstuvwxyz"]


def is_neighbor(word1,word2):
    return len([x for x,y in zip(word1,word2) if x != y]) == 1


def create_graph(words):
    graph = {}
    for i in range(len(words)):
        for j in range(len(words)):
            if is_neighbor(words[i],words[j]):
                if i not in graph.keys():
                    graph[i] = set(words[j])
                else:
                    graph[i].add(words[j])


def main():
    start = time.time()
    filename = sys.argv[1]
    with open(filename) as f:
        create_graph(f.read().strip().splitlines())
    print(time.time()-start)


if __name__ == "__main__":
    main()
