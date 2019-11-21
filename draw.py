import math

from pyglet.gl import *
from pyglet.window import key
from time import sleep


class Palette:
    def get_tex(self, file):
        tex = pyglet.image.load(file).get_texture()
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        return pyglet.graphics.TextureGroup(tex)

    def __init__(self):
        self.top = self.get_tex('resources/textures/wood.jpeg')
        self.side = self.get_tex('resources/textures/wood.jpeg')
        self.bottom = self.get_tex('resources/textures/wood.jpeg')

        self.batch = pyglet.graphics.Batch()

        tex_coords = ('t2f', (0, 0, 1, 0, 1, 1, 0, 1,))

        x, y, z = 0, 0, -1
        X, Y, Z = x + 120, y - 2, z + 80

        self.batch.add(4, GL_QUADS, self.side, ('v3f', (x, y, z, x, y, Z, x, Y, Z, x, Y, z,)), tex_coords)
        self.batch.add(4, GL_QUADS, self.side, ('v3f', (X, y, Z, X, y, z, X, Y, z, X, Y, Z,)), tex_coords)
        self.batch.add(4, GL_QUADS, self.bottom, ('v3f', (x, y, z, X, y, z, X, y, Z, x, y, Z,)), tex_coords)
        self.batch.add(4, GL_QUADS, self.top, ('v3f', (x, Y, Z, X, Y, Z, X, Y, z, x, Y, z,)), tex_coords)
        self.batch.add(4, GL_QUADS, self.side, ('v3f', (X, y, z, x, y, z, x, Y, z, X, Y, z,)), tex_coords)
        self.batch.add(4, GL_QUADS, self.side, ('v3f', (x, y, Z, X, y, Z, X, Y, Z, x, Y, Z,)), tex_coords)

    def draw(self):
        self.batch.draw()


class Box:

    def get_tex(self, file):
        tex = pyglet.image.load(file).get_texture()
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        return pyglet.graphics.TextureGroup(tex)

    def __init__(self, box):
        self.top = self.get_tex('test/grass_top.png')
        self.side = self.get_tex('resources/textures/side.png')
        self.bottom = self.get_tex('test/dirt.png')

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

    def draw(self):
        self.batch.draw()


class Player:
    def __init__(self, pos=(0, 0, 0), rot=(0, 0)):
        self.pos = list(pos)
        self.rot = list(rot)

    def mouse_motion(self, dx, dy):
        dx /= 8;
        dy /= 8;
        self.rot[0] += dy;
        self.rot[1] -= dx
        if self.rot[0] > 90:
            self.rot[0] = 90
        elif self.rot[0] < -90:
            self.rot[0] = -90

    def update(self, dt, keys):
        s = dt * 100
        rotY = -self.rot[1] / 180 * math.pi
        dx, dz = s * math.sin(rotY), s * math.cos(rotY)
        if keys[key.W]: self.pos[0] += dx; self.pos[2] -= dz
        if keys[key.S]: self.pos[0] -= dx; self.pos[2] += dz
        if keys[key.A]: self.pos[0] -= dz; self.pos[2] -= dx
        if keys[key.D]: self.pos[0] += dz; self.pos[2] += dx

        if keys[key.SPACE]: self.pos[1] += s
        if keys[key.LSHIFT]: self.pos[1] -= s


class Window(pyglet.window.Window):

    def addBox(self, box):
        self.boxes.append(Box(box))
        self.on_draw()

    def push(self, pos, rot):
        glPushMatrix();
        glRotatef(-rot[0], 1, 0, 0)
        glRotatef(-rot[1], 0, 1, 0)
        glTranslatef(-pos[0], -pos[1],
                     -pos[2], )

    def Projection(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

    def Model(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def set2d(self):
        self.Projection()
        gluOrtho2D(0, self.width, 0, self.height)
        self.Model()

    def set3d(self):
        self.Projection()
        gluPerspective(70, self.width / self.height, 0.05, 1000);
        self.Model()

    def setLock(self, state):
        self.lock = state
        self.set_exclusive_mouse(state)

    lock = False;
    mouse_lock = property(lambda self: self.lock, setLock)

    def __init__(self, boxes, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(300, 200)
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        pyglet.clock.schedule(self.update)
        self.palette = Palette()
        self.boxes = []
        self.spectator = Player((60, 100, 120), (-35, 0))
        self.box_pointer = 0
        for box in boxes:
            self.boxes.append(Box(box))

    def on_mouse_motion(self, x, y, dx, dy):
        if self.mouse_lock: self.spectator.mouse_motion(dx, dy)

    def on_key_press(self, KEY, MOD):
        if KEY == key.ESCAPE:
            self.close()
        elif KEY == key.E:
            self.mouse_lock = not self.mouse_lock
        elif KEY == key.UP:
            if self.box_pointer < len(self.boxes):
                self.box_pointer += 1
        elif KEY == key.DOWN:
            if self.box_pointer > 0:
                self.box_pointer -= 1

    def update(self, dt):
        self.spectator.update(dt, self.keys)

    def on_draw(self):
        self.clear()
        self.set3d()
        self.push(self.spectator.pos, self.spectator.rot)
        for i in range(0, self.box_pointer):
            self.boxes[i].draw()
        self.palette.draw()
        glPopMatrix()
