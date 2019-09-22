import sys
import time

alphabet = [*"abcdefghijklmnopqrstuvwxyz"]


def gen_swaps(word):
    ret = set()
    for w in range(len(word)):
        for a in alphabet:
            tmp = [*word[:]]
            tmp[w] = a
            tmp = ''.join(tmp)
            if tmp != word:
                ret.add(tmp)
    return ret


def create_graph(words):
    graph = {}
    for i in words:
        for j in gen_swaps(i):
            if j in words:
                if i not in graph.keys():
                    graph[i] = [j]
                else:
                    graph[i].append(j)

    print("Words: " + str(len(words)))
    print("Neighbor Pairs: " + str(len(words)/2))


def main():
    start = time.time()
    filename = sys.argv[1]
    with open(filename) as f:
        create_graph(f.read().strip().splitlines())
    print(time.time()-start)


if __name__ == "__main__":
    main()
