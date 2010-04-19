#!/usr/bin/env python

import phiface

sc = phiface.Context()

xloc = yloc = 20
defaultKerning = 20
kerningPairs = {
    "A": {
        "E": 5,
        "T": -10
    },
    "H": {
        "I": 10
    },
    "I": {
        "T": 15
    },
    "T": {
        "V": 25
    },
    "V": {
        "H": 10
    }
}

demoStr = "AEFHITVL"

for weight in [1, 3, 5, 7]:
    for i in range(len(demoStr)):
        a = demoStr[i]

        if a == " ":
            xloc += 30
            continue

        if i + 1 < len(demoStr):
            b = demoStr[i + 1]
        else:
            b = None

        kerning = defaultKerning

        if b and (a in kerningPairs) and (b in kerningPairs[a]):
            kerning = kerningPairs[a][b]

        glyph = phiface.glyphs[a](x=xloc, y=yloc)
        glyph.w = (weight * (glyph.capHeight() / 100.0))
        glyphBounds = sc.mergeSubPolys([glyph]).bounds
        xloc += glyphBounds[2] - glyphBounds[0] + kerning
        sc.draw([glyph])
    xloc = 20
    yloc += 150

sc.write("output.png")