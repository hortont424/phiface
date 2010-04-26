# -*- coding: utf-8 -*-

from glyph import *

@glyph(u'—')
class emDashGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(emDashGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em()

    def getPolygon(self):
        super(emDashGlyph, self).setupDrawing()

        mainLine = Line(self.p(0.0, 0.5), self.p(1.0, 0.5),
                        self.weight())

        return [mainLine]

@glyph('-')
class hyphenGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(hyphenGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em()

    def getPolygon(self):
        super(hyphenGlyph, self).setupDrawing()

        mainLine = Line(self.p(0.25, 0.5), self.p(0.75, 0.5),
                        self.weight() / PHI)

        return [mainLine]

@glyph('=')
class equalsGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(equalsGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.em()

    def getPolygon(self):
        super(equalsGlyph, self).setupDrawing()

        topLine = Line(self.p(0.2, 0.57), self.p(0.8, 0.57),
                       self.weight() / PHI)
        bottomLine = Line(self.p(0.2, 0.43), self.p(0.8, 0.43),
                          self.weight() / PHI)

        return [topLine, bottomLine]

@glyph('+')
class plusGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(plusGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.capHeight()

    def getPolygon(self):
        super(plusGlyph, self).setupDrawing()

        mainLine = Line(self.p(0.25, 0.5), self.p(0.75, 0.5),
                        self.weight() / PHI)
        downLine = Line(self.p(0.5, 0.25), self.p(0.5, 0.75),
                        self.weight() / PHI)

        return [mainLine, downLine]

@glyph(u'·')
class midDotGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(midDotGlyph, self).__init__(x, y, capHeight)
        self.autoKern = False

    def width(self):
        return self.em() / PHI

    def getPolygon(self):
        super(midDotGlyph, self).setupDrawing()

        circSize = 0.5 + ((0.6 * (self.weight() / 7)) /
                            (self.capHeight() / 40.0))

        circY = 0.5
        circ = Circle(self.p(0.5, circY),
                      self.p(circSize, circY),
                      -1.0)
        return [circ]

@glyph('.')
class periodGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(periodGlyph, self).__init__(x, y, capHeight)
        #self.autoKern = False

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
        #self.autoKern = False

    def width(self):
        return self.em() / PHI

    def getPolygon(self):
        super(commaGlyph, self).setupDrawing()

        mainLine = Line(self.p(0.5, 0.1), self.p(0.35, -0.15), self.weight())
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
        circ = Circle(self.p(0.5, 1.0 - circY, xHeight=True),
                      self.p(circSize, 1.0 - circY, xHeight=True),
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
        topcirc = Circle(self.p(0.5, 1.0 - circY, xHeight=True),
                         self.p(circSize, 1.0 - circY, xHeight=True),
                         -1.0)
        return [circ, topcirc]

@glyph('\'')
class quoteGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(quoteGlyph, self).__init__(x, y, capHeight)
        self.autoKern = False

    def width(self):
        return self.em() / PHI

    def getPolygon(self):
        super(quoteGlyph, self).setupDrawing()

        mainLine = Line(self.p(0.5, 1.1), self.p(0.35, 0.85), self.weight())
        return [mainLine]

@glyph('"')
class doubleQuoteGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(doubleQuoteGlyph, self).__init__(x, y, capHeight)
        self.autoKern = False

    def width(self):
        return self.em() / PHI

    def getPolygon(self):
        super(doubleQuoteGlyph, self).setupDrawing()

        shift = 0.2 + (self.weight() / self.width()) * 2.0

        mainLine = Line(self.p(0.5, 1.1), self.p(0.35, 0.85), self.weight())
        secondLine = Line(self.p(0.5 + shift, 1.1),
                          self.p(0.35 + shift, 0.85), self.weight())
        return [mainLine, secondLine]

@glyph('`')
class backQuoteGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(backQuoteGlyph, self).__init__(x, y, capHeight)
        self.autoKern = False

    def width(self):
        return self.em() / PHI

    def getPolygon(self):
        super(backQuoteGlyph, self).setupDrawing()

        mainLine = Line(self.p(0.35, 1.1), self.p(0.5, 0.85), self.weight())
        return [mainLine]

@glyph(u'“')
class doubleBackQuoteGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(doubleBackQuoteGlyph, self).__init__(x, y, capHeight)
        self.autoKern = False

    def width(self):
        return self.em() / PHI

    def getPolygon(self):
        super(doubleBackQuoteGlyph, self).setupDrawing()

        shift = 0.2 + (self.weight() / self.width()) * 2.0

        mainLine = Line(self.p(0.35, 1.1), self.p(0.5, 0.85), self.weight())
        secondLine = Line(self.p(0.35 + shift, 1.1),
                          self.p(0.5 + shift, 0.85), self.weight())
        return [mainLine, secondLine]

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

        bottomLine = Line(self.p(0.5, 0.0),
                        self.p(0.5, 0.45), self.weight())

        topLine = Line(self.p(0.5, 0.55),
                        self.p(0.5, 1.0), self.weight())

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

@glyph('<')
class lessThanGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(lessThanGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.capHeight()

    def getPolygon(self):
        super(lessThanGlyph, self).setupDrawing()

        bottomLine = Line(self.p(0.0, 0.5),
                          self.p(0.5, 0.0), self.weight(),
                          noclip=True, shift="up")

        topLine = Line(self.p(0.0, 0.5),
                       self.p(0.5, 1.0), self.weight(),
                       noclip=True)

        return [bottomLine, topLine]

@glyph('>')
class greaterThanGlyph(Glyph):
    def __init__(self, x, y, capHeight):
        super(greaterThanGlyph, self).__init__(x, y, capHeight)

    def width(self):
        return self.capHeight()

    def getPolygon(self):
        super(greaterThanGlyph, self).setupDrawing()

        bottomLine = Line(self.p(0.5, 0.5),
                          self.p(0.0, 0.0), self.weight(),
                          noclip=True, shift="up")

        topLine = Line(self.p(0.5, 0.5),
                       self.p(0.0, 1.0), self.weight(),
                       noclip=True)

        return [bottomLine, topLine]
