from line import Line

class Glyph(object):
    def __init__(self):
        super(Glyph, self).__init__()

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
        return (30.0, 30 + self.capHeight())

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
    def __init__(self):
        super(AGlyph, self).__init__()

    def width(self):
        return self.baseWidth()

    def getPolygon(self):
        leftLine = Line(self.origin(), self.midpointH(), 3)
        rightLine = Line(self.midpointH(), self.corner(l=False, b=True), 3)


        midHeight = self.midpointV(xHeight=True)
        midLeft = self.origin()[0] + leftLine.atY(midHeight)
        midRight = self.origin()[0] + rightLine.atY(midHeight)
        print midLeft, midRight

        midLine = Line((midLeft, midHeight), (midRight, midHeight), 3)

        return [leftLine, rightLine, midLine]
