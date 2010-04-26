# -*- coding: utf-8 -*-

from glyph import *

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
                self.p(0.5, topY), self.p(-1.0, topY),
                self.p(-1.0, 0.0), self.p(0.5, 0.0)
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
                        self.weight(), shift="up", serif=2)

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
                        self.weight(), shift="leftdown", serif=1)

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