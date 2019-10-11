from sys import argv
from math import sin, cos, acos, pi

names = {}  # name -> station code
graph = {}  # station code -> [ (lat,long), [neighbors] ]


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
                root = tmp.strip()
            elif dest == '':
                dest = tmp.strip()
            tmp = ''
    print(f"ROOT: {names[root]} -> {graph[names[root]]}")
    print(f"DEST: {names[dest]} -> {graph[names[dest]]}")


def h(x1, y1, x2, y2):
    x1 *= pi/180.0
    y1 *= pi/180.0
    x2 *= pi/180.0
    y2 *= pi/180.0
    return acos(sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1)) * 3958.76


def main():
    cities = argv[1:]
    load_table()
    a_star(cities)


if __name__ == '__main__':
    main()
