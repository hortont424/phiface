from glyph import Glyph, glyphs
from context import mergeSubPolys
from kerning import kernGlyphs

class TextBox(object):
    def __init__(self, box):
        super(TextBox, self).__init__()

        self.x = 0.0
        self.y = 0.0
        self.tracking = 0
        self.capHeight = 100
        self.weight = 4
        self.width = 1200

        # Pull in integer properties
        for prop in ["x", "y", "width"]:
            if prop in box.attrib:
                setattr(self, prop, int(box.attrib[prop]))

        # Pull in float properties
        for prop in ["tracking", "capHeight", "leading", "weight"]:
            if prop in box.attrib:
                setattr(self, prop, float(box.attrib[prop]))

        self.leading = self.capHeight / 2.0

        self.glyphs = []

        self.addXMLChunk(box)

    def addXMLChunk(self, chunk, weight=0, italic=False):
        if chunk.text:
            self.addTextChunk(chunk.text, weight=weight, italic=italic)
        for el in chunk:
            newWeight = weight
            newItalic = italic

            if el.tag == "b":
                newWeight = weight + 2
            elif el.tag == "t":
                newWeight = weight - 2
            elif el.tag == "i":
                newItalic = True
            self.addXMLChunk(el, weight=newWeight, italic=newItalic)
            if el.tail:
                self.addTextChunk(el.tail, weight=weight, italic=italic)

    def addTextChunk(self, text, weight=0, italic=False):
        for i in range(len(text)):
            a = text[i]

            if a == " ":
                self.glyphs += [None]
                continue

            glyph = glyphs[a](x=0, y=0, capHeight=self.capHeight)
            glyph.w = ((self.weight + weight) * (self.capHeight / 100.0))
            glyph.slanted = italic

            self.glyphs += [glyph]

    def layoutGlyphs(self):
        allGlyphs = []

        xloc = self.x
        yloc = self.y

        metrics = Glyph(0, 0, capHeight=self.capHeight)

        for i in range(len(self.glyphs)):
            a = self.glyphs[i]

            if a == None:
                xloc += metrics.em() + self.tracking
                continue

            if i + 1 < len(self.glyphs):
                b = self.glyphs[i + 1]
            else:
                b = None

            glyphBounds = mergeSubPolys([a]).bounds
            a.x = xloc
            a.y = yloc
            xShift = glyphBounds[2] - glyphBounds[0]

            if b is not None:
                xShift += (kernGlyphs(a.char, b.char, self.weight,
                                      capHeight=self.capHeight) + self.tracking)

                if a.outlined:
                    xShift += (self.capHeight / 15.0)

            if xloc + xShift > self.width:
                xloc = self.x
                yloc += metrics.capHeight() + self.leading
                a.x = xloc
                a.y = yloc
                xloc += xShift
            else:
                xloc += xShift

            allGlyphs += [a]

        xloc = self.x
        yloc += metrics.capHeight() + self.leading

        return allGlyphs