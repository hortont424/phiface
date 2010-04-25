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
#demoStr = "New <i>York</i> City"
#demoStr = ".|      |."
#demoStr = "./"

demoStr = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec tincidunt luctus mi in tempus. Nullam lacus erat, mollis porta eleifend eu, bibendum id leo. Vivamus pulvinar, enim ultricies congue laoreet, nisi leo lobortis urna, nec convallis metus eros in nulla. Vestibulum arcu mi, condimentum et laoreet eu, euismod nec nisi. Donec odio lectus, dignissim quis bibendum vitae, interdum quis nunc. Maecenas quis enim neque. Ut porttitor, ligula ac luctus molestie, dolor justo interdum nulla, nec imperdiet ante mauris nec tortor. Pellentesque porta semper congue. Sed euismod eleifend eros, et faucibus dolor malesuada ut. Pellentesque sed enim nec ligula tempus vulputate. Etiam commodo quam vitae nulla sagittis ac consequat risus consectetur. Maecenas pretium erat sed sem egestas eu adipiscing nisl bibendum. Sed consequat felis sed mauris facilisis elementum. Suspendisse mollis auctor odio eu convallis. Nulla facilisi. Nulla eleifend lectus quis leo tempor vitae blandit purus dignissim. Phasellus in ipsum id risus egestas vestibulum sed faucibus nisi."

src = "<?xml version='1.0' encoding='UTF-8'?><document width='1200' height='600'><textbox x='30' y='30' size='12' width='1100'><l>" + demoStr + "</l><br/><br/><r>" + demoStr + "</r><br/><br/><h>" + demoStr + "</h></textbox></document>"

#src = """<?xml version='1.0' encoding='UTF-8'?>
#<document width='1200' height='600'>
#<textbox x='30' y='30' size='50'>
#<color r='.969' g='0.0' b='.122' a='1.0'>
#<r><i>Never</i> gonna give you up!</r>
#</color>
#</textbox>
#</document>"""

document = ET.XML(src.encode('utf8'))

sc = phiface.Context(int(document.attrib["width"]),
                     int(document.attrib["height"]))

for box in document:
    tb = phiface.TextBox(box)
    sc.draw(tb.layoutGlyphs())

#

sc.write()
