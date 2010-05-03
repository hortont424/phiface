# -*- coding: utf-8 -*-

from glyph import *

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

        rw = self.weight() / self.capHeight() * 100

        if rw >= 7.0:
            topYY -= (self.weight() / self.capHeight()) * 0.0725
        elif rw >= 5.0:
            topYY -= (self.weight() / self.capHeight()) * 0.09
        elif rw >= 3.0:
            topYY -= (self.weight() / self.capHeight()) * 0.14
        elif rw >= 2.0:
            topYY -= (self.weight() / self.capHeight()) * 0.205
        elif rw >= 0.5:
            topYY -= (self.weight() / self.capHeight()) * 0.81

        circa = Circle(self.p(0.45, bottomY),
                       self.p(0.45, bottomYY),
                       self.weight())
        circb = Circle(self.p(0.55, topY),
                       self.p(0.55, topYY),
                       self.weight())

        bclipPoly = Polygon((self.p(0.5, topY), self.p(1.2, 1.1),
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
