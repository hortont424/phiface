#!/usr/bin/env python

import phiface

sc = phiface.Context()

a = phiface.AGlyph(x=30, y=30)
e = phiface.EGlyph(x=120, y=30)

sc.draw([a, e])
sc.write("output.png")