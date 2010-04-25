from glyph import Glyph, glyphs
from context import mergeSubPolys
from kerning import kernGlyphs

def layoutText(text):
    allGlyphs = []

    tracking = 0
    capHeight = 120
    leading = capHeight / 2.0
    xloc = initialX = 20.0
    yloc = initialY = 20.0
    weight = 4
    width = 1200

    metrics = Glyph(0, 0, capHeight=capHeight)

    for i in range(len(text)):
        a = text[i]
        print a

        if a == " ":
            xloc += metrics.em() + tracking
            continue

        if i + 1 < len(text):
            b = text[i + 1]
        else:
            b = None

        glyph = glyphs[a](x=0, y=0, capHeight=capHeight)
        glyph.w = (weight * (capHeight / 100.0))

        glyphBounds = mergeSubPolys([glyph]).bounds
        glyph.x = xloc
        glyph.y = yloc
        xShift = glyphBounds[2] - glyphBounds[0]

        if b is not " ":
            xShift += (kernGlyphs(a, b, weight, capHeight=capHeight) + tracking)

            if glyph.outlined:
                xShift += (capHeight / 15.0)

        if xloc + xShift > width:
            xloc = initialX
            yloc += metrics.capHeight() + leading
            glyph.x = xloc
            glyph.y = yloc
            xloc += xShift
        else:
            xloc += xShift

        allGlyphs += [glyph]

    xloc = initialX
    yloc += metrics.capHeight() + leading

    return allGlyphs