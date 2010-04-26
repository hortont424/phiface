# -*- coding: utf-8 -*-

import line
import circle
from line import Line
from circle import Circle
from context import mergeSubPolys
from shapely.geometry import *

from math import *

PHI = 1.618

glyphs = {}

def glyph(g):
    def wrap(cls):
        glyphs[g] = cls
        cls.char = g
        return cls
    return wrap

class Glyph(object):
    def __init__(self, x, y, capHeight=50):
        super(Glyph, self).__init__()
        self.x = x
        self.y = y
        self.w = 3
        self.pointSize = capHeight
        self.slanted = False
        self.outlined = False
        self.color = (0.0, 0.0, 0.0, 1.0)
        self.serifed = True
        self.willBeSerifed = True
        self.autoKern = True

    def capHeight(self):
        return self.pointSize

    def em(self):
        return self.capHeight() / PHI

    def width(self):
        pass

    def weight(self):
        return self.w

    def xHeight(self):
        return self.capHeight() / PHI

    def origin(self):
        return (self.x, self.y + self.capHeight())

    def p(self, ix, iy, xHeight=False):
        (x, y) = self.origin()
        height = self.capHeight()

        if xHeight:
            height = self.xHeight()
        return (x + (self.width() * ix), y - (height * iy))

    def setupDrawing(self):
        circle.capHeight = line.capHeight = self.capHeight()
        circle.drawSerifs = line.drawSerifs = self.serifed
