from sys import argv
from math import sin, cos, acos, pi
from heapq import heappush, heappop

names = {}  # name -> station code
graph = {}  # station code -> [ (lat,long), [neighbors] ]


def backtrack(visited_nodes, goal):
    path = [visited_nodes[goal]]
    for i in path:
        if i in visited_nodes.keys() and visited_nodes[i] != '':
            path.append(visited_nodes[i])
    path.append(goal)
    return path


def load_table():
    global names, graph
    names = {' '.join(x.split(" ")[1:]): x.split(" ")[0]
             for x in open('rrNodeCity.txt').read().splitlines()}
    for x in open('rrNodes.txt').read().splitlines():
        parts = x.split(" ")
        graph[parts[0]] = [(float(parts[1]), float(parts[2])), []]
    for x in open("rrEdges.txt").read().splitlines():
        parts = x.split(" ")
        graph[parts[0]][1].append(parts[1])
        graph[parts[1]][1].append(parts[0])


def a_star(root, dest):
    if root == dest:
        return root

    open_set, closed_set = [], {}
    h = gcd(graph[root][0][0], graph[root][0][1], graph[dest][0][0], graph[dest][0][1])
    open_set.append((0, h, root, ''))
    while open_set:
        g, h, elem, parent = heappop(open_set)
        if elem in closed_set:
            continue
        closed_set[elem] = parent
        for nbr in graph[elem][1]:
            if nbr == dest:
                closed_set[nbr] = parent
                final_h = gcd(graph[nbr][0][0], graph[nbr][0][1], graph[parent][0][0],graph[parent][0][1]) + g
                return backtrack(closed_set, dest), final_h
            else:
                h = gcd(graph[elem][0][0], graph[elem][0][1], graph[nbr][0][0], graph[nbr][0][1])
                heappush(open_set,(g+h, h, nbr, elem))



def gcd(x1, y1, x2, y2):
    x1 *= pi/180.0
    y1 *= pi/180.0
    x2 *= pi/180.0
    y2 *= pi/180.0
    return acos(sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1)) * 3958.76


def strip_cities(cities):
    root, dest = '', ''
    tmp = ''
    for x in range(len(cities)):
        tmp += cities[x] + " "
        if tmp.strip() in names:
            if root == '':
                root = names[tmp.strip()]
            elif dest == '':
                dest = names[tmp.strip()]
            tmp = ''
    return root, dest


def main():
    load_table()
    start, end = strip_cities(argv[1:])
    path = a_star(end,start)
    print(len(path[0]), path[1])


if __name__ == '__main__':
    main()
