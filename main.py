#!/usr/bin/env python
# -*- coding: utf-8 -*-

import phiface

sc = phiface.Context()

demoStr = [a for a in sorted(phiface.glyphs.keys())]

#demoStr = "HALF WENT VIM AT HIT AVE AWW LET LIE LEM LIVE"
#demoStr = "abdlojk"
#demoStr = "AEFHIKLMNOTVWXYZ"
#demoStr = "lotvwdxzb dot blow wow lot voltz"# AEFHIKLMNTVWXYZ
#demoStr = "Dolor"
#demoStr = "http://www.hortont.com/phiface"
#demoStr = "a; bcd. ef, ij!"
demoStr = "New York City"
#demoStr = "defghi"

sc.draw(phiface.text.layoutText("New York City"))

sc.write()
