from shapely.geometry import *
from shapely.ops import *
from math import *

drawSerifs = True
capHeight = 100 # TODO: completely retarded

class Line(object):
    def __init__(self, a, b, width, shift=None, serif=0):
        super(Line, self).__init__()
        self.a = a
        self.b = b
        self.delta = width
        self.shift = shift
        self.serif = serif

    def atY(self, val):
        ((x1, y1), (x2, y2)) = (self.a, self.b)
        return x1 + (((x2 - x1) / (y2 - y1)) * (val - y1))

    def getPolygon(self):
        ((x1, y1), (x2, y2)) = (self.a, self.b)

        angle = atan2(abs(y2 - y1), abs(x2 - x1)) #WRONGO
        xOff = yOff = 0.0

        endDirection = angle > pi / 4.0

        if endDirection:
            if self.shift is "left":
                x1 -= self.delta
                x2 -= self.delta
            elif self.shift is "right":
                x1 += self.delta
                x2 += self.delta
        else:
            if self.shift is "up":
                y1 -= self.delta
                y2 -= self.delta
            elif self.shift is "down":
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
        ss = capHeight / 20.0

        if self.serif == 1 or self.serif == 2:
            if self.shift is "down":
                serifPolys = [Line((x2 - serifWeight, y2 - self.delta),
                                   (x2 - serifWeight, y2 + self.delta + ss),
                                   serifWeight)]
            elif self.shift is "up":
                serifPolys = [Line((x2 - serifWeight, y2 + self.delta),
                                   (x2 - serifWeight, y2 - self.delta - ss),
                                   serifWeight)]
            else:
                serifPolys = [Line((x2 - serifWeight, y2 + self.delta + ss),
                                   (x2 - serifWeight, y2 - self.delta - ss),
                                   serifWeight)]
        if self.serif == 2:
            if self.shift is "down":
                serifPolys += [Line((x1 + serifWeight, y1 - self.delta),
                                    (x1 + serifWeight, y1 + self.delta + ss),
                                    serifWeight)]
            elif self.shift is "up":
                serifPolys += [Line((x1 + serifWeight, y1 + self.delta),
                                    (x1 + serifWeight, y1 - self.delta - ss),
                                    serifWeight)]
            else:
                serifPolys += [Line((x1 + serifWeight, y1 + self.delta + ss),
                                    (x1 + serifWeight, y1 - self.delta - ss),
                                    serifWeight)]
        if self.serif == 3 or self.serif == 4:
            if self.shift is "down":
                serifPolys = [Line((x2 + serifWeight + ss,
                                    y2 + serifWeight),
                                   (x2 - serifWeight - ss,
                                    y2 + serifWeight),
                                   serifWeight)]
            elif self.shift is "up":
                serifPolys = [Line((x2 + serifWeight + ss,
                                    y2 - serifWeight),
                                   (x2 - serifWeight - ss,
                                    y2 - serifWeight),
                                   serifWeight)]
            else:
                serifPolys = [Line((x2 + serifWeight + ss,
                                    y2 - serifWeight),
                                   (x2 - serifWeight - ss,
                                    y2 - serifWeight),
                                   serifWeight)]
        if self.serif == 4:
            if self.shift is "down":
                serifPolys += [Line((x1 + serifWeight + ss,
                                     y1 - serifWeight),
                                    (x1 - serifWeight - ss,
                                     y1 - serifWeight),
                                    serifWeight)]
            elif self.shift is "up":
                serifPolys += [Line((x1 + serifWeight + ss,
                                     y1 + serifWeight),
                                    (x1 - serifWeight - ss,
                                     y1 + serifWeight),
                                    serifWeight)]
            else:
                serifPolys += [Line((x1 + serifWeight + ss,
                                     y1 + serifWeight),
                                    (x1 - serifWeight - ss,
                                     y1 + serifWeight),
                                    serifWeight)]
        return [linePoly, serifPolys]