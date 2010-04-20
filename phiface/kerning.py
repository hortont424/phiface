from glyph import *
from context import *
from shapely.geometry import *

defaultKerning = 10
kerningOverrides = {
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

metrics = Glyph(0,0)

kerningPairs = {}

def autoKern(a, b, weight):
    if not (a in glyphs and b in glyphs):
        return metrics.em() / 1.618

    aGlyph = glyphs[a](x=0, y=0)
    aBounds = mergeSubPolys([aGlyph]).bounds

    for i in range(2, -30, -1):
        advance = (aBounds[2] - aBounds[0]) + i
        bGlyph = glyphs[b](x=advance, y=0)
        if type(mergeSubPolys([aGlyph, bGlyph])) is Polygon:
            return i
    print "BAD THING"

def kernGlyphs(a, b, weight):
    if (a in kerningPairs) and (b in kerningPairs[a]):
        return kerningPairs[a][b]

    kerning = autoKern(a, b, weight) + defaultKerning

    if b and (a in kerningOverrides) and (b in kerningOverrides[a]):
        kerning = kerningOverrides[a][b]

    if not (a in kerningPairs):
        kerningPairs[a] = {}

    if not (b in kerningPairs[a]):
        kerningPairs[a][b] = kerning

    return kerning