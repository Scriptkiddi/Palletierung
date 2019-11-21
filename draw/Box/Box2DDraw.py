import pyglet
from pyglet.gl import GL_LINES

from draw.Box.BoxDraw import BoxDraw


class Box2DDraw(BoxDraw):
    def __init__(self, box, dim_X, dim_Y, dim_Z):
        self.box = box

        self.batch = pyglet.graphics.Batch()

        tex_coords = ('t2f', (0, 0, 1, 0, 1, 1, 0, 1,))
        if dim_X and dim_Y:
            x, y = box.llc()[0] / 10, box.llc()[2] / 10
            X, Y = box.urc()[0] / 10, box.urc()[2] / 10
        if dim_X and dim_Z:
            x, y = box.llc()[0] / 10, box.llc()[1] / 10
            X, Y = box.urc()[0] / 10, box.urc()[1] / 10
        if dim_Y and dim_Z:
            x, y = box.llc()[2] / 10, box.llc()[1] / 10
            X, Y = box.urc()[2] / 10, box.urc()[1] / 10

        self.batch.add(2, GL_LINES, None, ('v2f', (x, y, X, y)))
        self.batch.add(2, GL_LINES, None, ('v2f', (X, y, X, Y)))
        self.batch.add(2, GL_LINES, None, ('v2f', (X, Y, x, Y)))
        self.batch.add(2, GL_LINES, None, ('v2f', (x, Y, x, y)))
