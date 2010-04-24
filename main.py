#!/usr/bin/env python
# -*- coding: utf-8 -*-

import phiface

sc = phiface.Context()

demoStr = [a for a in sorted(phiface.glyphs.keys())]

#demoStr = "HALF WENT VIM AT HIT AVE AWW LET LIE LEM LIVE"
#demoStr = "abdlojk"
#demoStr = "AEFHIKLMNOTVWXYZ"
#demoStr = "lotvwdxzb dot blow wow lot voltz"# AEFHIKLMNTVWXYZ
#demoStr = "Dolor"
#demoStr = "http://www.hortont.com/phiface"
#demoStr = "a; bcd. ef, ij!"
demoStr = "New York"
#demoStr = "Phiface"
#demoStr = "defghi"
tracking = 0
capHeight = 100
phiface.line.drawSerifs = phiface.circle.drawSerifs = True

xloc = yloc = 20
metrics = phiface.Glyph(0, 0, capHeight=capHeight)

for weight in [0.5, 2, 4, 7]:
    for i in range(len(demoStr)):
        a = demoStr[i]
        print a

        if a == " ":
            xloc += metrics.em() + tracking
            continue

        if i + 1 < len(demoStr):
            b = demoStr[i + 1]
        else:
            b = None

        glyph = phiface.glyphs[a](x=0, y=0, capHeight=capHeight)
        glyph.w = (weight * (capHeight / 100.0))

        if weight == 2:
            glyph.slanted = True

        if weight == 4:
            glyph.outlined = True

        glyphBounds = phiface.mergeSubPolys([glyph]).bounds
        glyph.x = xloc
        glyph.y = yloc
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
