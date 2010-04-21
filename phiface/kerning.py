from math import *
from glyph import *
from context import *
from shapely.geometry import *

defaultKerning = 10
kerningOverrides = {

}

kerningPairs = {}

def autoKern(a, b, weight, capHeight, metrics):
    if not (a in glyphs and b in glyphs):
        return metrics.em() / 1.618

    aGlyph = glyphs[a](x=0, y=0, capHeight=capHeight)
    aGlyph.w = (weight * (metrics.capHeight() / 100.0))
    aBounds = mergeSubPolys([aGlyph]).bounds
    i = minRange = direction = 0
    wantType = MultiPolygon

    bGlyph = glyphs[b](x=(aBounds[2] - aBounds[0]), y=0, capHeight=capHeight)
    bGlyph.w = (weight * (metrics.capHeight() / 100.0))

    if type(mergeSubPolys([aGlyph, bGlyph])) is Polygon:
        direction = 1
        minRange = 1000
        wantType = MultiPolygon
    else:
        direction = -1
        minRange = -1000
        wantType = Polygon

    while True:
        bGlyph.x = (aBounds[2] - aBounds[0]) + i

        if type(mergeSubPolys([aGlyph, bGlyph])) is wantType:
            return i

        i += direction

#TODO: CACHE IS BROKEN WHEN CAPHEIGHT CHANGES!

def kernGlyphs(a, b, weight, capHeight):
    metrics = Glyph(0, 0, capHeight=capHeight)

    if b:
        memoString = a + "~" + b + "~" + str(weight) + "~" + str(capHeight)
    else:
        memoString = a + "~" + str(weight) + "~" + str(capHeight)

    if (memoString in kerningPairs):
        return kerningPairs[memoString]

    kerning = autoKern(a, b, weight, capHeight, metrics)

    if (a in kerningOverrides) and ("default" in kerningOverrides[a]):
        kerning += kerningOverrides[a]["default"] * (metrics.capHeight() / 100.0)
    else:
        kerning += defaultKerning * (metrics.capHeight() / 100.0)

    if b and (a in kerningOverrides) and (b in kerningOverrides[a]):
        kerning = kerningOverrides[a][b] * (metrics.capHeight() / 100.0)

    kerningPairs[memoString] = kerning

    return kerning