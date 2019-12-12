import pyglet
import hashlib
from pyglet.gl import GL_QUADS

from draw.Box.BoxDraw import BoxDraw

side_textures = [
    'resources/textures/side.png',
    'resources/textures/crate.jpg',
    'resources/textures/supermarket1.jpg',
    'resources/textures/wine1.jpg',
    'resources/textures/wine2.png',
    'resources/textures/wine3.jpeg',
    'resources/textures/wood.jpeg',
]

top_textures = [
    'resources/textures/pappe1.jpg',
    'resources/textures/pappe2.png',
    'resources/textures/karton.png',
]

colors = [
    '#95bc22',
    '#43ac52',
    '#009671',
    '#007d7e',
    '#006274',
    '#2f4858',
    '#747f4b',
    '#edf5ce',
    '#005253',
    '#bffcfb',
    '#00cde9',
    '#68edcb',
    '#f29367',
    '#b65f36'
]


class Box3DDraw(BoxDraw):
    def __init__(self, box):
        self.box = box
        color_id = int(hashlib.sha256(box.get_type().identifier.encode('utf-8')).hexdigest(), 16) % 10 * 1
        color = colors[color_id % len(colors)]
        #top_texture = top_textures[color_id % len(top_textures)]
        #side_texture = side_textures[color_id % len(side_textures)]

        self.top = self.get_tex(color)
        self.side = self.get_tex(color)
        self.bottom = self.get_tex(color)

        self.batch = pyglet.graphics.Batch()

        tex_coords = ('t2f', (0, 0, 1, 0, 1, 1, 0, 1,))

        x, y, z = box.llc()[0] / 10, box.llc()[2] / 10, box.llc()[1] / 10
        X, Y, Z = box.urc()[0] / 10, box.urc()[2] / 10, box.urc()[1] / 10

        self.batch.add(4, GL_QUADS, self.side, ('v3f', (x, y, z, x, y, Z, x, Y, Z, x, Y, z,)), tex_coords)
        self.batch.add(4, GL_QUADS, self.side, ('v3f', (X, y, Z, X, y, z, X, Y, z, X, Y, Z,)), tex_coords)
        self.batch.add(4, GL_QUADS, self.bottom, ('v3f', (x, y, z, X, y, z, X, y, Z, x, y, Z,)), tex_coords)
        self.batch.add(4, GL_QUADS, self.top, ('v3f', (x, Y, Z, X, Y, Z, X, Y, z, x, Y, z,)), tex_coords)
        self.batch.add(4, GL_QUADS, self.side, ('v3f', (X, y, z, x, y, z, x, Y, z, X, Y, z,)), tex_coords)
        self.batch.add(4, GL_QUADS, self.side, ('v3f', (x, y, Z, X, y, Z, X, Y, Z, x, Y, Z,)), tex_coords)
