from line import Line

PHI = 1.618

class Glyph(object):
    def __init__(self, x, y):
        super(Glyph, self).__init__()
        self.x = x
        self.y = y
        self.w = 3

    def capHeight(self):
        return 150.0

    def baseWidth(self):
        return self.capHeight() / PHI

    def width(self):
        pass

    def weight(self):
        return self.w

    def descenderDepth(self):
        pass

    def ascenderHeight(self):
        pass

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
        leftLine = Line(self.p(0.0, 0.0), self.p(0.5, 1.0), self.weight())
        rightLine = Line(self.p(0.5, 1.0), self.p(1.0, 0.0), self.weight())

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
        leftLine = Line(self.p(0.0, 0.0), self.p(0.0, 1.0), self.weight())
        topLine = Line(self.p(0.0, 1.0), self.p(1.0, 1.0),
                       self.weight(), shift="down")
        bottomLine = Line(self.p(0.0, 0.0), self.p(1.0, 0.0),
                          self.weight(), shift="up")

        midHeight = self.p(0.0, 0.5, xHeight=True)[1]
        midLeft = leftLine.atY(midHeight)

        midLine = Line((midLeft, midHeight),
                       (midLeft + self.width() / PHI, midHeight),
                       self.weight())

        return [leftLine, topLine, midLine, bottomLine]

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
