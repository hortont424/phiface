#!/usr/bin/env python
# -*- coding: utf-8 -*-

import phiface
from xml.etree import ElementTree as ET

demoStr = "".join([a for a in sorted(phiface.glyphs.keys())])

#demoStr = "HALF WENT VIM AT HIT AVE AWW LET LIE LEM LIVE"
#demoStr = "abdlojk"
#demoStr = "AEFHIKLMNOTVWXYZ"
#demoStr = "lotvwdxzb dot blow wow lot voltz"# AEFHIKLMNTVWXYZ
#demoStr = "Dolor"
#demoStr = "http://www.hortont.com/phiface"
#demoStr = "a; bcd. ef, ij!"
#demoStr = "New York City"
demoStr = "QRSTUVqrstuv"

src = "<?xml version='1.0' encoding='UTF-8'?><document width='1200' height='600'><textbox x='30' y='30' size='40'><l>" + demoStr + "</l><br/><br/><r>" + demoStr + "</r><br/><br/><b>" + demoStr + "</b></textbox></document>"

document = ET.XML(src.encode('utf8'))

sc = phiface.Context(int(document.attrib["width"]),
                     int(document.attrib["height"]))

for box in document:
    tb = phiface.TextBox(box)
    sc.draw(tb.layoutGlyphs())

#

sc.write()
