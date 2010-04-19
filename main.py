#!/usr/bin/env python

import phiface

sc = phiface.Context()

xloc = yloc = 20
defaultKerning = 20
kerningPairs = {
    "A": {
        "E": 5,
        "L": 10,
        "T": -10,
        "V": -10,
        "W": 10
    },
    "H": {
        "default": 10
    },
    "I": {
        "T": 15
    },
    "L": {
        "default": 10,
        "V": -5
    },
    "M": {
        "default": 5
    },
    "N": {
        "T": 5
    },
    "T": {
        "V": 25
    },
    "V": {
        "E": 0,
        "H": 10,
        "I": 5
    },
    "W": {
        "E": 10
    }
}

#demoStr = "HALF WENT VIM AT HIT AVE AWW LET LIE LEM LIVE"
demoStr = "AEFHILMNTVWXYZx"
metrics = phiface.Glyph(0,0)

for weight in [1, 3, 5, 7]:
    for i in range(len(demoStr)):
        a = demoStr[i]

        if a == " ":
            xloc += (metrics.em() / 1.618)
            continue

        if i + 1 < len(demoStr):
            b = demoStr[i + 1]
        else:
            b = None

        kerning = defaultKerning

        if (a in kerningPairs) and ("default" in kerningPairs[a]):
            kerning = kerningPairs[a]["default"]

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

sc.write("output.png")