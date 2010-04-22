import line
import circle
from line import Line
from circle import Circle
from context import mergeSubPolys
from shapely.geometry import *

PHI = 1.618

glyphs = {}

def glyph(g):
    def wrap(cls):
        glyphs[g] = cls
        return cls
    return wrap

class Glyph(object):
    def __init__(self, x, y, capHeight=50):
        super(Glyph, self).__init__()
        self.x = x
        self.y = y
        self.w = 3
        self.pointSize = capHeight
        circle.capHeight = line.capHeight = self.capHeight()

    def capHeight(self):
        return self.pointSize

    def em(self):
        return self.baseWidth() * PHI * 0.618

    def baseWidth(self):
        return self.capHeight() / PHI

    def width(self):
        pass

    def weight(self):
        return self.w

    def xHeight(self):
        return self.capHeight() / PHI

    def origin(self):
        return (self.x, self.y + self.capHeight())

    def p(self, ix, iy, xHeight=False):
        (x, y) = self.origin()
        height = self.capHeight()

        if xHeight:
            height = self.xHeight()
        return (x + (self.width() * ix), y - (height * iy))

@glyph('A')
class AGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(AGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.baseWidth()

    def getPolygon(self):
        leftLine = Line(self.p(0.5, 1.0), self.p(0.0, 0.0),
                        self.weight(), serif=3)
        rightLine = Line(self.p(0.5, 1.0), self.p(1.0, 0.0),
                         self.weight(), serif=3)

        midHeight = self.p(0.0, 0.5, xHeight=True)[1]
        midLeft = leftLine.atY(midHeight)
        midRight = rightLine.atY(midHeight)

        midLine = Line((midLeft, midHeight),
                       (midRight, midHeight), self.weight())

        return [leftLine, rightLine, midLine]

@glyph('B')
class BGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(BGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.baseWidth()

    def getPolygon(self):
        shift = ((self.weight() / 2.0) / self.capHeight()) * 4
        bottomHeight = 0.5
        bottomY = bottomHeight / 2.0
        bottomYY = bottomY + (bottomHeight / 2.0)
        topHeight = 1.0 - bottomHeight
        topY = bottomYY + (topHeight / 2.0)
        topYY = bottomYY

        bottomYY += shift / 2.0
        bottomY += shift / 4.0

        topYY -= shift / 2.0
        topY -= shift / 4.0

        circa = Circle(self.p(0.5, bottomY),
                       self.p(0.5, bottomYY),
                       self.weight())
        circb = Circle(self.p(0.5, topY),
                       self.p(0.5, topYY),
                       self.weight())

        clipPoly = Polygon((self.p(0.5, 0.0), self.p(0.5, 1.0),
                            self.p(1.5, 1.0), self.p(1.5, 0.0)))

        threePoly = mergeSubPolys([circa, circb]).intersection(
            mergeSubPolys([clipPoly]))

        topLine = Line(self.p(0.0, 1.0), self.p(0.5, 1.0),
                       self.weight(), shift="down")
        bottomLine = Line(self.p(0.0, 0.0), self.p(0.5, 0.0),
                          self.weight(), shift="up")
        midLine = Line(self.p(0.0, 0.5), self.p(0.5, 0.5),
                       self.weight())

        leftLine = Line(self.p(0.0, 1.0), self.p(0.0, 0.0),
                        self.weight(), shift="right", serif=4)

        return [threePoly, topLine, bottomLine, leftLine, midLine]

@glyph('C')
class CGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(CGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.capHeight()

    def getPolygon(self):
        circ = Circle(self.p(0.5, 0.5),
                      self.p(0.5, 1.0),
                      self.weight(),
                      semiA=self.p(1.0, 0.8),
                      semiB=self.p(1.0, 0.2))
        return [circ]

@glyph('D')
class DGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(DGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.capHeight()

    def getPolygon(self):
        circ = Circle(self.p(0.5, 0.5),
                      self.p(0.5, 1.0),
                      self.weight(),
                      semiA=self.p(0.0, 0.8),
                      semiB=self.p(0.0, 0.2))

        clipPoly = Polygon((self.p(0.5, 0.0), self.p(0.5, 1.0),
                            self.p(1.5, 1.0), self.p(1.5, 0.0)))

        circ = mergeSubPolys([circ]).intersection(
            mergeSubPolys([clipPoly]))

        dWidth = 0.2
        leftLine = Line(self.p(dWidth, 1.0), self.p(dWidth, 0.0),
                        self.weight(), shift="right", serif=4)
        topLine = Line(self.p(dWidth, 1.0), self.p(0.5, 1.0),
                       self.weight(), shift="down")
        bottomLine = Line(self.p(dWidth, 0.0), self.p(0.5, 0.0),
                          self.weight(), shift="up")

        return [circ, leftLine, topLine, bottomLine]

@glyph('E')
class EGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(EGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.baseWidth()

    def getPolygon(self):
        leftLine = Line(self.p(0.0, 0.0), self.p(0.0, 1.0),
                        self.weight(), shift="right")
        topLine = Line(self.p(0.0, 1.0), self.p(1.0, 1.0),
                       self.weight(), shift="down", serif=1)
        bottomLine = Line(self.p(0.0, 0.0), self.p(1.0, 0.0),
                          self.weight(), shift="up", serif=1)

        midHeight = self.p(0.0, 0.5, xHeight=True)[1]
        midLeft = leftLine.atY(midHeight)

        midLine = Line((midLeft, midHeight),
                       (midLeft + self.width() / PHI, midHeight),
                       self.weight())

        return [leftLine, topLine, midLine, bottomLine]

@glyph('F')
class FGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(FGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.baseWidth()

    def getPolygon(self):
        leftLine = Line(self.p(0.0, 1.0), self.p(0.0, 0.0),
                        self.weight(), shift="right", serif=3)
        topLine = Line(self.p(0.0, 1.0), self.p(1.0, 1.0),
                       self.weight(), shift="down", serif=1)

        midHeight = self.p(0.0, 0.5, xHeight=True)[1]
        midLeft = leftLine.atY(midHeight)

        midLine = Line((midLeft, midHeight),
                       (midLeft + self.width() / PHI, midHeight),
                       self.weight())

        return [leftLine, topLine, midLine]

@glyph('G')
class GGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(GGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.capHeight()

    def getPolygon(self):
        leftShift = self.weight() / self.capHeight() / 2

        circ = Circle(self.p(0.5, 0.5),
                      self.p(0.5, 1.0),
                      self.weight(),
                      semiA=self.p(1.0, 0.8),
                      semiB=self.p(1.0, 0.5))

        midLine = Line(self.p(1.0 - leftShift, 0.5), self.p(0.5, 0.5),
                       self.weight(), shift="down")

        return [circ, midLine]

@glyph('H')
class HGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(HGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.baseWidth()

    def getPolygon(self):
        leftLine = Line(self.p(0.0, 1.0), self.p(0.0, 0.0),
                        self.weight(), serif=4)
        rightLine = Line(self.p(1.0, 1.0), self.p(1.0, 0.0),
                         self.weight(), serif=4)

        midHeight = self.p(0.0, 0.5, xHeight=True)[1]
        midLeft = leftLine.atY(midHeight)
        midRight = rightLine.atY(midHeight)

        midLine = Line((midLeft, midHeight),
                       (midRight, midHeight), self.weight())

        return [leftLine, rightLine, midLine]

@glyph('I')
class IGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(IGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.baseWidth() / PHI

    def getPolygon(self):
        mainLine = Line(self.p(0.5, 0.0), self.p(0.5, 1.0),
                        self.weight())
        topLine = Line(self.p(0.0, 1.0), self.p(1.0, 1.0),
                       self.weight() / PHI, shift="down")
        bottomLine = Line(self.p(0.0, 0.0), self.p(1.0, 0.0),
                          self.weight() / PHI, shift="up")
        return [mainLine, topLine, bottomLine]

@glyph('J')
class JGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(JGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.baseWidth() / PHI

    def getPolygon(self):
        mainLine = Line(self.p(1.0, 1.0), self.p(1.0, 0.0),
                        self.weight(), shift="left", serif=6)
        circ = Circle(self.p(0.5, 0.0),
                      self.p(1.0, 0.0),
                      self.weight())
        clipPoly = Polygon((self.p(0.5, 0.0), self.p(1.0, 0.0),
                            self.p(1.0, -1.0), self.p(0.5, -1.0)))

        circ = mergeSubPolys([circ]).intersection(
            mergeSubPolys([clipPoly]))

        return [mainLine, circ]

@glyph('K')
class KGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(KGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.baseWidth() * 0.8

    def getPolygon(self):
        mainLine = Line(self.p(0.0, 0.0), self.p(0.0, 1.0),
                        self.weight(), shift="down", serif=4)
        topLine = Line(self.p(0.0, 0.5), self.p(1.0, 1.0),
                       self.weight(), shift="down", serif=3)
        bottomLine = Line(self.p(0.0, 0.5), self.p(1.0, 0.0),
                          self.weight(), shift="up", serif=3)
        return [topLine, bottomLine, mainLine]

@glyph('L')
class LGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(LGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.baseWidth() / PHI

    def getPolygon(self):
        mainLine = Line(self.p(0.0, 0.0), self.p(0.0, 1.0),
                        self.weight(), shift="down", serif=3)
        bottomLine = Line(self.p(0.0, 0.0), self.p(1.0, 0.0),
                          self.weight(), shift="up", serif=1)
        return [mainLine, bottomLine]

@glyph('M')
class MGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(MGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em()

    def getPolygon(self):
        midHeight = (self.weight()) / self.xHeight()

        leftLine = Line(self.p(0.0, 1.0), self.p(0.0, 0.0),
                        self.weight(), shift="up", serif=3)
        downCrossLine = Line(self.p(0.0, 1.0),
                             self.p(0.5, 0.5 - midHeight, xHeight=True),
                             self.weight())
        upCrossLine = Line(self.p(0.5, 0.5 - midHeight, xHeight=True),
                           self.p(1.0, 1.0),
                           self.weight())
        rightLine = Line(self.p(1.0, 1.0), self.p(1.0, 0.0),
                         self.weight(), shift="up", serif=3)
        return [leftLine, downCrossLine, upCrossLine, rightLine]

@glyph('N')
class NGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(NGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.baseWidth()

    def getPolygon(self):
        leftLine = Line(self.p(0.0, 1.0), self.p(0.0, 0.0),
                        self.weight(), shift="up", serif=3)
        crossLine = Line(self.p(0.0, 1.0), self.p(1.0, 0.0),
                         self.weight())
        rightLine = Line(self.p(1.0, 0.0), self.p(1.0, 1.0),
                         self.weight(), shift="down", serif=3)
        return [leftLine, crossLine, rightLine]

@glyph('O')
class OGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(OGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.capHeight()

    def getPolygon(self):
        circ = Circle(self.p(0.5, 0.5),
                      self.p(0.5, 1.0),
                      self.weight())
        return [circ]

@glyph('P')
class PGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(PGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.baseWidth()

    def getPolygon(self):
        shift = ((self.weight() / 2.0) / self.capHeight()) * 4
        bottomHeight = 0.5
        bottomY = bottomHeight / 2.0
        bottomYY = bottomY + (bottomHeight / 2.0)
        topHeight = 1.0 - bottomHeight
        topY = bottomYY + (topHeight / 2.0)
        topYY = bottomYY

        topYY -= shift / 2.0
        topY -= shift / 4.0

        circa = Circle(self.p(0.5, topY),
                       self.p(0.5, topYY),
                       self.weight())

        clipPoly = Polygon((self.p(0.5, 0.0), self.p(0.5, 1.0),
                            self.p(1.5, 1.0), self.p(1.5, 0.0)))

        threePoly = mergeSubPolys([circa]).intersection(
            mergeSubPolys([clipPoly]))

        topLine = Line(self.p(0.0, 1.0), self.p(0.5, 1.0),
                       self.weight(), shift="down")
        midLine = Line(self.p(0.0, 0.5), self.p(0.5, 0.5),
                       self.weight())

        leftLine = Line(self.p(0.0, 1.0), self.p(0.0, 0.0),
                        self.weight(), shift="right", serif=4)

        return [threePoly, topLine, leftLine, midLine]

@glyph('Q')
class QGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(QGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.capHeight()

    def getPolygon(self):
        shift = (self.weight() / 20.0) / (self.capHeight() / 40.0)
        circ = Circle(self.p(0.5, 0.5),
                      self.p(0.5, 1.0),
                      self.weight())
        crossLine = Line(self.p(0.75 - shift, 0.25 + shift),
                         self.p(1.0, 0.0), self.weight(), noclip=True)
        return [circ, crossLine]

@glyph('R')
class RGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(RGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.baseWidth()

    def getPolygon(self):
        shift = ((self.weight() / 2.0) / self.capHeight()) * 4
        bottomHeight = 0.5
        bottomY = bottomHeight / 2.0
        bottomYY = bottomY + (bottomHeight / 2.0)
        topHeight = 1.0 - bottomHeight
        topY = bottomYY + (topHeight / 2.0)
        topYY = bottomYY

        topYY -= shift / 2.0
        topY -= shift / 4.0

        dy = topY - topYY

        circa = Circle(self.p(0.5, topY),
                       self.p(0.5, topYY),
                       self.weight())

        clipPoly = Polygon((self.p(0.5, 0.0), self.p(0.5, 1.0),
                            self.p(1.5, 1.0), self.p(1.5, 0.0)))

        threePoly = mergeSubPolys([circa]).intersection(
            mergeSubPolys([clipPoly]))

        topLine = Line(self.p(0.0, 1.0), self.p(0.5, 1.0),
                       self.weight(), shift="down")
        midLine = Line(self.p(0.0, 0.5), self.p(0.5, 0.5),
                       self.weight())

        leftLine = Line(self.p(0.0, 1.0), self.p(0.0, 0.0),
                        self.weight(), shift="right", serif=4)

        downLine = Line(self.p(0.5, 0.5), self.p(1.0, 0.0),
                        self.weight(), shift="up", serif=3)

        return [threePoly, topLine, leftLine, midLine, downLine]


@glyph('T')
class TGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(TGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.baseWidth()

    def getPolygon(self):
        mainLine = Line(self.p(0.5, 0.0), self.p(0.5, 1.0), self.weight())
        topLine = Line(self.p(0.0, 1.0), self.p(1.0, 1.0),
                       self.weight(), shift="down", serif=2)
        return [mainLine, topLine]

@glyph('U')
class UGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(UGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.baseWidth()

    def getPolygon(self):
        rad = 0.309
        shift = self.p(0.5, rad)[0] - self.p(0.0, 0.0)[0]
        shift -= self.p(0.5, 0.0)[1] - self.p(0.5, rad)[1]
        shift /= self.capHeight()

        circ = Circle(self.p(0.5, rad),
                       self.p(0.5, 0.0),
                       self.weight())

        clipPoly = Polygon((self.p(0.0, rad), self.p(1.0, rad),
                            self.p(1.0, -1.0), self.p(0.0, -1.0)))

        circ = mergeSubPolys([circ]).intersection(
            mergeSubPolys([clipPoly]))

        s = self.weight() * 1.25 / self.capHeight()

        leftLine = Line(self.p(0.0 + shift, rad), self.p(0.0 + shift, 1.0 - s),
                        self.weight(), shift="right", serif=3)

        rightLine = Line(self.p(1.0 - shift, rad), self.p(1.0 - shift, 1.0 - s),
                         self.weight(), shift="left", serif=3)

        return [circ, leftLine, rightLine]

@glyph('V')
class VGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(VGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.baseWidth()

    def getPolygon(self):
        leftLine = Line(self.p(0.5, 0.0), self.p(0.0, 1.0),
                        self.weight(), shift="down", serif=3)
        rightLine = Line(self.p(0.5, 0.0), self.p(1.0, 1.0),
                         self.weight(), shift="down", serif=3)
        return [leftLine, rightLine]

@glyph('W')
class WGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(WGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em()

    def getPolygon(self):
        midHeight = (self.weight()) / self.capHeight()

        leftLine = Line(self.p(0.0, 0.0), self.p(0.0, 1.0),
                        self.weight(), shift="down", serif=3)
        downCrossLine = Line(self.p(0.0, 0.0),
                             self.p(0.5, 0.6 + midHeight),
                             self.weight())
        upCrossLine = Line(self.p(0.5, 0.6 + midHeight),
                           self.p(1.0, 0.0),
                           self.weight())
        rightLine = Line(self.p(1.0, 0.0), self.p(1.0, 1.0),
                         self.weight(), shift="down", serif=3)
        return [leftLine, downCrossLine, upCrossLine, rightLine]

@glyph('X')
class XGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(XGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.baseWidth()

    def getPolygon(self):
        upCrossLine = Line(self.p(0.0, 0.0), self.p(1.0, 1.0),
                           self.weight(), shift="down", serif=4)
        downCrossLine = Line(self.p(0.0, 1.0), self.p(1.0, 0.0),
                             self.weight(), shift="up", serif=4)
        return [upCrossLine, downCrossLine]

@glyph('Y')
class YGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(YGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.baseWidth()

    def getPolygon(self):
        # Try with xHeight off, too
        leftLine = Line(self.p(0.5, 0.5, xHeight=True), self.p(0.0, 1.0),
                        self.weight(), shift="down", serif=3)
        rightLine = Line(self.p(0.5, 0.5, xHeight=True), self.p(1.0, 1.0),
                         self.weight(), shift="down", serif=3)
        downLine = Line(self.p(0.5, 0.5, xHeight=True), self.p(0.5, 0.0),
                        self.weight(), serif=3)
        return [leftLine, rightLine, downLine]

@glyph('Z')
class ZGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(ZGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.baseWidth()

    # TODO: beveled line endings to fix this horribleness at large weights

    def getPolygon(self):
        topLine = Line(self.p(0.9, 1.0), self.p(0.1, 1.0),
                       self.weight(), shift="down", serif=1)
        slashLine = Line(self.p(0.9, 1.0), self.p(0.0, 0.0),
                         self.weight(), shift="down")
        bottomLine = Line(self.p(0.0, 0.0), self.p(1.0, 0.0),
                          self.weight(), shift="up", serif=1)
        return [topLine, slashLine, bottomLine]

@glyph('a')
class aGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(aGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.baseWidth()

    def getPolygon(self):
        circX = 0.5
        mainLine = Line(self.p(1.0, 0.0), self.p(1.0, 1.0, xHeight=True),
                        self.weight(), shift="down")
        circ = Circle(self.p(circX, 0.5, xHeight=True),
                      self.p(circX, 1.0, xHeight=True),
                      self.weight())
        return [circ, mainLine]

@glyph('b')
class bGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(bGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.baseWidth()

    def getPolygon(self):
        circX = 0.5
        mainLine = Line(self.p(0.0, 0.0), self.p(0.0, 1.0),
                        self.weight(), shift="down", serif=3)
        circ = Circle(self.p(circX, 0.5, xHeight=True),
                      self.p(circX, 1.0, xHeight=True),
                      self.weight())
        return [circ, mainLine]

@glyph('c')
class cGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(cGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.baseWidth()

    def getPolygon(self):
        circ = Circle(self.p(0.5, 0.5, xHeight=True),
                      self.p(0.5, 1.0, xHeight=True),
                      self.weight(),
                      semiA=self.p(1.0, 0.8, xHeight=True),
                      semiB=self.p(1.0, 0.2, xHeight=True))
        return [circ]

@glyph('d')
class dGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(dGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.baseWidth()

    def getPolygon(self):
        circX = 0.5
        mainLine = Line(self.p(1.0, 0.0), self.p(1.0, 1.0),
                        self.weight(), shift="down", serif=3)
        circ = Circle(self.p(circX, 0.5, xHeight=True),
                      self.p(circX, 1.0, xHeight=True),
                      self.weight())
        return [circ, mainLine]

@glyph('e')
class eGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(eGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.baseWidth()

    def getPolygon(self):
        rightShift = self.weight() / self.xHeight() * 0.025
        leftShift = self.weight() / self.xHeight() / 2
        circ = Circle(self.p(0.5, 0.5, xHeight=True),
                      self.p(0.5, 1.0, xHeight=True),
                      self.weight(),
                      semiA=self.p(1.0, 0.5, xHeight=True),
                      semiB=self.p(1.0, 0.2, xHeight=True),
                      serif=0)
        clipCirc = Circle(self.p(0.5, 0.5, xHeight=True),
                          self.p(0.5, 1.0, xHeight=True),
                          -1.0)
        midLine = Line(self.p(0.0, 0.5, xHeight=True),
                       self.p(1.0, 0.5, xHeight=True),
                       self.weight() / PHI)
        midLine = mergeSubPolys([midLine]).intersection(
                mergeSubPolys([clipCirc]))
        return [circ, midLine]

@glyph('i')
class iGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(iGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.baseWidth() / PHI

    def getPolygon(self):
        circY = (0.8 - (0.01 / (self.weight() / 5) * (self.capHeight() / 40.0)))
        circSize = 0.5 + ((0.6 * (self.weight() / 7)) /
                            (self.capHeight() / 40.0))
        mainLine = Line(self.p(0.5, 1.0, xHeight=True), self.p(0.5, 0.0),
                        self.weight(), shift="up", serif=5)
        circ = Circle(self.p(0.5, circY),
                      self.p(circSize, circY),
                      self.weight())
        return [circ, mainLine]

@glyph('k')
class kGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(kGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.baseWidth() / PHI

    def getPolygon(self):
        mainLine = Line(self.p(0.0, 0.0), self.p(0.0, 1.0),
                        self.weight(), shift="down", serif=4)
        topLine = Line(self.p(0.0, 0.5, xHeight=True),
                       self.p(1.0, 1.0, xHeight=True),
                       self.weight(), shift="down", serif=3, swapAngle=True)
        bottomLine = Line(self.p(0.0, 0.5, xHeight=True), self.p(1.0, 0.0),
                          self.weight(), shift="up", serif=3, swapAngle=True)
        return [topLine, bottomLine, mainLine]

@glyph('l')
class lGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(lGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.baseWidth() / PHI

    def getPolygon(self):
        mainLine = Line(self.p(0.5, 1.0), self.p(0.5, 0.0),
                        self.weight(), serif=5)
        return [mainLine]

@glyph('o')
class oGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(oGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.baseWidth()

    def getPolygon(self):
        circ = Circle(self.p(0.5, 0.5, xHeight=True),
                      self.p(0.5, 1.0, xHeight=True),
                      self.weight())
        return [circ]

@glyph('p')
class pGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(pGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.baseWidth()

    def getPolygon(self):
        circX = 0.5
        mainLine = Line(self.p(0.0, 1.0, xHeight=True),
                        self.p(0.0, -0.4, xHeight=True),
                        self.weight(), shift="down", serif=3)
        circ = Circle(self.p(circX, 0.5, xHeight=True),
                      self.p(circX, 1.0, xHeight=True),
                      self.weight())
        return [circ, mainLine]

@glyph('q')
class qGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(qGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.baseWidth()

    def getPolygon(self):
        circX = 0.5
        mainLine = Line(self.p(1.0, 1.0, xHeight=True),
                        self.p(1.0, -0.4, xHeight=True),
                        self.weight(), shift="down", serif=3)
        circ = Circle(self.p(circX, 0.5, xHeight=True),
                      self.p(circX, 1.0, xHeight=True),
                      self.weight())
        return [circ, mainLine]

@glyph('t')
class tGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(tGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.baseWidth() / PHI

    def getPolygon(self):
        mainLine = Line(self.p(0.5, 1.0), self.p(0.5, 0.0),
                        self.weight(), shift="up", serif=3)
        topLine = Line(self.p(0.0, 1.0, xHeight=True),
                       self.p(1.0, 1.0, xHeight=True),
                       self.weight() / PHI, shift="down")
        return [mainLine, topLine]

@glyph('v')
class vGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(vGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.baseWidth() / PHI

    def getPolygon(self):
        leftLine = Line(self.p(0.5, 0.0), self.p(0.0, 1.0, xHeight=True),
                        self.weight(), shift="down", serif=3)
        rightLine = Line(self.p(0.5, 0.0), self.p(1.0, 1.0, xHeight=True),
                         self.weight(), shift="down", serif=3)
        return [leftLine, rightLine]

@glyph('w')
class wGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(wGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.baseWidth() * 0.8

    def getPolygon(self):
        midHeight = (self.weight()) / self.xHeight()

        leftLine = Line(self.p(0.0, 0.0), self.p(0.0, 1.0, xHeight=True),
                        self.weight(), shift="down", serif=3)
        downCrossLine = Line(self.p(0.0, 0.0),
                             self.p(0.5, 0.6 + midHeight, xHeight=True),
                             self.weight())
        upCrossLine = Line(self.p(0.5, 0.6 + midHeight, xHeight=True),
                           self.p(1.0, 0.0),
                           self.weight())
        rightLine = Line(self.p(1.0, 0.0), self.p(1.0, 1.0, xHeight=True),
                         self.weight(), shift="down", serif=3)
        return [leftLine, downCrossLine, upCrossLine, rightLine]

@glyph('x')
class xGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(xGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.baseWidth() / PHI

    def getPolygon(self):
        upCrossLine = Line(self.p(0.0, 0.0, xHeight=True),
                           self.p(1.0, 1.0, xHeight=True),
                           self.weight(), shift="down", serif=4)
        downCrossLine = Line(self.p(0.0, 1.0, xHeight=True),
                             self.p(1.0, 0.0, xHeight=True),
                             self.weight(), shift="up", serif=4)
        return [upCrossLine, downCrossLine]

@glyph('z')
class zGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(zGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.baseWidth() / PHI

    def getPolygon(self):
        topLine = Line(self.p(0.9, 1.0, xHeight=True),
                       self.p(0.1, 1.0, xHeight=True),
                       self.weight(), shift="down", serif=1)
        slashLine = Line(self.p(0.9, 1.0, xHeight=True),
                         self.p(0.0, 0.0, xHeight=True),
                         self.weight(), shift="down")
        bottomLine = Line(self.p(0.0, 0.0, xHeight=True),
                          self.p(1.0, 0.0, xHeight=True),
                          self.weight(), shift="up", serif=1)
        return [topLine, slashLine, bottomLine]

@glyph('1')
class oneGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(oneGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.baseWidth() * 0.8

    def getPolygon(self):
        shift = (self.weight() / 2.0) / self.width()
        mainLine = Line(self.p(0.5, 1.0), self.p(0.5, 0.0),
                        self.weight(), serif=3)
        overLine = Line(self.p(0.5 - shift, 1.0), self.p(0.0, 0.7),
                        self.weight(), shift="down", noclip=2)
        return [mainLine, overLine]

@glyph('3')
class threeGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(threeGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.baseWidth()

    def getPolygon(self):
        shift = ((self.weight() / 2.0) / self.capHeight()) * 4
        bottomHeight = 0.5 #0.618
        bottomY = bottomHeight / 2.0
        bottomYY = bottomY + (bottomHeight / 2.0)
        topHeight = 1.0 - bottomHeight
        topY = bottomYY + (topHeight / 2.0)
        topYY = bottomYY

        bottomYY += shift / 2.0
        bottomY += shift / 4.0

        topYY -= shift / 2.0
        topY -= shift / 4.0

        circa = Circle(self.p(0.5, bottomY),
                       self.p(0.5, bottomYY),
                       self.weight())
        circb = Circle(self.p(0.5, topY),
                       self.p(0.5, topYY),
                       self.weight())

        clipPoly = Polygon((self.p(0.5, 0.0), self.p(0.5, 1.0),
                            self.p(1.5, 1.0), self.p(1.5, 0.0)))

        threePoly = mergeSubPolys([circa, circb]).intersection(
            mergeSubPolys([clipPoly]))

        topLine = Line(self.p(0.15, 1.0), self.p(0.5, 1.0),
                       self.weight(), shift="down")
        bottomLine = Line(self.p(0.15, 0.0), self.p(0.5, 0.0),
                          self.weight(), shift="up")

        return [threePoly, topLine, bottomLine]

@glyph('4')
class fourGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(fourGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.baseWidth()

    def getPolygon(self):
        shift = (self.weight() / 2.0) / self.width()
        mainLine = Line(self.p(0.7, 1.0), self.p(0.7, 0.0),
                        self.weight(), serif=3)
        overLine = Line(self.p(0.7 - shift, 1.0),
                        self.p(0.0, 0.5, xHeight=True),
                        self.weight(), shift="down")
        backLine = Line(self.p(1.0, 0.5, xHeight=True),
                        self.p(0.0, 0.5, xHeight=True),
                        self.weight(), shift="up")
        return [mainLine, overLine, backLine]

@glyph('7')
class sevenGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(sevenGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.baseWidth()

    def getPolygon(self):
        shift = (self.weight() / 2.0) / self.width()
        mainLine = Line(self.p(1.0, 1.0), self.p(0.3, 0.0),
                        self.weight(), serif=0)
        overLine = Line(self.p(0.0, 1.0),
                        self.p(1.0, 1.0),
                        self.weight(), shift="down")
        return [mainLine, overLine]

@glyph('8')
class eightGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(eightGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.baseWidth()

    def getPolygon(self):
        shift = ((self.weight() / 2.0) / self.capHeight()) * 3
        bottomHeight = 0.55
        bottomY = bottomHeight / 2.0
        bottomYY = bottomY + (bottomHeight / 2.0)
        topHeight = 1.0 - bottomHeight
        topY = bottomYY + (topHeight / 2.0)
        topYY = bottomYY

        bottomYY += shift
        bottomY += shift / 2.0

        circa = Circle(self.p(0.5, bottomY),
                       self.p(0.5, bottomYY),
                       self.weight())
        circb = Circle(self.p(0.5, topY),
                       self.p(0.5, topYY),
                       self.weight())
        return [circa, circb]
