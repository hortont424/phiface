from cairo import *

class ShapelyCairo(object):
    def __init__(self):
        super(ShapelyCairo, self).__init__()

        self.surface = ImageSurface(FORMAT_ARGB32, 800, 800)
        self.ctx = Context(self.surface)

    def drawPolygon(self, poly):
        coords = poly.exterior.coords
        self.ctx.move_to(*coords[0])

        for (x, y) in coords:
            self.ctx.line_to(x, y)

        self.ctx.close_path()

    def write(self, filename):
        self.surface.write_to_png(filename)