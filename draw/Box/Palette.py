import pyglet
from pyglet.gl import GL_QUADS

from draw.Box.BoxDraw import BoxDraw


class Palette(BoxDraw):

    def __init__(self):
        self.top = self.get_tex('#000000', 'resources/textures/wood.jpeg')
        self.side = self.get_tex('#000000', 'resources/textures/wood.jpeg')
        self.bottom = self.get_tex('#000000', 'resources/textures/wood.jpeg')

        self.batch = pyglet.graphics.Batch()

        tex_coords = ('t2f', (0, 0, 1, 0, 1, 1, 0, 1,))

        x, y, z = 0, 0, 0
        X, Y, Z = x + 120, y - 2, z + 80

        self.batch.add(4, GL_QUADS, self.side, ('v3f', (x, y, z, x, y, Z, x, Y, Z, x, Y, z,)), tex_coords)
        self.batch.add(4, GL_QUADS, self.side, ('v3f', (X, y, Z, X, y, z, X, Y, z, X, Y, Z,)), tex_coords)
        self.batch.add(4, GL_QUADS, self.bottom, ('v3f', (x, y, z, X, y, z, X, y, Z, x, y, Z,)), tex_coords)
        self.batch.add(4, GL_QUADS, self.top, ('v3f', (x, Y, Z, X, Y, Z, X, Y, z, x, Y, z,)), tex_coords)
        self.batch.add(4, GL_QUADS, self.side, ('v3f', (X, y, z, x, y, z, x, Y, z, X, Y, z,)), tex_coords)
        self.batch.add(4, GL_QUADS, self.side, ('v3f', (x, y, Z, X, y, Z, X, Y, Z, x, Y, Z,)), tex_coords)
