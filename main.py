#!/usr/bin/env python

import phiface
from shapely.geometry import *

sc = phiface.Context()

xloc = yloc = 20
defaultKerning = 10
kerningPairs = {
    "A": {
        "T": -10,
        "V": -10
    },
    "E": {
        "M": 15
    },
    "I": {
        "L": 20,
        "M": 20
    }
}

demoStr = "HALF WENT VIM AT HIT AVE AWW LET LIE LEM LIVE"
#demoStr = "AVEFHILMNTVWXYZx"
metrics = phiface.Glyph(0,0)

def autoKern(a, b, weight):
    if not (a in phiface.glyphs and b in phiface.glyphs):
        return metrics.em() / 1.618

    aGlyph = phiface.glyphs[a](x=0, y=0)
    aBounds = sc.mergeSubPolys([aGlyph]).bounds

    for i in range(2, -30, -1):
        advance = (aBounds[2] - aBounds[0]) + i
        bGlyph = phiface.glyphs[b](x=advance, y=0)
        if type(sc.mergeSubPolys([aGlyph, bGlyph])) is Polygon:
            return i
    print "BAD THING"

for weight in [0.5, 1, 3, 5, 7]:
    for i in range(len(demoStr)):
        a = demoStr[i]

        if a == " ":
            xloc += (metrics.em() / 1.618)
            continue

        if i + 1 < len(demoStr):
            b = demoStr[i + 1]
        else:
            b = None

        kerning = autoKern(a, b, weight) + defaultKerning

        if b and (a in kerningPairs) and (b in kerningPairs[a]):
            kerning = kerningPairs[a][b]

        glyph = phiface.glyphs[a](x=xloc, y=yloc)
        glyph.w = (weight * (glyph.capHeight() / 100.0))

        kerning *= (glyph.capHeight() / 100.0)
        glyphBounds = sc.mergeSubPolys([glyph]).bounds
        xShift = glyphBounds[2] - glyphBounds[0]

        if b is not " ":
            xShift += kerning

        if xloc + xShift > sc.width:
            xloc = 20
            yloc += metrics.capHeight() + 50
            glyph.x = xloc
            glyph.y = yloc
            xloc += xShift
        else:
            xloc += xShift
        sc.draw([glyph])
    xloc = 20
    yloc += metrics.capHeight() + 50

sc.write()