import cairo
from shapely.geometry import *

class Context(object):
    def __init__(self):
        super(Context, self).__init__()

        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 800, 800)
        self.ctx = cairo.Context(self.surface)

        self.ctx.set_source_rgba(1.0, 1.0, 1.0, 1.0)
        self.ctx.rectangle(0, 0, 800, 800)
        self.ctx.fill()

    def _drawCoords(self, coords):
        self.ctx.move_to(*coords[0])

        for (x, y) in coords:
            self.ctx.line_to(x, y)

        self.ctx.close_path()

    def _drawPolygon(self, poly):
        self._drawCoords(poly.exterior.coords)

        for hole in poly.interiors:
            self._drawCoords(hole.coords)

        self.ctx.set_source_rgba(0.0, 0.0, 0.0, 1.0)
        self.ctx.fill()

    def draw(self, polys):
        poly = reduce(lambda x, y: x.union(y), [p.getPolygon() for p in polys])

        if type(poly) is MultiPolygon:
            for subPoly in poly.geoms:
                self._drawPolygon(subPoly)
        else:
            self._drawPolygon(poly)

    def write(self, filename):
        self.surface.write_to_png(filename)