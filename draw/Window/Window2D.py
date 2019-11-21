import pyglet
from pyglet.gl import glPopMatrix
from pyglet.window import key

from draw.Box.Box2DDraw import Box2DDraw
from draw.Box.Spectator import Spectator
from draw.Window.Window import Window


class Window2D(Window):
    def __init__(self, boxes, x_width, y_width, z_width, x, y, z, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # the main class defined z has height and not y
        self.dim_X = x
        self.dim_Y = z
        self.dim_Z = y
        assert self.dim_X and self.dim_Y and not self.dim_Z or \
               self.dim_X and not self.dim_Y and self.dim_Z or \
               not self.dim_X and self.dim_Y and self.dim_Z
        self.set_minimum_size(300, 200)
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        pyglet.clock.schedule(self.update)
        self.boxes = []
        if self.dim_X and self.dim_Y:
            self.spectator = Spectator((int(x_width / 10), int(y_width/10), 100), (0, 0))
        elif self.dim_X and self.dim_Z:
            self.spectator = Spectator((int(x_width / 10), int(z_width/10), 100), (0, 0))
        elif self.dim_Y and self.dim_Z:
            self.spectator = Spectator((int(y_width / 10), int(z_width / 10), 100), (0, 0))
        self.box_pointer = 0
        for box in boxes:
            self.boxes.append(Box2DDraw(box, self.dim_X, self.dim_Y, self.dim_Z))

    def on_key_press(self, KEY, MOD):
        if KEY == key.ESCAPE:
            self.close()
        elif KEY == key.UP:
            if self.box_pointer < len(self.boxes)-1:
                self.box_pointer += 1
                print(self.boxes[self.box_pointer].box)
        elif KEY == key.DOWN:
            if self.box_pointer > 0:
                self.box_pointer -= 1

    def on_draw(self):
        self.clear()
        self.set3d()
        self.push(self.spectator.pos, self.spectator.rot)
        for i in range(0, self.box_pointer):
            self.boxes[i].draw()
        glPopMatrix()
