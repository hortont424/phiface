#!/usr/bin/env python

import phiface

sc = phiface.Context()

xloc = yloc = 20

demoStr = "HALF WENT VIM AT HIT AVE AWW LET LIE LEM LIVE"
#demoStr = "AVEFHILMNTVWXYZx"
metrics = phiface.Glyph(0,0)

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

        glyph = phiface.glyphs[a](x=xloc, y=yloc)
        glyph.w = (weight * (glyph.capHeight() / 100.0))

        glyphBounds = phiface.mergeSubPolys([glyph]).bounds
        xShift = glyphBounds[2] - glyphBounds[0]

        if b is not " ":
            xShift += (phiface.kernGlyphs(a, b, weight) *
                (glyph.capHeight() / 100.0))

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