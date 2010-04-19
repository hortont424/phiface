#!/usr/bin/env python

import phiface

sc = phiface.Context()

yloc = 30

for weight in [1, 3, 5, 7]:
    xloc = 30
    A = phiface.AGlyph(x=xloc, y=yloc)

    xloc += A.width() + 40
    E = phiface.EGlyph(x=xloc, y=yloc)

    xloc += E.width() + 20
    I = phiface.IGlyph(x=xloc, y=yloc)

    xloc += I.width() + 20
    T = phiface.TGlyph(x=xloc, y=yloc)

    xloc += T.width() + 20
    V = phiface.VGlyph(x=xloc, y=yloc)

    A.w = E.w = I.w = T.w = V.w = (weight * (A.capHeight() / 150.0))

    sc.draw([A, E, I, T, V])

    yloc += A.capHeight() + 20

sc.write("output.png")