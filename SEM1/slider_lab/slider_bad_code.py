import sys
from time import time
from math import sqrt


def get_children(parent, d):
    index = parent.find('_')
    row = index // d
    neighbors = [i for i in [index+d, index-d] if 0 <= i < len(parent)]
    if (index + 1) // d == row:
        neighbors.append(index+1)
    if (index -1) //d  == row:
        neighbors.append(index-1)
    true_neighbors = []
    for neighbor in neighbors:
        temp = list(parent[:])
        temp[index], temp[neighbor] = temp[neighbor], temp[index]
        true_neighbors.append(''.join(temp))
    return true_neighbors


def backtrack(visited_nodes, goal, d):
    if len(visited_nodes) == 0:
        return [goal], 0, d
    path = [visited_nodes[goal]]
    for i in path:
        if i in visited_nodes.keys() and visited_nodes[i] != '':
            tmp = visited_nodes[i]
            path.append(tmp)
    return path[::-1] + [goal], len(path)


def main():
    start_time = time()
    puzzle = sys.argv[1]
    goal = sys.argv[2] if len(sys.argv) > 2 else "12345678_"
    dim = int(sqrt(len(puzzle)))
    if puzzle == goal:
        for i in range(dim):
            for s in [goal]:
                print(s[dim * i:dim + (dim * i)], end="\t")
            print("")
        print("Steps: {0}".format(0))
        print("Time: %.2lfs" % (time() - start_time))
        return

    solved, steps = ['NULL'], -1
    parent = [puzzle]
    visited = {parent[0]: ''}
    index = 0
    while parent:
        if index < len(parent):
            elem, index = parent[index], index + 1
        else:
            for i in range(dim):
                for s in [puzzle]:
                    print(s[dim * i:dim + (dim * i)], end="\t")
                print("")
            print("Steps: -1")
            print("Time: %.2lfs" % (time() - start_time))
            return
        neighbors = get_children(elem,dim)
        for n in neighbors:
            if n == goal:
                visited[n] = elem
                solved, steps = backtrack(visited,goal,dim)
                arr = [solved[0][i:i + 12] for i in range(0, len(solved[0]), 12)]
                for x in arr:
                    for i in range(dim):
                        for s in x:
                            print(s[dim * i:dim + (dim * i)], end="\t")
                        print("")
                print("Steps: {0}".format(steps))
                print("Time: %.2lfs" % (time() - start_time))
                return
            elif n not in visited.keys():
                visited[n] = elem
                parent.append(n)
    for i in range(dim):
        for s in [puzzle]:
            print(s[dim * i:dim + (dim * i)], end="\t")
        print("")
    print("Steps: -1")
    print("Time: %.2lfs" % (time() - start_time))
    return


if __name__ == '__main__':
    main()