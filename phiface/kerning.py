from math import *
from glyph import *
from context import *
from shapely.geometry import *

defaultKerning = 10
kerningOverrides = {
    "b": {
        "d": -5,
        "q": -5
    },
    "p": {
        "d": -5,
        "q": -5
    }
}

kerningPairs = {}

def autoKern(a, b, weight, capHeight, metrics):
    if not (a in glyphs and b in glyphs):
        return metrics.em() / 1.618

    aGlyph = glyphs[a](x=0, y=0, capHeight=capHeight)
    aGlyph.w = (weight * (metrics.capHeight() / 100.0))
    aBounds = mergeSubPolys([aGlyph]).bounds
    i = direction = 0
    wantType = MultiPolygon

    bGlyph = glyphs[b](x=(aBounds[2] - aBounds[0]), y=0, capHeight=capHeight)
    bGlyph.w = (weight * (metrics.capHeight() / 100.0))

    if mergeSubPolys([aGlyph]).intersects(mergeSubPolys([bGlyph])):
        direction = min(capHeight / 50.0, 1.0)
        wantType = False
    else:
        direction = -min(capHeight / 50.0, 1.0)
        wantType = True

    minRange = 1000 * direction

    while True:
        bGlyph.x = (aBounds[2] - aBounds[0]) + i

        if (mergeSubPolys([aGlyph]).intersects(mergeSubPolys([bGlyph])) ==
            wantType):
            return i

        i += direction

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
        kerning += (kerningOverrides[a]["default"] *
            (metrics.capHeight() / 100.0))
    else:
        kerning += defaultKerning * (metrics.capHeight() / 100.0)

    if b and (a in kerningOverrides) and (b in kerningOverrides[a]):
        kerning += kerningOverrides[a][b] * (metrics.capHeight() / 100.0)

    kerningPairs[memoString] = kerning

    return kerning