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
    },
    "x": {
        "t": -5
    },
    "R": {
        "S": 10
    }
}

kerningPairs = {}

def autoKern(a, b, weight, capHeight, metrics):
    if not (a in glyphs and b in glyphs):
        return metrics.em() / 1.618

    aGlyph = glyphs[a](x=0, y=0, capHeight=capHeight)

    if not aGlyph.autoKern:
        aGlyph = glyphs["l"](x=0, y=0, capHeight=capHeight)

    aGlyph.w = (weight * (capHeight / 100.0))
    aBounds = mergeSubPolys([aGlyph]).bounds
    i = direction = 0
    wantType = MultiPolygon
    startX = aBounds[2]

    bGlyph = glyphs[b](x=startX, y=0, capHeight=capHeight)

    if not bGlyph.autoKern:
        bGlyph = glyphs["l"](x=0, y=0, capHeight=capHeight)

    bGlyph.w = (weight * (capHeight / 100.0))
    bBounds = mergeSubPolys([bGlyph]).bounds

    if mergeSubPolys([aGlyph]).intersects(mergeSubPolys([bGlyph])):
        direction = capHeight / 10.0
        wantType = False
    else:
        direction = - capHeight / 10.0
        wantType = True

    minRange = capHeight * direction

    while True:
        bGlyph.x = startX + i

        if (mergeSubPolys([aGlyph]).intersects(mergeSubPolys([bGlyph])) ==
            wantType):
            if abs(direction) < 0.1:
                return i + aBounds[0]
            else:
                minRange = -minRange * 2.0
                direction = -direction * 0.5
                wantType = not wantType

        if i == minRange:
            minRange = -minRange * 2.0
            direction = -direction * 0.5

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
