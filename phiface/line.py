# -*- coding: utf-8 -*-

from shapely.geometry import *
from shapely.ops import *
from math import *
from context import mergeSubPolys

drawSerifs = True
capHeight = 100 # TODO: completely retarded

class Line(object):
    def __init__(self, a, b, width, shift=None, serif=0, noclip=False,
                 swapAngle=False):
        super(Line, self).__init__()
        self.a = a
        self.b = b
        self.delta = width
        self.shift = shift
        self.serif = serif
        self.noclip = noclip
        self.swapAngle = swapAngle

    def atY(self, val):
        ((x1, y1), (x2, y2)) = (self.a, self.b)
        return x1 + (((x2 - x1) / (y2 - y1)) * (val - y1))

    def getPolygon(self):
        ((x1, y1), (x2, y2)) = (self.a, self.b)

        angle = atan2(abs(y2 - y1), abs(x2 - x1))
        realAngle = atan2(y2 - y1, x2 - x1)
        xOff = yOff = 0.0

        endDirection = angle > pi / 4.0

        if self.swapAngle:
            endDirection = not endDirection

        if endDirection:
            if self.shift and "left" in self.shift:
                x1 -= self.delta
                x2 -= self.delta
            elif self.shift and "right" in self.shift:
                x1 += self.delta
                x2 += self.delta
        else:
            if self.shift and "up" in self.shift:
                y1 -= self.delta
                y2 -= self.delta
            elif self.shift and "down" in self.shift:
                y1 += self.delta
                y2 += self.delta

        dx = x1-x2
        dy = y1-y2
        dist = sqrt(dx*dx + dy*dy)
        dx /= dist
        dy /= dist
        rx1 = x1 + (self.delta)*dy
        ry1 = y1 - (self.delta)*dx
        rx2 = x1 - (self.delta)*dy
        ry2 = y1 + (self.delta)*dx

        rx3 = x2 + (self.delta)*dy
        ry3 = y2 - (self.delta)*dx
        rx4 = x2 - (self.delta)*dy
        ry4 = y2 + (self.delta)*dx

        linePoly = Polygon(((rx1, ry1), (rx2, ry2),
                            (rx4, ry4), (rx3, ry3)))

        xInf = yInf = 0
        if endDirection:
            xInf = 200
        else:
            yInf = 200

        if (not self.noclip) or (self.noclip == 2):
            clipPoly = None

            if self.noclip == 2:
                clipPoly = Polygon(((x1 - xInf, y1 - yInf),
                                    (x1 - xInf, y2 + 200),
                                    (x2 + 200, y2 + 200),
                                    (x2 + 200, y1 - yInf)))
            else:
                clipPoly = Polygon(((x1 - xInf, y1 - yInf),
                                    (x1 - xInf, y2 + yInf),
                                    (x2 + xInf, y2 + yInf),
                                    (x2 + xInf, y1 - yInf)))

            clipPoly = linePoly.intersection(clipPoly)

            if type(clipPoly) is not GeometryCollection:
                linePoly = clipPoly

        # Done, unless we want serifs
        if not drawSerifs:
            return linePoly

        serifPolys = []
        serifWeight = self.delta * 0.618
        ss = capHeight / 15.0
        angleShift = cos(realAngle) * (self.delta * -1.2)

        if self.serif == 1 or self.serif == 2:
            if self.shift and "down" in self.shift:
                serifPolys = [Line((x2 - serifWeight, y2 - self.delta),
                                   (x2 - serifWeight, y2 + self.delta + ss),
                                   serifWeight)]
            elif self.shift and "up" in self.shift:
                serifPolys = [Line((x2 - serifWeight, y2 + self.delta),
                                   (x2 - serifWeight, y2 - self.delta - ss),
                                   serifWeight)]
            else:
                serifPolys = [Line((x2 - serifWeight, y2 + self.delta + ss),
                                   (x2 - serifWeight, y2 - self.delta - ss),
                                   serifWeight)]
        if self.serif == 2:
            if self.shift and "down" in self.shift:
                serifPolys += [Line((x1 + serifWeight, y1 - self.delta),
                                    (x1 + serifWeight, y1 + self.delta + ss),
                                    serifWeight)]
            elif self.shift and "up" in self.shift:
                serifPolys += [Line((x1 + serifWeight, y1 + self.delta),
                                    (x1 + serifWeight, y1 - self.delta - ss),
                                    serifWeight)]
            else:
                serifPolys += [Line((x1 + serifWeight, y1 + self.delta + ss),
                                    (x1 + serifWeight, y1 - self.delta - ss),
                                    serifWeight)]
        if self.serif == 3 or self.serif == 4 or self.serif == 5:
            if self.shift and "down" in self.shift:
                serifPolys = [Line((x2 + serifWeight + ss + angleShift,
                                    y2 + serifWeight),
                                   (x2 - serifWeight - ss + angleShift,
                                    y2 + serifWeight),
                                   serifWeight)]
            elif self.shift and "up" in self.shift:
                serifPolys = [Line((x2 + serifWeight + ss + angleShift,
                                    y2 - serifWeight),
                                   (x2 - serifWeight - ss + angleShift,
                                    y2 - serifWeight),
                                   serifWeight)]
            else:
                serifPolys = [Line((x2 + serifWeight + ss + angleShift,
                                    y2 - serifWeight),
                                   (x2 - serifWeight - ss + angleShift,
                                    y2 - serifWeight),
                                   serifWeight)]
        if self.serif == 4:
            if self.shift and "down" in self.shift:
                serifPolys += [Line((x1 + serifWeight + ss - angleShift,
                                     y1 - serifWeight),
                                    (x1 - serifWeight - ss - angleShift,
                                     y1 - serifWeight),
                                    serifWeight)]
            elif self.shift and "up" in self.shift:
                serifPolys += [Line((x1 + serifWeight + ss - angleShift,
                                     y1 + serifWeight),
                                    (x1 - serifWeight - ss - angleShift,
                                     y1 + serifWeight),
                                    serifWeight)]
            else:
                serifPolys += [Line((x1 + serifWeight + ss - angleShift,
                                     y1 + serifWeight),
                                    (x1 - serifWeight - ss - angleShift,
                                     y1 + serifWeight),
                                    serifWeight)]
        if self.serif == 5 or self.serif == 6:
            if self.shift and "down" in self.shift:
                serifPolys += [Line((x1,
                                     y1 - serifWeight),
                                    (x1 - serifWeight - ss - angleShift,
                                     y1 - serifWeight),
                                    serifWeight)]
            elif self.shift and "up" in self.shift:
                serifPolys += [Line((x1,
                                     y1 + serifWeight),
                                    (x1 - serifWeight - ss - angleShift,
                                     y1 + serifWeight),
                                    serifWeight)]
            else:
                serifPolys += [Line((x1,
                                     y1 + serifWeight),
                                    (x1 - serifWeight - ss - angleShift,
                                     y1 + serifWeight),
                                    serifWeight)]
        return mergeSubPolys([linePoly, serifPolys])
