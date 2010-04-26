#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import phiface
from xml.etree import ElementTree as ET

#demoStr = "".join([a for a in sorted(phiface.glyphs.keys())])

# make space a special character using pipe kerning + 1 em or something?

def render(filename):
    phiface.loadKerningData()

    outputFilename = os.path.splitext(filename)[0] + ".pdf"

    file = open(filename, "r")
    tree = ET.parse(file)
    document = tree.getroot()

    sc = phiface.Context(int(document.attrib["width"]),
                         int(document.attrib["height"]),
                         outputFilename)

    for box in document:
        tb = phiface.TextBox(box, document)
        sc.draw(tb.layoutGlyphs())

    phiface.saveKerningData()

    return outputFilename

if len(sys.argv) == 2:
    os.system("open {0}".format(render(sys.argv[1])))
else:
    print "Usage: {0} filename.xml".format(sys.argv[0])