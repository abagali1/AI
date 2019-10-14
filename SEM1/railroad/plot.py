from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

map = Basemap(llcrnrlat=12.737800, llcrnrlon=-132.398842, urcrnrlat=52.039690, urcrnrlon=-56.444490,
              area_thresh=1000, projection='merc', resolution='l', lat_0=40, lon_0=-87.)
map.drawcoastlines(color='white')
map.drawcountries(color='white')
map.fillcontinents(color='black')
map.drawmapboundary()

coors = open('rrNodes.txt').read().splitlines()
lat = [float(x.split(" ")[1]) for x in coors]
lon = [float(x.split(" ")[2]) for x in coors]
x,y = map(lon, lat)
map.plot(x, y, 'ro', markersize=0.1)
plt.show()