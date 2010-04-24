from shapely.geometry import *
from shapely.ops import *
from math import *
from line import Line

capHeight = 100

class Circle(object):
    def __init__(self, a, b, weight, semiA=None, semiB=None, serif=0,
                 swapClip=False):
        super(Circle, self).__init__()
        self.a = a
        self.b = b
        self.weight = weight
        self.semiA = semiA
        self.semiB = semiB
        self.serif = serif
        self.swapClip = swapClip

    def getPolygon(self):
        (x1, y1), (x2, y2) = self.a, self.b
        ax = ay = bx = by = 0
        width = sqrt((x2-x1)**2 + (y2-y1)**2)
        circ = Point(x1, y1).buffer(width, quadsegs=64)

        if self.weight > 0:
            innerCirc = Point(x1, y1).buffer(width - (self.weight * 2),
                                             quadsegs=64)
            circ = circ.difference(innerCirc)

        if self.semiA and self.semiB:
            (ax, ay), (bx, by) = self.semiA, self.semiB

            clipPoly = Polygon(((x1, y1),
                                (ax, ay),
                                (bx, by)))

            if self.swapClip:
                circ = circ.intersection(clipPoly)
            else:
                circ = circ.difference(clipPoly)

        # Done, if we don't want serifs
        if self.serif == 0 or not (self.semiA and self.semiB):
            return [circ]

        serifPolys = []
        serifWeight = self.weight * 0.618 + max((capHeight / 90.0) - 1.0, 0.0)
        ss = capHeight / 15.0 + (self.weight * capHeight / 200.0)

        topAngle = atan2(by - y1, bx - x1)
        bottomAngle = atan2(ay - y1, ax - x1)

        if self.serif == 1 or self.serif == 2:
            serifPolys = [Line((x1 + (width-self.weight)*cos(topAngle),
                                y1 - (width-self.weight)*sin(topAngle) + ss +
                                    self.weight / 2.0),
                               (x1 + (width-self.weight)*cos(topAngle),
                                y1 - (width-self.weight)*sin(topAngle) - ss +
                                    self.weight / 2.0),
                               serifWeight)]
        if self.serif == 2:
            serifPolys += [Line((x1 + (width-self.weight)*cos(bottomAngle),
                                 y1 - (width-self.weight)*sin(bottomAngle) +
                                     ss - self.weight / 2.0),
                                (x1 + (width-self.weight)*cos(bottomAngle),
                                 y1 - (width-self.weight)*sin(bottomAngle) -
                                     ss - self.weight / 2.0),
                                serifWeight)]

        return [circ, serifPolys]
