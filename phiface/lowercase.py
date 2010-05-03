# -*- coding: utf-8 -*-

from glyph import *

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

        rw = self.weight() / self.capHeight() * 100

        if rw >= 7.0:
            topYY -= (self.weight() / self.xHeight()) * 0.0275
        elif rw >= 5.0:
            topYY -= (self.weight() / self.xHeight()) * 0.03
        elif rw >= 3.0:
            topYY -= (self.weight() / self.xHeight()) * 0.04
        elif rw >= 2.0:
            topYY -= (self.weight() / self.xHeight()) * 0.06
        elif rw >= 0.5:
            topYY -= (self.weight() / self.xHeight()) * 0.22

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