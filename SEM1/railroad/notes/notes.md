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