from math import *
from glyph import *
from context import *
from shapely.geometry import *

defaultKerning = 10
kerningOverrides = {

}

metrics = Glyph(0,0)

kerningPairs = {}

def autoKern(a, b, weight, capHeight):
    if not (a in glyphs and b in glyphs):
        return metrics.em() / 1.618

    aGlyph = glyphs[a](x=0, y=0, capHeight=capHeight)
    aGlyph.w = (weight * (metrics.capHeight() / 100.0))
    aBounds = mergeSubPolys([aGlyph]).bounds
    maxRange = 15

    for i in range(maxRange, -1000, -1):
        advance = (aBounds[2] - aBounds[0]) + i
        bGlyph = glyphs[b](x=advance, y=0, capHeight=capHeight)
        bGlyph.w = (weight * (metrics.capHeight() / 100.0))
        bBounds = mergeSubPolys([bGlyph]).bounds
        if type(mergeSubPolys([aGlyph, bGlyph])) is Polygon:
            if i == maxRange:
                print "Autokern max range failure for glyphs:", a, b
                return 0
            return i
    print "Autokern failed for glyphs:", a, b
    return 0

#TODO: CACHE IS BROKEN WHEN CAPHEIGHT CHANGES!

def kernGlyphs(a, b, weight, capHeight):
    #if (a in kerningPairs) and (b in kerningPairs[a]):
    #    return kerningPairs[a][b]

    kerning = autoKern(a, b, weight, capHeight)

    if (a in kerningOverrides) and ("default" in kerningOverrides[a]):
        kerning += kerningOverrides[a]["default"] * (metrics.capHeight() / 100.0)
    else:
        kerning += defaultKerning * (metrics.capHeight() / 100.0)

    #if b and (a in kerningOverrides) and (b in kerningOverrides[a]):
    #    kerning = kerningOverrides[a][b] * (metrics.capHeight() / 100.0)

    #if not (a in kerningPairs):
    #    kerningPairs[a] = {}
    #
    #if not (b in kerningPairs[a]):
    #    kerningPairs[a][b] = kerning

    return kerning