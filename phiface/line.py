from shapely.geometry import *
from shapely.ops import *

class Line(object):
    def __init__(self, a, b, width):
        super(Line, self).__init__()
        self.a = a
        self.b = b
        self.adelta = self.bdelta = width

    def getPolygon(self):
        ((x1, y1), (x2, y2)) = (self.a, self.b)
        # double check ordering of 1 vs. 2
        return Polygon(((x1 - self.adelta, y1), (x2 - self.bdelta, y2),
                        (x2 + self.bdelta, y2), (x1 + self.adelta, y1)))