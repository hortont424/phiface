# -*- coding: utf-8 -*-

import line
import circle
from line import Line
from circle import Circle
from context import mergeSubPolys
from shapely.geometry import *

from math import *

PHI = 1.618

glyphs = {}

def glyph(g):
    def wrap(cls):
        glyphs[g] = cls
        cls.char = g
        return cls
    return wrap

class Glyph(object):
    def __init__(self, x, y, capHeight=50):
        super(Glyph, self).__init__()
        self.x = x
        self.y = y
        self.w = 3
        self.pointSize = capHeight
        self.slanted = False
        self.outlined = False
        self.color = (0.0, 0.0, 0.0, 1.0)
        self.serifed = True
        self.autoKern = True

    def capHeight(self):
        return self.pointSize

    def em(self):
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

    def setupDrawing(self):
        circle.capHeight = line.capHeight = self.capHeight()
        circle.drawSerifs = line.drawSerifs = self.serifed

@glyph('A')
class AGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(AGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em()

    def getPolygon(self):
        super(AGlyph, self).setupDrawing()

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
        return self.em()

    def getPolygon(self):
        super(BGlyph, self).setupDrawing()

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
        super(CGlyph, self).setupDrawing()

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
        super(DGlyph, self).setupDrawing()

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
        return self.em()

    def getPolygon(self):
        super(EGlyph, self).setupDrawing()

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
        return self.em()

    def getPolygon(self):
        super(FGlyph, self).setupDrawing()

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
        super(GGlyph, self).setupDrawing()

        leftShift = self.weight() / self.capHeight()

        circ = Circle(self.p(0.5, 0.5),
                      self.p(0.5, 1.0),
                      self.weight())

        clipPoly = Polygon((self.p(0.5, 0.5), self.p(1.0, 0.8),
                            self.p(1.0, 0.5, xHeight=True),
                            self.p(0.5, 0.5, xHeight=True)))

        circ = mergeSubPolys([circ]).difference(
            mergeSubPolys([clipPoly]))

        midLine = Line(self.p(1.0, 0.5, xHeight=True),
                       self.p(0.5, 0.5, xHeight=True),
                       self.weight())

        lineClip = Circle(self.p(0.5, 0.5),
                         self.p(0.5, 1.0),
                         -1.0)

        midLine = mergeSubPolys([midLine]).intersection(
            mergeSubPolys([lineClip]))

        return [circ, midLine]

@glyph('H')
class HGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(HGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em()

    def getPolygon(self):
        super(HGlyph, self).setupDrawing()

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
        return self.em() / PHI

    def getPolygon(self):
        super(IGlyph, self).setupDrawing()

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
        return self.em() / PHI

    def getPolygon(self):
        super(JGlyph, self).setupDrawing()

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
        return self.em() * 0.8

    def getPolygon(self):
        super(KGlyph, self).setupDrawing()

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
        return self.em() / PHI

    def getPolygon(self):
        super(LGlyph, self).setupDrawing()

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
        super(MGlyph, self).setupDrawing()

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
        return self.em()

    def getPolygon(self):
        super(NGlyph, self).setupDrawing()

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
        super(OGlyph, self).setupDrawing()

        circ = Circle(self.p(0.5, 0.5),
                      self.p(0.5, 1.0),
                      self.weight())
        return [circ]

@glyph('P')
class PGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(PGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em()

    def getPolygon(self):
        super(PGlyph, self).setupDrawing()

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
        super(QGlyph, self).setupDrawing()

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
        return self.em()

    def getPolygon(self):
        super(RGlyph, self).setupDrawing()

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

@glyph('S')
class SGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(SGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em()

    def getPolygon(self):
        super(SGlyph, self).setupDrawing()

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

        circa = Circle(self.p(0.45, bottomY),
                       self.p(0.45, bottomYY),
                       self.weight())
        circb = Circle(self.p(0.55, topY),
                       self.p(0.55, topYY),
                       self.weight())

        bclipPoly = Polygon((self.p(0.5, topY), self.p(1.0, 0.9),
                            self.p(1.0, -1.0), self.p(0.5, -1.0)))

        circb = mergeSubPolys([circb]).difference(
            mergeSubPolys([bclipPoly]))

        aclipPoly = Polygon((self.p(0.5, bottomY), self.p(-1.0, -0.25),
                            self.p(-1.0, 1.0), self.p(0.5, 1.0)))

        circa = mergeSubPolys([circa]).difference(
            mergeSubPolys([aclipPoly]))

        return [circa, circb]

@glyph('T')
class TGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(TGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em()

    def getPolygon(self):
        super(TGlyph, self).setupDrawing()

        mainLine = Line(self.p(0.5, 0.0), self.p(0.5, 1.0), self.weight())
        topLine = Line(self.p(0.0, 1.0), self.p(1.0, 1.0),
                       self.weight(), shift="down", serif=2)
        return [mainLine, topLine]

@glyph('U')
class UGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(UGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em()

    def getPolygon(self):
        super(UGlyph, self).setupDrawing()

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
        return self.em()

    def getPolygon(self):
        super(VGlyph, self).setupDrawing()

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
        super(WGlyph, self).setupDrawing()

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
        return self.em()

    def getPolygon(self):
        super(XGlyph, self).setupDrawing()

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
        return self.em()

    def getPolygon(self):
        super(YGlyph, self).setupDrawing()

        # Try with xHeight off, too
        # TODO: Something is wrong with how this attaches at large weights

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
        return self.em()

    def getPolygon(self):
        super(ZGlyph, self).setupDrawing()

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
        return self.em()

    def getPolygon(self):
        super(aGlyph, self).setupDrawing()

        circX = 0.5
        mainLine = Line(self.p(1.0, 0.0), self.p(1.0, 1.0, xHeight=True),
                        self.weight(), shift="leftdown")
        circ = Circle(self.p(circX, 0.5, xHeight=True),
                      self.p(circX, 1.0, xHeight=True),
                      self.weight())
        return [circ, mainLine]

@glyph('b')
class bGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(bGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em()

    def getPolygon(self):
        super(bGlyph, self).setupDrawing()

        circX = 0.5
        mainLine = Line(self.p(0.0, 0.0), self.p(0.0, 1.0),
                        self.weight(), shift="rightdown", serif=3)
        circ = Circle(self.p(circX, 0.5, xHeight=True),
                      self.p(circX, 1.0, xHeight=True),
                      self.weight())
        return [circ, mainLine]

@glyph('c')
class cGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(cGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em()

    def getPolygon(self):
        super(cGlyph, self).setupDrawing()

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
        return self.em()

    def getPolygon(self):
        super(dGlyph, self).setupDrawing()

        circX = 0.5
        mainLine = Line(self.p(1.0, 0.0), self.p(1.0, 1.0),
                        self.weight(), shift="leftdown", serif=3)
        circ = Circle(self.p(circX, 0.5, xHeight=True),
                      self.p(circX, 1.0, xHeight=True),
                      self.weight())
        return [circ, mainLine]

@glyph('e')
class eGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(eGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em()

    def getPolygon(self):
        super(eGlyph, self).setupDrawing()

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

@glyph('f')
class fGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(fGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em()

    def getPolygon(self):
        super(fGlyph, self).setupDrawing()

        height = 0.691
        mainLine = Line(self.p(0.0, height), self.p(0.0, 0.0),
                        self.weight(), shift="right", serif=3)
        circ = Circle(self.p(0.5, height),
                      self.p(0.5, 1.0),
                      self.weight())
        clipPoly = Polygon((self.p(0.0, height),
                            self.p(0.618, height),
                            self.p(0.618, 1.0),
                            self.p(1.0, 1.0),
                            self.p(1.0, 0.0),
                            self.p(0.0, 0.0)))

        circ = mergeSubPolys([circ]).difference(
            mergeSubPolys([clipPoly]))

        topLine = Line(self.p(-0.25, 1.0, xHeight=True),
                       self.p(0.5, 1.0, xHeight=True),
                       self.weight() / PHI, shift="down")

        return [circ, mainLine, topLine]

@glyph('g')
class gGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(gGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em()

    def getPolygon(self):
        super(gGlyph, self).setupDrawing()

        circX = 0.5
        mainLine = Line(self.p(1.0, 1.0, xHeight=True),
                        self.p(1.0, 0.0, xHeight=True),
                        self.weight(), shift="left")
        circ = Circle(self.p(circX, 0.5, xHeight=True),
                      self.p(circX, 1.0, xHeight=True),
                      self.weight())

        bcirc = Circle(self.p(0.5, 0.0),
                       self.p(1.0, 0.0),
                       self.weight())
        bclipPoly = Polygon((self.p(0.5, 0.0), self.p(1.0, 0.0),
                             self.p(1.0, -1.0), self.p(0.5, -1.0)))

        bcirc = mergeSubPolys([bcirc]).intersection(
            mergeSubPolys([bclipPoly]))

        return [circ, mainLine, bcirc]

@glyph('h')
class hGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(hGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em()

    def getPolygon(self):
        super(hGlyph, self).setupDrawing()

        mWidth = 0.4

        mainLine = Line(self.p(0.0, 1.0), self.p(0.0, 0.0),
                        self.weight(), shift="right", serif=4)
        midLine = Line(self.p(mWidth * 2.0, (1.0 - mWidth), xHeight=True),
                       self.p(mWidth * 2.0, 0.0),
                       self.weight(), shift="left", serif=3)
        circ = Circle(self.p(mWidth, (1.0 - mWidth), xHeight=True),
                      self.p(mWidth, 1.0, xHeight=True),
                      self.weight())
        clipPoly = Polygon((self.p(0.0, (1.0 - mWidth), xHeight=True),
                            self.p(1.0, (1.0 - mWidth), xHeight=True),
                            self.p(1.0, 0.0, xHeight=True),
                            self.p(0.0, 0.0)))

        circ = mergeSubPolys([circ]).difference(
            mergeSubPolys([clipPoly]))

        return [circ, mainLine, midLine]

@glyph('i')
class iGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(iGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em() / PHI

    def getPolygon(self):
        super(iGlyph, self).setupDrawing()

        circY = (0.8 - (0.01 / (self.weight() / 5) * (self.capHeight() / 40.0)))
        circSize = 0.5 + ((0.6 * (self.weight() / 7)) /
                            (self.capHeight() / 40.0))
        mainLine = Line(self.p(0.5, 1.0, xHeight=True), self.p(0.5, 0.0),
                        self.weight(), shift="up", serif=5)
        circ = Circle(self.p(0.5, circY),
                      self.p(circSize, circY),
                      self.weight())
        return [circ, mainLine]

@glyph('j')
class jGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(jGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em() / PHI

    def getPolygon(self):
        super(jGlyph, self).setupDrawing()

        #dotX = 1.0 - ((self.weight() / 10.0) / (self.capHeight() / 40.0)) + 0.05
        dotX = 1.0 - (self.weight() / self.capHeight()) * 3.0
        dotY = (0.8 - (0.01 / (self.weight() / 5) * (self.capHeight() / 40.0)))
        dotSize = ((0.6 * (self.weight() / 7)) /
                            (self.capHeight() / 40.0))
        dot = Circle(self.p(dotX, dotY),
                      self.p(dotX + dotSize, dotY),
                      self.weight())
        mainLine = Line(self.p(1.0, 1.0, xHeight=True), self.p(1.0, 0.0),
                        self.weight(), shift="left", serif=6)
        circ = Circle(self.p(0.5, 0.0),
                      self.p(1.0, 0.0),
                      self.weight())
        clipPoly = Polygon((self.p(0.5, 0.0), self.p(1.0, 0.0),
                            self.p(1.0, -1.0), self.p(0.5, -1.0)))

        circ = mergeSubPolys([circ]).intersection(
            mergeSubPolys([clipPoly]))

        return [mainLine, circ, dot]

@glyph('k')
class kGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(kGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em() / PHI

    def getPolygon(self):
        super(kGlyph, self).setupDrawing()

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
        return self.em() / PHI

    def getPolygon(self):
        super(lGlyph, self).setupDrawing()

        mainLine = Line(self.p(0.5, 1.0), self.p(0.5, 0.0),
                        self.weight(), serif=5)
        return [mainLine]

@glyph('m')
class mGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(mGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em()

    def getPolygon(self):
        super(mGlyph, self).setupDrawing()

        mWidth = 0.4
        sh = self.weight() / self.width() * 2.0

        mainLine = Line(self.p(0.0, 1.0, xHeight=True), self.p(0.0, 0.0),
                        self.weight(), shift="right", serif=5)
        midLine = Line(self.p(mWidth * 2.0, (1.0 - mWidth), xHeight=True),
                       self.p(mWidth * 2.0, 0.0),
                       self.weight(), shift="left", serif=3)
        rightLine = Line(self.p(mWidth * 4.0 - sh, 1.0 - mWidth, xHeight=True),
                         self.p(mWidth * 4.0 - sh, 0.0),
                         self.weight(), shift="left", serif=3)
        circa = Circle(self.p(mWidth, (1.0 - mWidth), xHeight=True),
                       self.p(mWidth, 1.0, xHeight=True),
                       self.weight())
        circb = Circle(self.p(mWidth * 3.0 - sh, (1.0 - mWidth), xHeight=True),
                       self.p(mWidth * 3.0 - sh, 1.0, xHeight=True),
                       self.weight())
        clipPoly = Polygon((self.p(0.0, (1.0 - mWidth), xHeight=True),
                            self.p(2.0, (1.0 - mWidth), xHeight=True),
                            self.p(2.0, 0.0, xHeight=True),
                            self.p(0.0, 0.0)))

        circ = mergeSubPolys([circa, circb]).difference(
            mergeSubPolys([clipPoly]))

        return [circ, mainLine, midLine, rightLine]

@glyph('n')
class nGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(nGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em()

    def getPolygon(self):
        super(nGlyph, self).setupDrawing()

        mWidth = 0.4

        mainLine = Line(self.p(0.0, 1.0, xHeight=True), self.p(0.0, 0.0),
                        self.weight(), shift="right", serif=5)
        midLine = Line(self.p(mWidth * 2.0, (1.0 - mWidth), xHeight=True),
                       self.p(mWidth * 2.0, 0.0),
                       self.weight(), shift="left", serif=3)
        circ = Circle(self.p(mWidth, (1.0 - mWidth), xHeight=True),
                      self.p(mWidth, 1.0, xHeight=True),
                      self.weight())
        clipPoly = Polygon((self.p(0.0, (1.0 - mWidth), xHeight=True),
                            self.p(1.0, (1.0 - mWidth), xHeight=True),
                            self.p(1.0, 0.0, xHeight=True),
                            self.p(0.0, 0.0)))

        circ = mergeSubPolys([circ]).difference(
            mergeSubPolys([clipPoly]))

        return [circ, mainLine, midLine]

@glyph('o')
class oGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(oGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em()

    def getPolygon(self):
        super(oGlyph, self).setupDrawing()

        circ = Circle(self.p(0.5, 0.5, xHeight=True),
                      self.p(0.5, 1.0, xHeight=True),
                      self.weight())
        return [circ]

@glyph('p')
class pGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(pGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em()

    def getPolygon(self):
        super(pGlyph, self).setupDrawing()

        circX = 0.5
        mainLine = Line(self.p(0.0, 1.0, xHeight=True),
                        self.p(0.0, -0.4, xHeight=True),
                        self.weight(), shift="rightdown", serif=3)
        circ = Circle(self.p(circX, 0.5, xHeight=True),
                      self.p(circX, 1.0, xHeight=True),
                      self.weight())
        return [circ, mainLine]

@glyph('q')
class qGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(qGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em()

    def getPolygon(self):
        super(qGlyph, self).setupDrawing()

        circX = 0.5
        mainLine = Line(self.p(1.0, 1.0, xHeight=True),
                        self.p(1.0, -0.4, xHeight=True),
                        self.weight(), shift="leftdown", serif=3)
        circ = Circle(self.p(circX, 0.5, xHeight=True),
                      self.p(circX, 1.0, xHeight=True),
                      self.weight())
        return [circ, mainLine]

@glyph('r')
class rGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(rGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em()

    def getPolygon(self):
        super(rGlyph, self).setupDrawing()

        mainLine = Line(self.p(0.0, 1.0, xHeight=True), self.p(0.0, 0.0),
                        self.weight(), shift="right", serif=5)
        circ = Circle(self.p(0.5, 0.5, xHeight=True),
                      self.p(0.5, 1.0, xHeight=True),
                      self.weight())
        clipPoly = Polygon((self.p(0.0, 0.5, xHeight=True),
                            self.p(0.618, 0.5, xHeight=True),
                            self.p(0.618, 1.0, xHeight=True),
                            self.p(1.0, 1.0, xHeight=True),
                            self.p(1.0, 0.0, xHeight=True),
                            self.p(0.0, 0.0)))

        circ = mergeSubPolys([circ]).difference(
            mergeSubPolys([clipPoly]))

        return [circ, mainLine]

@glyph('s')
class sGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(sGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em()

    def getPolygon(self):
        super(sGlyph, self).setupDrawing()

        shift = ((self.weight() / 2.0) / self.xHeight()) * 4
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

        circa = Circle(self.p(0.48, bottomY, xHeight=True),
                       self.p(0.48, bottomYY, xHeight=True),
                       self.weight())
        circb = Circle(self.p(0.52, topY, xHeight=True),
                       self.p(0.52, topYY, xHeight=True),
                       self.weight())

        bclipPoly = Polygon((self.p(0.5, topY, xHeight=True),
                             self.p(1.0, 0.8, xHeight=True),
                             self.p(1.0, -1.0, xHeight=True),
                             self.p(0.5, -1.0, xHeight=True)))

        circb = mergeSubPolys([circb]).difference(
            mergeSubPolys([bclipPoly]))

        aclipPoly = Polygon((self.p(0.5, bottomY, xHeight=True),
                             self.p(-1.0, -0.2, xHeight=True),
                             self.p(-1.0, 1.0, xHeight=True),
                             self.p(0.5, 1.0, xHeight=True)))

        circa = mergeSubPolys([circa]).difference(
            mergeSubPolys([aclipPoly]))

        return [circa, circb]

@glyph('t')
class tGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(tGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em() / PHI

    def getPolygon(self):
        super(tGlyph, self).setupDrawing()

        mainLine = Line(self.p(0.5, 1.0), self.p(0.5, 0.0),
                        self.weight(), shift="up", serif=3)
        topLine = Line(self.p(0.0, 1.0, xHeight=True),
                       self.p(1.0, 1.0, xHeight=True),
                       self.weight() / PHI, shift="down")
        return [mainLine, topLine]

@glyph('u')
class uGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(uGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em() * 0.8

    def getPolygon(self):
        super(uGlyph, self).setupDrawing()

        rad = 0.4
        shift = (self.p(0.5, rad, xHeight=True)[0] -
                 self.p(0.0, 0.0, xHeight=True)[0])
        shift -= (self.p(0.5, 0.0, xHeight=True)[1] -
                  self.p(0.5, rad, xHeight=True)[1])
        shift /= self.capHeight()

        circ = Circle(self.p(0.5, rad, xHeight=True),
                       self.p(0.5, 0.0, xHeight=True),
                       self.weight())

        clipPoly = Polygon((self.p(0.0, rad, xHeight=True),
                            self.p(1.0, rad, xHeight=True),
                            self.p(1.0, -1.0, xHeight=True),
                            self.p(0.0, -1.0, xHeight=True)))

        circ = mergeSubPolys([circ]).intersection(
            mergeSubPolys([clipPoly]))

        s = self.weight() * 1.25 / self.xHeight()

        leftLine = Line(self.p(0.0 + shift, rad, xHeight=True),
                        self.p(0.0 + shift, 1.0 - s, xHeight=True),
                        self.weight(), shift="right", serif=3)

        rightLine = Line(self.p(1.0 - shift, rad, xHeight=True),
                         self.p(1.0 - shift, 1.0 - s, xHeight=True),
                         self.weight(), shift="left", serif=3)

        return [circ, leftLine, rightLine]

@glyph('v')
class vGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(vGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em() / PHI

    def getPolygon(self):
        super(vGlyph, self).setupDrawing()

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
        return self.em() * 0.8

    def getPolygon(self):
        super(wGlyph, self).setupDrawing()

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
        return self.em() / PHI

    def getPolygon(self):
        super(xGlyph, self).setupDrawing()

        upCrossLine = Line(self.p(0.0, 0.0, xHeight=True),
                           self.p(1.0, 1.0, xHeight=True),
                           self.weight(), shift="down", serif=4)
        downCrossLine = Line(self.p(0.0, 1.0, xHeight=True),
                             self.p(1.0, 0.0, xHeight=True),
                             self.weight(), shift="up", serif=4)
        return [upCrossLine, downCrossLine]

@glyph('y')
class yGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(yGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em() / PHI

    def getPolygon(self):
        super(yGlyph, self).setupDrawing()

        leftLine = Line(self.p(0.5, 0.0), self.p(0.0, 1.0, xHeight=True),
                        self.weight(), shift="down", serif=3)
        rightLine = Line(self.p(0.5, 0.0), self.p(1.0, 1.0, xHeight=True),
                         self.weight(), shift="down", serif=3)
        downLine = Line(self.p(1.0, 1.0, xHeight=True),
                        self.p(0.25, -0.5, xHeight=True),
                        self.weight(), shift="up", serif=3)
        return [leftLine, rightLine, downLine]

@glyph('z')
class zGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(zGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em() / PHI

    def getPolygon(self):
        super(zGlyph, self).setupDrawing()

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

@glyph('0')
class zeroGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(zeroGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.capHeight()

    def getPolygon(self):
        super(zeroGlyph, self).setupDrawing()

        circ = Circle(self.p(0.5, 0.5),
                      self.p(0.5, 1.0),
                      self.weight())

        crossLine = Line(self.p(0.5 + 0.25 * sqrt(2.0), 0.5 + 0.25 * sqrt(2.0)),
                         self.p(0.5 - 0.25 * sqrt(2.0), 0.5 - 0.25 * sqrt(2.0)),
                         self.weight() / PHI)

        return [circ, crossLine]

@glyph('1')
class oneGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(oneGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em() * 0.8

    def getPolygon(self):
        super(oneGlyph, self).setupDrawing()

        shift = (self.weight() / 2.0) / self.width()
        mainLine = Line(self.p(0.5, 1.0), self.p(0.5, 0.0),
                        self.weight(), serif=3)
        overLine = Line(self.p(0.5 - shift, 1.0), self.p(0.0, 0.7),
                        self.weight(), shift="down", noclip=2)
        return [mainLine, overLine]

@glyph('2')
class twoGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(twoGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em()

    def getPolygon(self):
        super(twoGlyph, self).setupDrawing()

        shift = ((self.weight() / 2.0) / self.capHeight()) * 4
        bottomHeight = 0.47 - (0.1 * (self.weight() / 6.0))
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

        circb = mergeSubPolys([circb]).difference(
            mergeSubPolys([Polygon((
                self.p(0.5, topY), self.p(0.0, topY),
                self.p(0.0, 0.0), self.p(0.5, 0.0)
            ))]))

        circa = mergeSubPolys([circa]).difference(
            mergeSubPolys([Polygon((
                self.p(0.5, 0.0), self.p(0.5, 1.0),
                self.p(1.5, 1.0), self.p(1.5, 0.0)
            ))])).difference(
            mergeSubPolys([Polygon((
                self.p(0.5, bottomY), self.p(-1.0, bottomY),
                self.p(-1.0, 0.0), self.p(0.5, 0.0)
            ))]))

        dshift = ((self.p(0.0, bottomY)[1] - self.p(0.0, bottomYY)[1]) /
                  self.width())

        downLine = Line(self.p(0.5 - dshift, bottomY),
                        self.p(0.5 - dshift, 0.0),
                        self.weight(), shift="right")

        overLine = Line(self.p(0.5 - dshift, 0.0),
                        self.p(1.0, 0.0),
                        self.weight(), shift="up")

        return [circa, circb, downLine, overLine]

@glyph('3')
class threeGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(threeGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em()

    def getPolygon(self):
        super(threeGlyph, self).setupDrawing()

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

        topLine = Line(self.p(0.5, 1.0), self.p(0.15, 1.0),
                       self.weight(), shift="down")
        bottomLine = Line(self.p(0.5, 0.0), self.p(0.15, 0.0),
                          self.weight(), shift="up")

        return [threePoly, topLine, bottomLine]

@glyph('4')
class fourGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(fourGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em()

    def getPolygon(self):
        super(fourGlyph, self).setupDrawing()

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

@glyph('5')
class fiveGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(fiveGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em()

    def getPolygon(self):
        super(fiveGlyph, self).setupDrawing()

        shift = ((self.weight() / 2.0) / self.capHeight()) * 4
        bottomHeight = 0.5
        bottomY = bottomHeight / 2.0
        bottomYY = bottomY + (bottomHeight / 2.0)
        topHeight = 1.0 - bottomHeight

        bottomYY += shift
        bottomY += shift / 2.0

        shift = 0.18

        circa = Circle(self.p(0.5, bottomY),
                       self.p(0.5, bottomYY),
                       self.weight())

        clipPoly = Polygon((self.p(0.5, bottomY), self.p(0.0, bottomYY),
                            self.p(-1.0, -0.5)))

        circa = mergeSubPolys([circa]).difference(
            mergeSubPolys([clipPoly]))

        clipPoly = Polygon((self.p(shift, 1.0), self.p(shift, bottomY),
                            self.p(0.0, bottomY), self.p(0.0, 1.0)))

        circa = mergeSubPolys([circa]).difference(
            mergeSubPolys([clipPoly]))

        upLine = Line(self.p(shift, bottomY),
                      self.p(shift, 1.0),
                      self.weight(), shift="right")

        clipUpLine = Circle(self.p(0.5, bottomY),
                       self.p(0.5, bottomYY),
                       -1.0)

        upLine = mergeSubPolys([upLine]).difference(
            mergeSubPolys([clipUpLine]))

        overLine = Line(self.p(shift, 1.0),
                        self.p(0.9, 1.0),
                        self.weight(), shift="leftdown")

        return [circa, upLine, overLine]

@glyph('6')
class sixGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(sixGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em()

    def getPolygon(self):
        super(sixGlyph, self).setupDrawing()

        shift = ((self.weight() / 2.0) / self.capHeight()) * 4
        bottomHeight = 0.5
        bottomY = bottomHeight / 2.0
        bottomYY = bottomY + (bottomHeight / 2.0)
        topHeight = 1.0 - bottomHeight
        topY = bottomYY + (topHeight / 2.0)
        topYY = bottomYY

        bottomYY += shift
        bottomY += shift / 2.0

        hshift = self.weight() / self.width()

        height = 0.691
        mainLine = Line(self.p(0.00, height + 0.01), self.p(-0.005, bottomY),
                        self.weight(), shift="right")
        circ = Circle(self.p(0.5, height),
                      self.p(0.5, 1.0),
                      self.weight())
        clipPoly = Polygon((self.p(0.0, height),
                            self.p(0.5, height),
                            self.p(1.0, 1.3),
                            self.p(1.0, 0.0),
                            self.p(0.0, 0.0)))

        circ = mergeSubPolys([circ]).difference(
            mergeSubPolys([clipPoly]))

        circa = Circle(self.p(0.398 + hshift, bottomY),
                       self.p(0.398 + hshift, bottomYY),
                       self.weight())

        mainLineClip = Circle(self.p(0.398 + hshift, bottomY),
                              self.p(0.398 + hshift, bottomYY),
                              -1)

        mainLine = mergeSubPolys([mainLine]).difference(
            mergeSubPolys([mainLineClip]))

        return [circ, mainLine, circa]

@glyph('7')
class sevenGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(sevenGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em()

    def getPolygon(self):
        super(sevenGlyph, self).setupDrawing()

        shift = (self.weight() / 2.0) / self.width()
        mainLine = Line(self.p(1.0, 1.0), self.p(0.3, 0.0),
                        self.weight(), serif=0)
        overLine = Line(self.p(1.0, 1.0),
                        self.p(0.1, 1.0),
                        self.weight(), shift="down", serif=1)
        return [mainLine, overLine]

@glyph('8')
class eightGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(eightGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em()

    def getPolygon(self):
        super(eightGlyph, self).setupDrawing()

        shift = ((self.weight() / 2.0) / self.capHeight()) * 4
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

@glyph('9')
class nineGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(nineGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em() / PHI

    def getPolygon(self):
        super(nineGlyph, self).setupDrawing()

        shift = ((self.weight() / 2.0) / self.capHeight()) * 4
        bottomHeight = 0.4
        bottomY = bottomHeight / 2.0
        bottomYY = bottomY + (bottomHeight / 2.0)
        topHeight = 1.0 - bottomHeight
        topY = bottomYY + (topHeight / 2.0)
        topYY = bottomYY

        #bottomYY += shift
        #bottomY += shift / 2.0

        hshift = self.weight() / self.width()

        height = 0.309
        circCenter = .398 + hshift

        mainLine = Line(self.p(1.185, topY - topYY), self.p(1.185, topY),
                        self.weight())
        circ = Circle(self.p(circCenter, topY - topYY),
                      self.p(circCenter, 0.0),
                      self.weight())
        clipPoly = Polygon((self.p(circCenter, topY - topYY),
                            self.p(1.5, topY - topYY),
                            self.p(1.5, 0.0),
                            self.p(circCenter - 0.4, 0.0)))

        circ = mergeSubPolys([circ]).intersection(
            mergeSubPolys([clipPoly]))

        circa = Circle(self.p(0.398 + hshift, topY),
                       self.p(0.398 + hshift, topYY),
                       self.weight())

        mainLineClip = Circle(self.p(0.398 + hshift, topY),
                              self.p(0.398 + hshift, topYY),
                              -1)

        mainLine = mergeSubPolys([mainLine]).difference(
            mergeSubPolys([mainLineClip]))

        return [circa, mainLine, circ]

@glyph('.')
class periodGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(periodGlyph, self).__init__(x, y, capHeight)
        self.autoKern = False

    def width(self):
        return self.em() / PHI

    def getPolygon(self):
        super(periodGlyph, self).setupDrawing()

        circSize = 0.5 + ((0.6 * (self.weight() / 7)) /
                            (self.capHeight() / 40.0))

        circY = (circSize - 0.5) / 3.0
        circ = Circle(self.p(0.5, circY),
                      self.p(circSize, circY),
                      -1.0)
        return [circ]

@glyph(',')
class commaGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(commaGlyph, self).__init__(x, y, capHeight)
        self.autoKern = False

    def width(self):
        return self.em() / PHI

    def getPolygon(self):
        super(commaGlyph, self).setupDrawing()

        mainLine = Line(self.p(0.5, 0.1), self.p(0.4, -0.1), self.weight())
        return [mainLine]

@glyph(';')
class semicolonGlyph(commaGlyph):
    def __init__(self, x, y, capHeight):
        super(semicolonGlyph, self).__init__(x, y, capHeight)
        self.autoKern = False

    def getPolygon(self):
        super(semicolonGlyph, self).setupDrawing()
        parentPoly = super(semicolonGlyph, self).getPolygon()

        circSize = 0.5 + ((0.6 * (self.weight() / 7)) /
                            (self.capHeight() / 40.0))

        circY = (circSize - 0.5) / 3.0
        circ = Circle(self.p(0.5, 0.8 - circY),
                      self.p(circSize, 0.8 - circY),
                      -1.0)

        return [parentPoly, circ]

@glyph(':')
class colonGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(colonGlyph, self).__init__(x, y, capHeight)
        self.autoKern = False

    def width(self):
        return self.em() / PHI

    def getPolygon(self):
        super(colonGlyph, self).setupDrawing()

        circSize = 0.5 + ((0.6 * (self.weight() / 7)) /
                            (self.capHeight() / 40.0))

        circY = (circSize - 0.5) / 3.0
        circ = Circle(self.p(0.5, circY),
                      self.p(circSize, circY),
                      -1.0)
        topcirc = Circle(self.p(0.5, 0.8 - circY),
                         self.p(circSize, 0.8 - circY),
                         -1.0)
        return [circ, topcirc]

@glyph('!')
class exclamationGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(exclamationGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em() / PHI

    def getPolygon(self):
        super(exclamationGlyph, self).setupDrawing()

        circSize = 0.5 + ((0.6 * (self.weight() / 7)) /
                            (self.capHeight() / 40.0))

        circY = (circSize - 0.5) / 3.0
        circ = Circle(self.p(0.5, circY),
                      self.p(circSize, circY),
                      -1.0)

        mainLine = Line(self.p(0.5, 1.0),
                        self.p(0.5, circY * 2 + 0.15), self.weight())

        return [circ, mainLine]

@glyph('?')
class questionGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(questionGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em() / PHI

    def getPolygon(self):
        super(questionGlyph, self).setupDrawing()

        circSize = 0.5 + ((0.6 * (self.weight() / 7)) /
                            (self.capHeight() / 40.0))

        circY = (circSize - 0.5) / 3.0
        circ = Circle(self.p(0.5, circY),
                      self.p(circSize, circY),
                      -1.0)

        topCirc = Circle(self.p(0.5, 0.75),
                         self.p(0.5, 1.0),
                         self.weight())

        clipPoly = Polygon((self.p(0.5, 0.75), self.p(-1.0, 0.75),
                            self.p(-1.0, 0.0), self.p(0.5, 0.0)))

        topCirc = mergeSubPolys([topCirc]).difference(
            mergeSubPolys([clipPoly]))

        shift = (self.weight() / self.capHeight()) * 2.0

        mainLine = Line(self.p(0.5, 0.5 + shift),
                        self.p(0.5, circY * 2 + 0.15), self.weight())

        return [circ, mainLine, topCirc]

@glyph(u'‽')
class interrobangGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(interrobangGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em() / PHI

    def getPolygon(self):
        super(interrobangGlyph, self).setupDrawing()

        circSize = 0.5 + ((0.6 * (self.weight() / 7)) /
                            (self.capHeight() / 40.0))

        circY = (circSize - 0.5) / 3.0
        circ = Circle(self.p(0.5, circY),
                      self.p(circSize, circY),
                      -1.0)

        topCirc = Circle(self.p(0.5, 0.75),
                         self.p(0.5, 1.0),
                         self.weight())

        clipPoly = Polygon((self.p(0.5, 0.75), self.p(-1.0, 0.75),
                            self.p(-1.0, 0.0), self.p(0.5, 0.0)))

        topCirc = mergeSubPolys([topCirc]).difference(
            mergeSubPolys([clipPoly]))

        mainLine = Line(self.p(0.5, 0.75),
                        self.p(0.5, circY * 2 + 0.15), self.weight())

        return [circ, mainLine, topCirc]

@glyph('/')
class fwSlashGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(fwSlashGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em() / PHI / PHI

    def getPolygon(self):
        super(fwSlashGlyph, self).setupDrawing()

        mainLine = Line(self.p(0.0, -0.1),
                        self.p(1.0, 0.9), self.weight(), noclip=True)

        return [mainLine]

@glyph('\\')
class bkSlashGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(bkSlashGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em() / PHI / PHI

    def getPolygon(self):
        super(bkSlashGlyph, self).setupDrawing()

        mainLine = Line(self.p(1.0, -0.1),
                        self.p(0.0, 0.9), self.weight(), noclip=True)

        return [mainLine]

@glyph('|')
class pipeGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(pipeGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em() / PHI / PHI

    def getPolygon(self):
        super(pipeGlyph, self).setupDrawing()

        bottomLine = Line(self.p(0.0, 0.0),
                        self.p(0.0, 0.45), self.weight())

        topLine = Line(self.p(0.0, 0.55),
                        self.p(0.0, 1.0), self.weight())

        return [topLine, bottomLine]

@glyph('[')
class openSquareBracketGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(openSquareBracketGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em() / PHI

    def getPolygon(self):
        super(openSquareBracketGlyph, self).setupDrawing()

        width = (self.weight() / self.capHeight()) * 10.0

        mainLine = Line(self.p(0.0, 0.0),
                        self.p(0.0, 1.0), self.weight(), shift="right")
        topLine = Line(self.p(0.0, 1.0),
                       self.p(width, 1.0), self.weight(), shift="down")
        bottomLine = Line(self.p(0.0, 0.0),
                          self.p(width, 0.0), self.weight(), shift="up")

        return [mainLine, topLine, bottomLine]

@glyph(']')
class closeSquareBracketGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(closeSquareBracketGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em() / PHI / PHI

    def getPolygon(self):
        super(closeSquareBracketGlyph, self).setupDrawing()

        width = (self.weight() / self.capHeight()) * 10.0

        mainLine = Line(self.p(1.0, 0.0),
                        self.p(1.0, 1.0), self.weight(), shift="right")
        topLine = Line(self.p(1.0, 1.0),
                       self.p(1.0 - width, 1.0), self.weight(), shift="down")
        bottomLine = Line(self.p(1.0, 0.0),
                          self.p(1.0 - width, 0.0), self.weight(), shift="up")

        return [mainLine, topLine, bottomLine]

@glyph('(')
class openParenGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(openParenGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em() / PHI

    def getPolygon(self):
        super(openParenGlyph, self).setupDrawing()

        circSize = 3.0

        circ = Circle(self.p(circSize, 0.5),
                      self.p(circSize * 2.0, 0.5),
                      self.weight())

        clipPoly = Polygon((self.p(0.0, 0.0), self.p(1.0, 0.0),
                            self.p(1.0, 1.0), self.p(0.0, 1.0)))

        circ = mergeSubPolys([circ]).intersection(
            mergeSubPolys([clipPoly]))

        return [circ]

@glyph(')')
class closeParenGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(closeParenGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em() / PHI

    def getPolygon(self):
        super(closeParenGlyph, self).setupDrawing()

        circSize = 3.0

        circ = Circle(self.p(-circSize + 1.0, 0.5),
                      self.p(-circSize * 2.0 + 1.0, 0.5),
                      self.weight())

        clipPoly = Polygon((self.p(0.0, 0.0), self.p(1.0, 0.0),
                            self.p(1.0, 1.0), self.p(0.0, 1.0)))

        circ = mergeSubPolys([circ]).intersection(
            mergeSubPolys([clipPoly]))

        return [circ]
