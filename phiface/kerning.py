from math import *
from glyph import *
from context import *
from shapely.geometry import *

import cPickle

cacheData = {"totalHits": 0, "cacheHits": 0}
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
    "t": {
        "t": -5
    },
    "f": {
        "f": -13
    },
    "4": {
        "5": 7
    }
}

def autoKern(a, b, weight, capHeight, metrics):
    if not (a in glyphs and b in glyphs):
        return metrics.em() / 1.618

    aGlyph = glyphs[a](x=0, y=0, capHeight=capHeight)

    if not aGlyph.autoKern:
        aGlyph = glyphs["l"](x=0, y=0, capHeight=capHeight)
        aGlyph.serifed = False

    aGlyph.w = weight
    aBounds = mergeSubPolys([aGlyph]).bounds
    direction = 0
    i = 0
    wantType = MultiPolygon
    startX = aBounds[2]

    bGlyph = glyphs[b](x=startX, y=0, capHeight=capHeight)

    if not bGlyph.autoKern:
        bGlyph = glyphs["l"](x=startX, y=0, capHeight=capHeight)
        bGlyph.serifed = False

    bGlyph.x = startX + i
    bGlyph.w = weight
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
            if abs(direction) < 0.01:
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
    if not hasattr(kernGlyphs, "kerningPairs"):
        kernGlyphs.kerningPairs = {}

    if b:
        memoString = a + "~" + b + "~" + str(weight) + "~" + str(capHeight)
    else:
        memoString = a + "~" + str(weight) + "~" + str(capHeight)

    metrics = Glyph(0, 0, capHeight=capHeight)

    cacheData["totalHits"] += 1

    if (memoString in kernGlyphs.kerningPairs):
        cacheData["cacheHits"] += 1
        return kernGlyphs.kerningPairs[memoString]

    kerning = autoKern(a, b, weight, capHeight, metrics)

    if (a in kerningOverrides) and ("default" in kerningOverrides[a]):
        kerning += (kerningOverrides[a]["default"] *
            (metrics.capHeight() / 100.0))
    else:
        kerning += defaultKerning * (metrics.capHeight() / 100.0)

    if b and (a in kerningOverrides) and (b in kerningOverrides[a]):
        kerning += kerningOverrides[a][b] * (metrics.capHeight() / 100.0)

    kernGlyphs.kerningPairs[memoString] = kerning

    return kerning

def saveKerningData():
    kfile = open("kerning.dat", "w")
    cPickle.dump(kernGlyphs.kerningPairs, kfile)
    kfile.close()
    print "{0}/{1} in cache.".format(cacheData["cacheHits"],
                                     cacheData["totalHits"])
    print "Saved {0} kerning entries.".format(len(kernGlyphs.kerningPairs))

def loadKerningData():
    try:
        kfile = open("kerning.dat", "r")
        kernGlyphs.kerningPairs = cPickle.load(kfile)
        kfile.close()
        print "Loaded {0} kerning entries.".format(len(kernGlyphs.kerningPairs))
    except:
        print "No kerning data to load."
        kernGlyphs.kerningPairs = {}