#!/usr/bin/env python

import phiface

sc = phiface.ShapelyCairo()

sc.drawPolygon(phiface.test())
sc.write("output.png")