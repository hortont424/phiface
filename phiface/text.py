# -*- coding: utf-8 -*-

from glyph import Glyph, glyphs
from context import mergeSubPolys
from kerning import kernGlyphs
from punctuation import spaceGlyph

class LineBreak(object):
    def __init__(self, leading):
        super(LineBreak, self).__init__()

        self.leading = leading

class TextBox(object):
    def __init__(self, box, parent):
        super(TextBox, self).__init__()

        self.x = 0.0
        self.y = 0.0
        self.tracking = 0
        self.size = 100
        self.weight = 3.0
        self.width = int(parent.attrib["width"])
        self.serif = True
        self.leading = None

        # Pull in integer properties
        for prop in ["x", "y", "width"]:
            if prop in box.attrib:
                setattr(self, prop, int(box.attrib[prop]))

        # Pull in float properties
        for prop in ["tracking", "size", "leading", "weight"]:
            if prop in box.attrib:
                setattr(self, prop, float(box.attrib[prop]))

        if self.leading == None:
            self.leading = self.size / 2.0

        self.glyphs = []

        self.addXMLChunk(box)

    def addXMLChunk(self, chunk, weight=None, italic=False, capHeight=None,
                    color=None, serif=None, tracking=None, leading=None):
        if chunk.text:
            self.addTextChunk(chunk.text, weight=weight, italic=italic,
                              capHeight=capHeight, color=color, serif=serif,
                              tracking=tracking, leading=leading)
        for el in chunk:
            newWeight = weight
            newItalic = italic
            newCapHeight = capHeight
            newColor = color
            newSerif = serif
            newTracking = tracking
            newLeading = leading

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
            elif el.tag == "leading":
                newLeading = float(el.attrib["px"])
            elif el.tag == "tracking":
                newTracking = float(el.attrib["px"])
            elif el.tag == "size":
                newCapHeight = float(el.attrib["px"])
                if newLeading == None:
                    newLeading = newCapHeight / 2.0
            elif el.tag == "br":
                self.addTextChunk("\n", capHeight=capHeight, leading=newLeading,
                                  stripNewline=False)
            elif el.tag == "color":
                newColor = (float(el.attrib["r"]),
                            float(el.attrib["g"]),
                            float(el.attrib["b"]),
                            float(el.attrib["a"]))
            elif el.tag == "sans":
                newSerif = False
            elif el.tag == "serif":
                newSerif = True

            self.addXMLChunk(el, weight=newWeight, italic=newItalic,
                             capHeight=newCapHeight, color=newColor,
                             serif=newSerif, tracking=newTracking,
                             leading=newLeading)
            if el.tail:
                self.addTextChunk(el.tail, weight=weight, italic=italic,
                                  capHeight=capHeight, color=color,
                                  serif=serif, tracking=tracking,
                                  leading=leading)

    def addTextChunk(self, text, weight=None, italic=False, capHeight=None,
                     stripNewline=True, color=None, serif=None, tracking=None,
                     leading=None):
        for i in range(len(text)):
            a = text[i]

            if weight == None:
                weight = self.weight

            if capHeight == None:
                capHeight = self.size

            if color == None:
                color = (0.0, 0.0, 0.0, 1.0)

            if serif == None:
                serif = self.serif

            if tracking == None:
                tracking = self.tracking

            if leading == None:
                leading = self.leading

            #if a == " ":
            #    self.glyphs += [" "]
            #    continue

            if a == "\n":
                if not stripNewline:
                    self.glyphs += [LineBreak(leading)]
                continue

            glyph = glyphs[a](x=0, y=0, capHeight=capHeight)
            glyph.w = (weight * (glyph.capHeight() / 100.0))
            glyph.slanted = italic
            glyph.color = color
            glyph.willBeSerifed = serif
            glyph.tracking = tracking

            self.glyphs += [glyph]

    def layoutGlyphs(self):
        allGlyphs = []
        wordGlyphs = []

        xloc = self.x
        yloc = self.y

        metrics = Glyph(0, 0, capHeight=self.size)

        for i in range(len(self.glyphs)):
            a = self.glyphs[i]

            if i + 1 < len(self.glyphs):
                b = self.glyphs[i + 1]
            else:
                b = None

            if isinstance(a, LineBreak):
                xloc = self.x
                yloc += metrics.capHeight() + a.leading

                allGlyphs += wordGlyphs
                wordGlyphs = []
                continue

            glyphBounds = mergeSubPolys([a]).bounds
            a.x = xloc
            a.y = yloc
            xShift = glyphBounds[2] - glyphBounds[0]

            if isinstance(b, Glyph):
                xShift += (kernGlyphs(a.char, b.char, a.weight(),
                                      capHeight=a.capHeight()) + a.tracking)

                if a.outlined:
                    xShift += (a.capHeight() / 15.0)

            xloc += xShift

            if isinstance(a, spaceGlyph):
                if len(wordGlyphs):
                    if xloc > self.width:
                        xloc = self.x
                        yloc += metrics.capHeight() + self.leading

                    allGlyphs += wordGlyphs
                    wordGlyphs = []
            else:
                wordGlyphs += [a]

        allGlyphs += wordGlyphs

        for g in allGlyphs:
            g.serifed = g.willBeSerifed

        return allGlyphs
