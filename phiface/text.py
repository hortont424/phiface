from glyph import Glyph, glyphs
from context import mergeSubPolys
from kerning import kernGlyphs

class TextBox(object):
    def __init__(self, box):
        super(TextBox, self).__init__()

        self.x = 0.0
        self.y = 0.0
        self.tracking = 0
        self.size = 100
        self.weight = 3.0
        self.width = 1200

        # Pull in integer properties
        for prop in ["x", "y", "width"]:
            if prop in box.attrib:
                setattr(self, prop, int(box.attrib[prop]))

        # Pull in float properties
        for prop in ["tracking", "size", "leading", "weight"]:
            if prop in box.attrib:
                setattr(self, prop, float(box.attrib[prop]))

        self.leading = self.size / 2.0

        self.glyphs = []

        self.addXMLChunk(box)

    def addXMLChunk(self, chunk, weight=None, italic=False, capHeight=None):
        if chunk.text:
            self.addTextChunk(chunk.text, weight=weight, italic=italic,
                              capHeight=capHeight)
        for el in chunk:
            newWeight = weight
            newItalic = italic
            newCapHeight = capHeight

            if el.tag == "u":
                newWeight = 0.5
            elif el.tag == "l":
                newWeight = 2.0
            elif el.tag == "m":
                newWeight = 3.0
            elif el.tag == "b":
                newWeight = 5.0
            elif el.tag == "h":
                newWeight = 7.0
            elif el.tag == "i":
                newItalic = True
            elif el.tag == "size":
                newCapHeight = int(el.attrib["px"])
            elif el.tag == "br":
                self.addTextChunk("\n", capHeight=capHeight, stripNewline=False)

            self.addXMLChunk(el, weight=newWeight, italic=newItalic,
                             capHeight=newCapHeight)
            if el.tail:
                self.addTextChunk(el.tail, weight=weight, italic=italic,
                                  capHeight=capHeight)

    def addTextChunk(self, text, weight=None, italic=False, capHeight=None,
                     stripNewline=True):
        for i in range(len(text)):
            a = text[i]

            if weight == None:
                weight = self.weight

            if capHeight == None:
                capHeight = self.size

            if a == " ":
                self.glyphs += [" "]
                continue

            if a == "\n":
                if not stripNewline:
                    self.glyphs += ["\n"]
                continue

            glyph = glyphs[a](x=0, y=0, capHeight=capHeight)
            glyph.w = (weight * (glyph.capHeight() / 100.0))
            glyph.slanted = italic

            self.glyphs += [glyph]

    def layoutGlyphs(self):
        allGlyphs = []

        xloc = self.x
        yloc = self.y

        metrics = Glyph(0, 0, capHeight=self.size)

        for i in range(len(self.glyphs)):
            a = self.glyphs[i]

            if a == " ":
                xloc += metrics.em() + self.tracking
                continue

            if a == "\n":
                xloc = self.x
                yloc += metrics.capHeight() + self.leading
                continue

            if i + 1 < len(self.glyphs):
                b = self.glyphs[i + 1]
            else:
                b = None

            glyphBounds = mergeSubPolys([a]).bounds
            a.x = xloc
            a.y = yloc
            xShift = glyphBounds[2] - glyphBounds[0]

            if isinstance(b, Glyph):
                xShift += (kernGlyphs(a.char, b.char, a.weight(),
                                      capHeight=a.capHeight()) + self.tracking)

                if a.outlined:
                    xShift += (a.capHeight() / 15.0)

            if xloc + xShift > self.width:
                xloc = self.x
                yloc += metrics.capHeight() + self.leading
                a.x = xloc
                a.y = yloc
                xloc += xShift
            else:
                xloc += xShift

            allGlyphs += [a]

        return allGlyphs