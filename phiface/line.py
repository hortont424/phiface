from shapely.geometry import *
from shapely.ops import *
from math import *

class Line(object):
    def __init__(self, a, b, width, shift=None):
        super(Line, self).__init__()
        self.a = a
        self.b = b
        self.adelta = self.bdelta = width
        self.shift = shift

    def atY(self, val):
        ((x1, y1), (x2, y2)) = (self.a, self.b)
        return x1 + (((x2 - x1) / (y2 - y1)) * (val - y1))

    def getPolygon(self):
        ((x1, y1), (x2, y2)) = (self.a, self.b)

        angle = atan2(abs(y2 - y1), abs(x2 - x1))
        axOff = ayOff = bxOff = byOff = 0.0

        if angle > pi / 4.0:
            axOff = self.adelta
            bxOff = self.bdelta
            if self.shift is "left":
                x1 -= axOff
                x2 -= bxOff
            elif self.shift is "right":
                x1 += axOff
                x2 += bxOff
        else:
            ayOff = self.adelta
            byOff = self.bdelta
            if self.shift is "up":
                y1 -= ayOff
                y2 -= byOff
            elif self.shift is "down":
                y1 += ayOff
                y2 += byOff

        return Polygon(((x1 - axOff, y1 - ayOff), (x2 - bxOff, y2 - byOff),
                        (x2 + bxOff, y2 + byOff), (x1 + axOff, y1 + ayOff)))