#!/usr/bin/env python

import phiface

sc = phiface.Context()


line = phiface.Line((10.0, 100.0), (30.9023485785, 100.0), 2)
lineTwo = phiface.Line((30.9023485785, 100.0), (71.804697157, 200.0), 2)
lineThree = phiface.Line((20, 200), (150, 100), 2)

a = phiface.AGlyph()

sc.draw([a])
sc.write("output.png")