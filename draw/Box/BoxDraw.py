import pyglet
from pyglet.gl import glTexParameterf, GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST, GL_TEXTURE_MAG_FILTER
from pyglet.image import SolidColorImagePattern


class BoxDraw:

    def hex_to_rgb(self, hex):
        hex = hex.lstrip('#')
        hlen = len(hex)
        return tuple(int(hex[i:i + hlen // 3], 16) for i in range(0, hlen, hlen // 3))

    def get_tex(self, color, file=None):
        if file:
            tex = pyglet.image.load(file).get_texture()
        else:
            rgb_color = self.hex_to_rgb(color)
            color = SolidColorImagePattern(color=(rgb_color[0], rgb_color[1], rgb_color[2], 0))
            tex = color.create_image(8, 8).get_texture()
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        return pyglet.graphics.TextureGroup(tex)

    def draw(self):
        self.batch.draw()
        self.lines.draw()
