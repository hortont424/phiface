#!/usr/bin/env python

import phiface

sc = phiface.Context()

demoStr = [a for a in sorted(phiface.glyphs.keys())]

#demoStr = "HALF WENT VIM AT HIT AVE AWW LET LIE LEM LIVE"
#demoStr = "abdlokKpqi"
#demoStr = "AEFHIKLMNOTVWXYZ"
#demoStr = "lotvwdxzb dot blow wow lot voltz"# AEFHIKLMNTVWXYZ
#demoStr = "TextMate Mail"
demoStr = "14M"
tracking = 0
capHeight = 50

xloc = yloc = 20
metrics = phiface.Glyph(0,0,capHeight=capHeight)
for weight in [2, 4, 7]:
    for i in range(len(demoStr)):
        a = demoStr[i]

        if a == " ":
            xloc += metrics.em() + tracking
            continue

        if i + 1 < len(demoStr):
            b = demoStr[i + 1]
        else:
            b = None

        glyph = phiface.glyphs[a](x=xloc, y=yloc, capHeight=capHeight)
        glyph.w = (weight * (glyph.capHeight() / 100.0))

        glyphBounds = phiface.mergeSubPolys([glyph]).bounds
        xShift = glyphBounds[2] - glyphBounds[0]

        if b is not " ":
            xShift += (phiface.kernGlyphs(a, b, weight, capHeight=capHeight) +
                       tracking)

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