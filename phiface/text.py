from glyph import Glyph, glyphs
from context import mergeSubPolys
from kerning import kernGlyphs

class TextBox(object):
    def __init__(self, box):
        #, x=0, y=0, text="Hello, World!", capHeight=100, tracking=0, weight=4, width=1200):
        super(TextBox, self).__init__()

        self.x = 0.0
        self.y = 0.0
        self.text = "Hello, World!"
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

        self.text = box.text

        self.leading = self.capHeight / 2.0

    def layoutGlyphs(self):
        allGlyphs = []

        xloc = self.x
        yloc = self.y

        metrics = Glyph(0, 0, capHeight=self.capHeight)

        for i in range(len(self.text)):
            a = self.text[i]
            print a

            if a == " ":
                xloc += metrics.em() + self.tracking
                continue

            if i + 1 < len(self.text):
                b = self.text[i + 1]
            else:
                b = None

            glyph = glyphs[a](x=0, y=0, capHeight=self.capHeight)
            glyph.w = (self.weight * (self.capHeight / 100.0))

            glyphBounds = mergeSubPolys([glyph]).bounds
            glyph.x = xloc
            glyph.y = yloc
            xShift = glyphBounds[2] - glyphBounds[0]

            if b is not " ":
                xShift += (kernGlyphs(a, b, self.weight,
                                      capHeight=self.capHeight) + self.tracking)

                if glyph.outlined:
                    xShift += (self.capHeight / 15.0)

            if xloc + xShift > self.width:
                xloc = self.x
                yloc += metrics.capHeight() + self.leading
                glyph.x = xloc
                glyph.y = yloc
                xloc += xShift
            else:
                xloc += xShift

            allGlyphs += [glyph]

        xloc = self.x
        yloc += metrics.capHeight() + self.leading

        return allGlyphs