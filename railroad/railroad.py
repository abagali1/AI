from random import randint
from sys import argv, exit
from time import sleep
from math import sin, cos, acos, pi
from heapq import heappush, heappop
from tkinter import *


names = {}  # name -> station code
codes = {}  # station code -> name
graph = {}  # station code -> [ (lat,long), [neighbors] ]
edges = []  # list of lists of tuples (specific to pyplot)
PATH_COLOR, FRINGE_COLOR, CLOSED_COLOR, FINAL_COLOR, BACKGROUND_COLOR = 'white', 'deep pink', 'green2', 'yellow', 'black'
LINE_WIDTH = 2


def backtrack(ROOT, canvas, visited_nodes, goal, f):
    path = [visited_nodes[goal]]
    for i in path:
        if i[0] in visited_nodes.keys() and visited_nodes[i[0]] != '':
            path.append(visited_nodes[i[0]])
    path = list(reversed(path))
    path.append((goal, f))
    for i in range(1, len(path)-1):
        if path[i-1][0] != '':
            line(canvas, graph[path[i-1][0]][0][0], graph[path[i-1][0]][0][1], graph[path[i][0]][0][0], graph[path[i][0]][0][1],
                 FINAL_COLOR, width=4)
    ROOT.update()
    return path


def load_table():
    global names, graph, codes
    names = {' '.join(x.split(" ")[1:]): x.split(" ")[0]
             for x in open('rrNodeCity.txt').read().splitlines()}
    codes = dict((y, x) for x, y in names.items())

    for x in open('rrNodes.txt').read().splitlines():
        parts = x.split(" ")
        graph[parts[0]] = [(float(parts[2]), float(parts[1])), []]
    for x in open("rrEdges.txt").read().splitlines():
        parts = x.split(" ")
        graph[parts[0]][1].append(parts[1])
        graph[parts[1]][1].append(parts[0])
    for i in graph:
        for n in graph[i][1]:
            edges.append([graph[i][0], graph[n][0]])


def load_map():
    ROOT = Tk()
    ROOT.title("railroad")
    canvas = Canvas(ROOT, background=BACKGROUND_COLOR)
    draw_edges(ROOT, canvas)

    return ROOT, canvas


def draw_edges(r, c):
    r.geometry("950x950")
    c.pack(fill=BOTH, expand=1)
    for i in edges:
        line(c, i[0][0], i[0][1], i[1][0], i[1][1], PATH_COLOR)
    r.update()


def line(c, x1, y1, x2, y2, color, **kwargs):
    x1, y1, x2, y2 = float(x1), float(y1), float(x2), float(y2)
    c.create_line((x1)*10+1500, (50-y1)*10+400, (x2)
                  * 10+1500, (50-y2)*10+400, fil=color, **kwargs)


def a_star(ROOT, canvas, root, dest):
    if root == dest:
        return root

    open_set, closed_set = [], {}
    h = gcd(graph[root][0][0], graph[root][0][1],
            graph[dest][0][0], graph[dest][0][1])
    open_set.append((h, 0, h, root, ''))
    while open_set:
        f, g, h, elem, parent = heappop(open_set)
        if parent != '':
            line(canvas, graph[elem][0][0], graph[elem][0][1], graph[parent][0][0], graph[parent][0][1],
                 CLOSED_COLOR, width=LINE_WIDTH)
        if elem in closed_set:
            continue
        else:
            closed_set[elem] = (parent, g)
        for nbr in graph[elem][1]:
            if nbr == dest:
                closed_set[nbr] = (parent, g)
                return backtrack(ROOT, canvas, closed_set, dest, f), f
            else:
                new_g = g + gcd(graph[elem][0][0], graph[elem][0][1],
                                graph[nbr][0][0], graph[nbr][0][1])
                new_h = gcd(graph[nbr][0][0], graph[nbr][0][1],
                            graph[dest][0][0], graph[dest][0][1])
                heappush(open_set, (new_g+new_h, new_g, new_h, nbr, elem))
                if nbr not in closed_set:
                    line(canvas, graph[nbr][0][0], graph[nbr][0][1], graph[elem][0][0], graph[elem][0][1],
                         FRINGE_COLOR, width=LINE_WIDTH)
        if randint(0, int(f)) <= 15:
            ROOT.update()


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
    if len(argv) < 3:
        print("Usage: railroad.py <start> <end>")
        print("Missing required city")
        return
    load_table()
    ROOT, canvas = load_map()
    ROOT.protocol("WM_DELETE_WINDOW", lambda: ROOT.destroy())

    start, end = strip_cities(argv[1:])
    path = a_star(ROOT, canvas, start, end)
    for i in range(1, len(path[0])):
        if path[0][i][0] in codes:
            print("Station {0}: {1} %.2lf miles".format(
                i, codes[path[0][i][0]]) % path[0][i][1])
        else:
            print("Station {0}: {1} %.2lf miles".format(
                i, path[0][i][0]) % path[0][i][1])
    print("The distance from {0} to {1} is %.2lf miles".format(
        codes[start], codes[end]) % path[1])

    try:
        while True:
            sleep(1)  # allow Tkinter canvas to persist after A* termination
    except KeyboardInterrupt:  # exit quietly
        exit(0)


if __name__ == '__main__':
    main()
