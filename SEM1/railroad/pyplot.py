from matplotlib import collections as mc
import matplotlib.pyplot as plt

graph = {}  # station code -> [ (lat,long), [neighbors] ]


def load_table():
    global graph
    for x in open('rrNodes.txt').read().splitlines():
        parts = x.split(" ")
        graph[parts[0]] = [(float(parts[2]), float(parts[1])), []]
    for x in open("rrEdges.txt").read().splitlines():
        parts = x.split(" ")
        graph[parts[0]][1].append(parts[1])
        graph[parts[1]][1].append(parts[0])


load_table()

edges = []
for i in graph:
    for n in graph[i][1]:
        edges.append([ graph[i][0], graph[n][0] ])

lc = mc.LineCollection(edges, linewidths=2)
fig, ax = plt.subplots()

ax.add_collection(lc)
ax.autoscale()
ax.margins(0.1)

plt.show()