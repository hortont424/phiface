from shapely.geometry import *
from shapely.ops import *

def test():
    a = Polygon(((-1.0, -1.0), (-1.0, 1.0), (1.0, 1.0), (1.0, -1.0)))
    b = Polygon(((-2.0, -2.0), (-2.0, 0.5), (0.5, 0.5), (0.5, -2.0)))
    c = a.union(b)

    for (x, y) in c.exterior.coords:
        print x, y

    return c