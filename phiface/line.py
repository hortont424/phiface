from shapely.geometry import *
from shapely.ops import *
from math import *

drawSerifs = True
capHeight = 100 # TODO: completely retarded

class Line(object):
    def __init__(self, a, b, width, shift=None, serif=0, snapEnd=False):
        super(Line, self).__init__()
        self.a = a
        self.b = b
        self.delta = width
        self.shift = shift
        self.serif = serif
        self.snapEnd = snapEnd

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

        if self.snapEnd:
            if endDirection:
                ry4 = ry3 = y2
                ry2 = ry1 = y1
            else:
                rx4 = rx3 = x2
                rx2 = rx1 = x1

        linePoly = Polygon(((rx1, ry1), (rx2, ry2),
                            (rx4, ry4), (rx3, ry3)))

        # Done, unless we want serifs
        if not drawSerifs:
            return linePoly

        serifPolys = []
        serifWeight = self.delta * 0.618
        ss = capHeight / 20.0
        angleShift = 0.0 #cos(angle) * (self.delta * 0.7)
        if x2 > x1:
            angleShift *= -1

        #x1 = rx1
        #x2 = rx4
        #y1 = ry1
        #y2 = ry4

        if self.serif == 1 or self.serif == 2:
            if self.shift is "down":
                serifPolys = [Line((x2, y2 - self.delta),
                                   (x2, y2 + self.delta + ss),
                                   serifWeight)]
            elif self.shift is "up":
                serifPolys = [Line((x2, y2 + self.delta),
                                   (x2, y2 - self.delta - ss),
                                   serifWeight)]
            else:
                serifPolys = [Line((x2, y2 + self.delta + ss),
                                   (x2, y2 - self.delta - ss),
                                   serifWeight)]
        if self.serif == 2:
            if self.shift is "down":
                serifPolys += [Line((x1, y1 - self.delta),
                                    (x1, y1 + self.delta + ss),
                                    serifWeight)]
            elif self.shift is "up":
                serifPolys += [Line((x1, y1 + self.delta),
                                    (x1, y1 - self.delta - ss),
                                    serifWeight)]
            else:
                serifPolys += [Line((x1, y1 + self.delta + ss),
                                    (x1, y1 - self.delta - ss),
                                    serifWeight)]
        if self.serif == 3 or self.serif == 4:
            if self.shift is "down":
                serifPolys = [Line((x2 + serifWeight + ss + angleShift,
                                    y2),
                                   (x2 - serifWeight - ss + angleShift,
                                    y2),
                                   serifWeight)]
            elif self.shift is "up":
                serifPolys = [Line((x2 + serifWeight + ss + angleShift,
                                    y2),
                                   (x2 - serifWeight - ss + angleShift,
                                    y2),
                                   serifWeight)]
            else:
                serifPolys = [Line((x2 + serifWeight + ss + angleShift,
                                    y2),
                                   (x2 - serifWeight - ss + angleShift,
                                    y2),
                                   serifWeight)]
        if self.serif == 4:
            if self.shift is "down":
                serifPolys += [Line((x1 + serifWeight + ss - angleShift,
                                     y1),
                                    (x1 - serifWeight - ss - angleShift,
                                     y1),
                                    serifWeight)]
            elif self.shift is "up":
                serifPolys += [Line((x1 + serifWeight + ss - angleShift,
                                     y1),
                                    (x1 - serifWeight - ss - angleShift,
                                     y1),
                                    serifWeight)]
            else:
                serifPolys += [Line((x1 + serifWeight + ss - angleShift,
                                     y1),
                                    (x1 - serifWeight - ss - angleShift,
                                     y1),
                                    serifWeight)]
        return [linePoly, serifPolys]