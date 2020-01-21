# Railroad

### Files

`rrNodes.txt` -> identifier, longitude, latitude (identifier is a unique code for a station)

`rrEdges.txt` -> identifier: identifier (lists all edges)

`rrNodeCity.txt` -> identifier: name (maps code to city name)

the distance between two stations is **NOT** 1!

### Calculating Station Distance
[Great Circle Distance](https://en.wikipedia.org/wiki/Great-circle_distance)
[script](https://compsci.sites.tjhsst.edu/ai/distanceDemo.py.txt)


### Inputs
arg[0] -> `script.py`

arg[1] -> from city

arg[2:] -> end city

### Output
- Use Tkinter to display `A*` working
    * list of cities with distances -> list
    * final distance traverse -> int
    
#### Dummy Check
* output of going from Point A to Point B is the same as going from Point B to Point A

#### Planning

1. Read sys args
2. load data from files
```json
"identifier":{
  (name, (lat,long), [neighbors] )
}
```
3. Run A* alongside with Tkinter
* g=level
* h=Great Circle Distance from current node to goal

#### Using Basemap
1. Use `pip` to install dependencies from `requirements.txt`
2. Install the [PROJ4](https://proj.org/install.html) library
  * Available through `pacman` (`pacman -S proj`)
3. Install the [GEOS](https://trac.osgeo.org/geos/) library
  * Available through `pacman` (`pacman -S geos`)
4. Run `pip3 install git+https://github.com/matplotlib/basemap.git`
5. Run `plot.py` in the same directory as `rrNodes.txt'

**Using `venv` is recommended**
