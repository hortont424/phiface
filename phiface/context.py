import cairo
from shapely.geometry import *

PDFOutput = True

# flatten from:
# http://rightfootin.blogspot.com/2006/09/more-on-python-flatten.html
def flatten(l, ltypes=(list, tuple)):
    ltype = type(l)
    l = list(l)
    i = 0
    while i < len(l):
        while isinstance(l[i], ltypes):
            if not l[i]:
                l.pop(i)
                i -= 1
                break
            else:
                l[i:i + 1] = l[i]
        i += 1
    return ltype(l)

class Context(object):
    def __init__(self):
        super(Context, self).__init__()

        self.width = 1200
        self.height = 800

        if PDFOutput:
            self.surface = cairo.PDFSurface("output.pdf",
                                            self.width, self.height)
        else:
            self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,
                                              self.width, self.height)

        self.ctx = cairo.Context(self.surface)

        self.ctx.set_source_rgba(1.0, 1.0, 1.0, 1.0)
        self.ctx.rectangle(0, 0, self.width, self.height)
        self.ctx.fill()

    def _drawCoords(self, coords):
        self.ctx.move_to(*coords[0])

        for (x, y) in coords:
            self.ctx.line_to(x, y)

        self.ctx.close_path()

    def _drawPolygon(self, poly, outline=False):
        self._drawCoords(poly.exterior.coords)

        for hole in poly.interiors:
            self._drawCoords(hole.coords)

        self.ctx.set_source_rgba(0.0, 0.0, 0.0, 1.0)

        if outline:
            self.ctx.stroke()
        else:
            self.ctx.fill()

        #(bx1, by1, bx2, by2) = poly.exterior.bounds
        #
        #self._drawCoords([(bx1, by1), (bx1, by2), (bx2, by2), (bx2, by1)])
        #self.ctx.set_source_rgba(1.0, 0.0, 0.0, 0.5)
        #self.ctx.set_line_width(1.0)
        #self.ctx.stroke()

    def draw(self, glyphs):
        from glyph import Glyph
        for glyph in glyphs:
            if not isinstance(glyph, Glyph):
                print "draw() should be given a list of Glyphs"

            self.ctx.identity_matrix()

            if glyph.slanted:
                self.ctx.set_matrix(cairo.Matrix(xy = -0.1, x0 = glyph.y * 0.1))

            poly = mergeSubPolys(glyphs)

            if type(poly) is MultiPolygon:
                for subPoly in poly.geoms:
                    self._drawPolygon(subPoly, outline=glyph.outlined)
            else:
                self._drawPolygon(poly, outline=glyph.outlined)

    def write(self):
        if not PDFOutput:
            self.surface.write_to_png("output.png")

def mergeSubPolys(polygons):
    def _flattenPolys(polys):
        polyList = []

        if type(polys) is Polygon or type(polys) is MultiPolygon:
            return polys

        for p in polys:
            if not p:
                continue
            if type(p) is list:
                polyList += _flattenPolys(p)
            elif type(p) is Polygon or type(p) is MultiPolygon:
                polyList.append(p)
            else:
                polyList += flatten([_flattenPolys(p.getPolygon())])
        return polyList

    return reduce(lambda x, y: x.union(y), _flattenPolys(polygons))