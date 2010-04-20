from shapely.geometry import *
from shapely.ops import *
from math import *

class Circle(object):
    def __init__(self, a, b, weight):
        super(Circle, self).__init__()
        self.a = a
        self.b = b
        self.weight = weight

    def getPolygon(self):
        (x1, y1), (x2, y2) = self.a, self.b
        width = sqrt((x2-x1)**2 + (y2-y1)**2)
        circ = Point(x1, y1).buffer(width)
        innerCirc = Point(x1, y1).buffer(width - (self.weight * 2))
        circ = circ.difference(innerCirc)
        return [circ]