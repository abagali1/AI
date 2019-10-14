from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.animation as animation

graph = {}  # station code -> [ (lat,long), [neighbors] ]


def load_table():
    global graph
    for x in open('rrNodes.txt').read().splitlines():
        parts = x.split(" ")
        graph[parts[0]] = [(float(parts[1]), float(parts[2])), []]
    for x in open("rrEdges.txt").read().splitlines():
        parts = x.split(" ")
        graph[parts[0]][1].append(parts[1])
        graph[parts[1]][1].append(parts[0])

load_table()
map = Basemap(llcrnrlat=12.737800, llcrnrlon=-132.398842, urcrnrlat=52.039690, urcrnrlon=-56.444490,
              area_thresh=1000, projection='merc', resolution='l', lat_0=40, lon_0=-87.)
map.drawcountries(color='white')
map.fillcontinents(color='black')
map.drawmapboundary()


lines = {}
for i in graph:
    for n in graph[i][1]:
        if (n,i) not in lines:
            lines[(i,n)] = map.drawgreatcircle(graph[i][0][1],graph[i][0][0],graph[n][0][1],graph[n][0][0],color='r',markersize=0.01)[0]
            lines[(n,i)] = lines[(i,n)]




plt.savefig('map.png', dpi=1440)