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
        return ((y2 - y1) / (x2 - x1)) * val # this is currently wrong

    def getPolygon(self):
        ((x1, y1), (x2, y2)) = (self.a, self.b)

        angle = atan2(abs(y2 - y1), abs(x2 - x1))
        axShift = ayShift = bxShift = byShift = 0.0

        if angle > pi / 4.0:
            axShift = self.adelta
            bxShift = self.bdelta
        else:
            ayShift = self.adelta
            byShift = self.bdelta

        return Polygon(((x1 - axShift, y1 - ayShift), (x2 - bxShift, y2 - byShift),
                        (x2 + bxShift, y2 + byShift), (x1 + axShift, y1 + ayShift)))