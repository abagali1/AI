from sys import argv
from math import sin, cos, acos, pi
from heapq import heappush, heappop
from matplotlib import collections as mc
import matplotlib.pyplot as plt
from tkinter import *


names = {}  # name -> station code
graph = {}  # station code -> [ (lat,long), [neighbors] ]
edges = []  # list of lists of tuples (specific to pyplot)
DEFAULT_COLOR = 'red'
PATH_COLOR = 'blue'
FINAL_COLOR = 'green'


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
        graph[parts[0]] = [(float(parts[2]), float(parts[1])), []]
    for x in open("rrEdges.txt").read().splitlines():
        parts = x.split(" ")
        graph[parts[0]][1].append(parts[1])
        graph[parts[1]][1].append(parts[0])
    for i in graph:
        for n in graph[i][1]:
            edges.append([graph[i][0], graph[n][0]])


def load_map():
    pass
    # m = mc.LineCollection(edges, linewidths=1, color=DEFAULT_COLOR)
    # figure, plot = plt.subplots()
    #
    # plot.add_collection(m)
    # plot.autoscale()
    # plot.margins(0.1)
    #
    # plt.show()


def draw_edges(r, c):
    r.geometry("1200x800")
    c.pack(fill=BOTH, expand=1)
    for i in edges:
        line(c,i[0][0],i[0][1],i[1][0],i[1][1], 'white')
    r.update()


def line(c, x1,y1,x2,y2, color):
    x1, y1, x2, y2 = float(x1), float(y1), float(x2), float(y2)
    c.create_line((x1)*10+1500, (50-y1)*10+400, (x2)*10+1500, (50-y2)*10+400, fil=color)


def a_star(root, dest):
    ROOT = Tk()
    ROOT.title("railroad")
    canvas = Canvas(ROOT,background='black')
    draw_edges(ROOT,canvas)
    if root == dest:
        return root

    open_set, closed_set = [], {}
    h = gcd(graph[root][0][1], graph[root][0][0], graph[dest][0][1], graph[dest][0][0])
    open_set.append((0, h, root, ''))
    while open_set:
        g, h, elem, parent = heappop(open_set)
        if elem in closed_set:
            continue
        closed_set[elem] = parent
        if parent != '':
            line(canvas, graph[elem][0][0], graph[elem][0][1], graph[parent][0][0], graph[parent][0][1],'red')
        for nbr in graph[elem][1]:
            if nbr == dest:
                closed_set[nbr] = parent
                final_h = gcd(graph[nbr][0][1], graph[nbr][0][0], graph[parent][0][1],graph[parent][0][0]) + g
                return backtrack(closed_set, dest), final_h
            else:
                h = gcd(graph[elem][0][1], graph[elem][0][0], graph[nbr][0][1], graph[nbr][0][0])
                heappush(open_set,(g+h, h, nbr, elem))
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
    load_table()
    load_map()
    start, end = strip_cities(argv[1:])
    path = a_star(end,start)
    print(path)


if __name__ == '__main__':
    main()
