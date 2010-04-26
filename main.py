#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cProfile
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
#demoStr = "New <i>York</i> City"
#demoStr = ".|      |."
#demoStr = "./"

demoStr = "Once I got back to RPI (in late January), I asked Carol (and Nate) if I could steal her for a day at the end of March. She managed to get a day off from work, and we got tickets to the concert and various forms of transportation. Getting concert tickets was a bit of a pain; the internet has made it very easy for scalpers to immediately consume the entire supply of tickets, especially to very small shows like this; but we eventually got it all sorted out.<br/><br/>As March drew to a close, it became clear that the 29th was going to be a disgustingly rainy day, both in NYC and Troy. Oh, well, we said as we boarded a Megabus nearby the local Amtrak station; we were determined to make something awesome of the day, regardless of the weather."

src = "<?xml version='1.0' encoding='UTF-8'?><document width='1200' height='600'><textbox x='30' y='30' size='12' width='1100'><l>" + demoStr + "</l><br/><br/><r>" + demoStr + "</r><br/><br/><h>" + demoStr + "</h></textbox></document>"

#src = """<?xml version='1.0' encoding='UTF-8'?>
#<document width='1200' height='600'>
#<textbox x='30' y='30' size='50'>
#<color r='.969' g='0.0' b='.122' a='1.0'>
#<r><i>Never</i> gonna give you up!</r>
#</color>
#</textbox>
#</document>"""

def main():
    phiface.loadKerningData()
    document = ET.XML(src.encode('utf8'))

    sc = phiface.Context(int(document.attrib["width"]),
                         int(document.attrib["height"]))

    for box in document:
        tb = phiface.TextBox(box)
        sc.draw(tb.layoutGlyphs())

    sc.write()
    phiface.saveKerningData()

#cProfile.run('main()')
main()
