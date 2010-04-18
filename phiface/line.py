from shapely.geometry import *
from shapely.ops import *
from math import *

class Line(object):
    def __init__(self, a, b, width):
        super(Line, self).__init__()
        self.a = a
        self.b = b
        self.adelta = self.bdelta = width

    def atY(self, val):
        ((x1, y1), (x2, y2)) = (self.a, self.b)

        #if y2 > y1:
        #    y1, y2 = y2, y1
        #    x1, x2 = x2, x1

        print x1, y1, x2, y2

        return x1 + (((x2 - x1) / (y2 - y1)) * (val - y1))

    def getPolygon(self):
        ((x1, y1), (x2, y2)) = (self.a, self.b)

        angle = atan2(abs(y2 - y1), abs(x2 - x1))
        axOff = ayOff = bxOff = byOff = 0.0

        if angle > pi / 4.0:
            axOff = self.adelta
            bxOff = self.bdelta
        else:
            ayOff = self.adelta
            byOff = self.bdelta

        return Polygon(((x1 - axOff, y1 - ayOff), (x2 - bxOff, y2 - byOff),
                        (x2 + bxOff, y2 + byOff), (x1 + axOff, y1 + ayOff)))