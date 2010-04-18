#!/usr/bin/env python

import phiface

sc = phiface.ShapelyCairo()

line = phiface.Line((10, 10), (100, 200), 3)
lineTwo = phiface.Line((30, 30), (100, 100), 5)
sc.draw([line, lineTwo])
sc.write("output.png")