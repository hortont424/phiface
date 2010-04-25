#!/usr/bin/env python
# -*- coding: utf-8 -*-

import phiface
from xml.etree import ElementTree as ET

#demoStr = [a for a in sorted(phiface.glyphs.keys())]

#demoStr = "HALF WENT VIM AT HIT AVE AWW LET LIE LEM LIVE"
#demoStr = "abdlojk"
#demoStr = "AEFHIKLMNOTVWXYZ"
#demoStr = "lotvwdxzb dot blow wow lot voltz"# AEFHIKLMNTVWXYZ
#demoStr = "Dolor"
#demoStr = "http://www.hortont.com/phiface"
#demoStr = "a; bcd. ef, ij!"
#demoStr = "New York City"
#demoStr = "defghi"

src = """
<document width='1200' height='600'>
    <textbox x='30' y='30'><t>New</t> <i>Y<b>or</b>k</i> <b>Ci<b>ty</b></b></textbox>
    <textbox x='30' y='180'>Woohoo!</textbox>
</document>"""

document = ET.XML(src)

sc = phiface.Context(int(document.attrib["width"]),
                     int(document.attrib["height"]))

for box in document:
    tb = phiface.TextBox(box)
    sc.draw(tb.layoutGlyphs())

#

sc.write()
