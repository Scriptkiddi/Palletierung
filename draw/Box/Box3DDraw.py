import pyglet
from pyglet.gl import GL_QUADS

from draw.Box.BoxDraw import BoxDraw


class Box3DDraw(BoxDraw):
    def __init__(self, box):
        self.box = box
        self.top = self.get_tex('resources/textures/grass_top.png')
        self.side = self.get_tex('resources/textures/side.png')
        self.bottom = self.get_tex('resources/textures/dirt.png')

        self.batch = pyglet.graphics.Batch()

        tex_coords = ('t2f', (0, 0, 1, 0, 1, 1, 0, 1,))

        print(box.llc())
        x, y, z = box.llc()[0] / 10, box.llc()[2] / 10, box.llc()[1] / 10
        X, Y, Z = box.urc()[0] / 10, box.urc()[2] / 10, box.urc()[1] / 10

        self.batch.add(4, GL_QUADS, self.side, ('v3f', (x, y, z, x, y, Z, x, Y, Z, x, Y, z,)), tex_coords)
        self.batch.add(4, GL_QUADS, self.side, ('v3f', (X, y, Z, X, y, z, X, Y, z, X, Y, Z,)), tex_coords)
        self.batch.add(4, GL_QUADS, self.bottom, ('v3f', (x, y, z, X, y, z, X, y, Z, x, y, Z,)), tex_coords)
        self.batch.add(4, GL_QUADS, self.top, ('v3f', (x, Y, Z, X, Y, Z, X, Y, z, x, Y, z,)), tex_coords)
        self.batch.add(4, GL_QUADS, self.side, ('v3f', (X, y, z, x, y, z, x, Y, z, X, Y, z,)), tex_coords)
        self.batch.add(4, GL_QUADS, self.side, ('v3f', (x, y, Z, X, y, Z, X, Y, Z, x, Y, Z,)), tex_coords)
