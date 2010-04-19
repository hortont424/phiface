import line
from line import Line

PHI = 1.618

class Glyph(object):
    def __init__(self, x, y):
        super(Glyph, self).__init__()
        self.x = x
        self.y = y
        self.w = 3
        line.capHeight = self.capHeight()

    def capHeight(self):
        return 70.0

    def em(self):
        return self.baseWidth() * PHI * 0.8

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

class AGlyph(Glyph):
    def __init__(self, x, y):
        super(AGlyph, self).__init__(x, y)

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

class EGlyph(Glyph):
    def __init__(self, x, y):
        super(EGlyph, self).__init__(x, y)

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

class FGlyph(Glyph):
    def __init__(self, x, y):
        super(FGlyph, self).__init__(x, y)

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

class HGlyph(Glyph):
    def __init__(self, x, y):
        super(HGlyph, self).__init__(x, y)

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

class IGlyph(Glyph):
    def __init__(self, x, y):
        super(IGlyph, self).__init__(x, y)

    def width(self):
        return self.baseWidth() / PHI

    def getPolygon(self):
        mainLine = Line(self.p(0.5, 0.0), self.p(0.5, 1.0), self.weight())
        topLine = Line(self.p(0.0, 1.0), self.p(1.0, 1.0),
                       self.weight(), shift="down")
        bottomLine = Line(self.p(0.0, 0.0), self.p(1.0, 0.0),
                          self.weight(), shift="up")
        return [mainLine, topLine, bottomLine]

class LGlyph(Glyph):
    def __init__(self, x, y):
        super(LGlyph, self).__init__(x, y)

    def width(self):
        return self.baseWidth() / PHI

    def getPolygon(self):
        mainLine = Line(self.p(0.0, 0.0), self.p(0.0, 1.0),
                        self.weight(), shift="down", serif=3)
        bottomLine = Line(self.p(0.0, 0.0), self.p(1.0, 0.0),
                          self.weight(), shift="up", serif=1)
        return [mainLine, bottomLine]

class MGlyph(Glyph):
    def __init__(self, x, y):
        super(MGlyph, self).__init__(x, y)

    def width(self):
        return self.em()

    def getPolygon(self):
        midHeight = (self.weight()) / self.capHeight() #BORKEN

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

class NGlyph(Glyph):
    def __init__(self, x, y):
        super(NGlyph, self).__init__(x, y)

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

class TGlyph(Glyph):
    def __init__(self, x, y):
        super(TGlyph, self).__init__(x, y)

    def width(self):
        return self.baseWidth()

    def getPolygon(self):
        mainLine = Line(self.p(0.5, 0.0), self.p(0.5, 1.0), self.weight())
        topLine = Line(self.p(0.0, 1.0), self.p(1.0, 1.0),
                       self.weight(), shift="down", serif=2)
        return [mainLine, topLine]

class VGlyph(Glyph):
    def __init__(self, x, y):
        super(VGlyph, self).__init__(x, y)

    def width(self):
        return self.baseWidth()

    def getPolygon(self):
        leftLine = Line(self.p(0.5, 0.0), self.p(0.0, 1.0),
                        self.weight(), shift="down", serif=3)
        rightLine = Line(self.p(0.5, 0.0), self.p(1.0, 1.0),
                         self.weight(), shift="down", serif=3)
        return [leftLine, rightLine]

class WGlyph(Glyph):
    def __init__(self, x, y):
        super(WGlyph, self).__init__(x, y)

    def width(self):
        return self.em()

    def getPolygon(self):
        midHeight = (self.weight()) / self.capHeight() #BORKEN

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

class XGlyph(Glyph):
    def __init__(self, x, y):
        super(XGlyph, self).__init__(x, y)

    def width(self):
        return self.baseWidth()

    def getPolygon(self):
        upCrossLine = Line(self.p(0.0, 0.0), self.p(1.0, 1.0),
                           self.weight(), shift="down", serif=4)
        downCrossLine = Line(self.p(0.0, 1.0), self.p(1.0, 0.0),
                             self.weight(), shift="up", serif=4)
        return [upCrossLine, downCrossLine]

class YGlyph(Glyph):
    def __init__(self, x, y):
        super(YGlyph, self).__init__(x, y)

    def width(self):
        return self.baseWidth()

    def getPolygon(self):

        leftLine = Line(self.p(0.5, 0.5, xHeight=True), self.p(0.0, 1.0),
                        self.weight(), shift="down", serif=3)
        rightLine = Line(self.p(0.5, 0.5, xHeight=True), self.p(1.0, 1.0),
                         self.weight(), shift="down", serif=3)
        downLine = Line(self.p(0.5, 0.5, xHeight=True), self.p(0.5, 0.0),
                        self.weight(), shift="up", serif=3)
        return [leftLine, rightLine, downLine]

class xGlyph(Glyph):
    def __init__(self, x, y):
        super(xGlyph, self).__init__(x, y)

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

glyphs = {
    "A": AGlyph,
    "E": EGlyph,
    "F": FGlyph,
    "H": HGlyph,
    "I": IGlyph,
    "L": LGlyph,
    "M": MGlyph,
    "N": NGlyph,
    "T": TGlyph,
    "V": VGlyph,
    "W": WGlyph,
    "X": XGlyph,
    "Y": YGlyph,
    "x": xGlyph
}