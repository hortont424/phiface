from line import Line

class Glyph(object):
    def __init__(self, x, y):
        super(Glyph, self).__init__()
        self.x = x
        self.y = y

    def capHeight(self):
        return 100.0

    def baseWidth(self):
        return self.capHeight() / 1.618

    def width(self):
        pass

    def descenderDepth(self):
        pass

    def ascenderHeight(self):
        pass

    def xHeight(self):
        return self.capHeight() / 1.618

    def origin(self):
        return (self.x, self.y + self.capHeight())

    def originPlus(self, (x2, y2)):
        (x, y) = self.origin()
        return (x + x2, y + y2)

    def corner(self, l=False, b=False):
        (x, y) = self.origin()

        if l and b:
            return (x, y)
        elif l and not b:
            return (x, y - self.capHeight())
        elif not l and b:
            return (x + self.width(), y)
        elif not l and not b:
            return (x + self.width(), y - self.capHeight())

    def midpointH(self, b=False):
        (x, y) = self.origin()
        if not b:
            return (x + self.width() / 2.0, y - self.capHeight())
        else:
            return (x + self.width() / 2.0, y)

    def midpointV(self, xHeight=False):
        (x, y) = self.origin()
        height = self.capHeight()

        if xHeight:
            height = self.xHeight()

        return y - (height / 2.0)

class AGlyph(Glyph):
    def __init__(self, x, y):
        super(AGlyph, self).__init__(x, y)

    def width(self):
        return self.baseWidth()

    def getPolygon(self):
        leftLine = Line(self.origin(), self.midpointH(), 3)
        rightLine = Line(self.midpointH(), self.corner(l=False, b=True), 3)

        midHeight = self.midpointV(xHeight=True)
        midLeft = leftLine.atY(midHeight)
        midRight = rightLine.atY(midHeight)

        midLine = Line((midLeft, midHeight), (midRight, midHeight), 3)

        return [leftLine, rightLine, midLine]

class EGlyph(Glyph):
    def __init__(self, x, y):
        super(EGlyph, self).__init__(x, y)

    def width(self):
        return self.baseWidth()

    def getPolygon(self):
        leftLine = Line(self.origin(), self.corner(l=True, b=False), 3)
        topLine = Line(self.corner(l=True, b=False),
                       self.corner(l=False, b=False), 3, shift="down")
        bottomLine = Line(self.corner(l=True, b=True),
                          self.corner(l=False, b=True), 3, shift="up")

        midHeight = self.midpointV(xHeight=True)
        midLeft = leftLine.atY(midHeight)

        midLine = Line((midLeft, midHeight),
                       (midLeft + self.width() * 0.618, midHeight), 3)

        return [leftLine, topLine, midLine, bottomLine]
