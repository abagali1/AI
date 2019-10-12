from sys import argv
from math import sin, cos, acos, pi

names = {}  # name -> station code
graph = {}  # station code -> [ (lat,long), [neighbors] ]


def backtrack(visited_nodes, goal):
    path = [visited_nodes[goal]]
    for i in path:
        if i in visited_nodes.keys() and visited_nodes[i] != '':
            path.append(visited_nodes[i])
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


def a_star(cities):
    global names, graph
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

    open_set, closed_set = [], {}
    h = gcd(graph[root][0][0], graph[root][0][1], graph[dest][0][0], graph[dest][0][1])
    open_set.append((0, h, root, ''))
    while open_set:
        elem = open_set.pop(0)
        if elem in closed_set:
            continue
        closed_set[elem] = elem[3]
        for nbr in graph[elem[2]][1]:
            if nbr == dest:
                return backtrack(closed_set, dest)
            else:
                h = gcd(graph[elem[2]][0][0], graph[elem[2]][0][1], graph[nbr][0][0], graph[nbr][0][1])
                open_set.append((elem[0]+1, h, nbr, elem[3]))
        if elem[0] + elem[1] != open_set[0][0] + open_set[0][1]:
            open_set.sort(key=lambda a: a[0]+a[1])


def gcd(x1, y1, x2, y2):
    x1 *= pi/180.0
    y1 *= pi/180.0
    x2 *= pi/180.0
    y2 *= pi/180.0
    return acos(sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1)) * 3958.76


def main():
    cities = argv[1:]
    load_table()
    print(a_star(cities))


if __name__ == '__main__':
    main()
