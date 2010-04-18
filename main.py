#!/usr/bin/env python

import phiface

sc = phiface.Context()

line = phiface.Line((20, 20), (300, 300), 2)
lineTwo = phiface.Line((20, 20), (200, 300), 2)
lineThree = phiface.Line((20, 200), (150, 100), 2)
sc.draw([line, lineTwo, lineThree])
sc.write("output.png")