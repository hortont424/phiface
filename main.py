#!/usr/bin/env python

import phiface

sc = phiface.Context()

A = phiface.AGlyph(x=30, y=30)
E = phiface.EGlyph(x=30 + A.width() + 40, y=30)
I = phiface.IGlyph(x=30 + A.width() + 40 + E.width() + 20, y=30)

sc.draw([A, E, I])

A = phiface.AGlyph(x=30, y=215)
E = phiface.EGlyph(x=30 + A.width() + 40, y=215)
I = phiface.IGlyph(x=30 + A.width() + 40 + E.width() + 20, y=215)
A.w = E.w = I.w = 10

sc.draw([A, E, I])

A = phiface.AGlyph(x=30, y=400)
E = phiface.EGlyph(x=30 + A.width() + 40, y=400)
I = phiface.IGlyph(x=30 + A.width() + 40 + E.width() + 20, y=400)
A.w = E.w = I.w = 1

sc.draw([A, E, I])

sc.write("output.png")