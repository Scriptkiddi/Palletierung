import pyglet
from pyglet.gl import glTexParameterf, GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST, GL_TEXTURE_MAG_FILTER


class BoxDraw:
    def get_tex(self, file):
        tex = pyglet.image.load(file).get_texture()
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        return pyglet.graphics.TextureGroup(tex)

    def draw(self):
        self.batch.draw()
