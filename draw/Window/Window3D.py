import pyglet
from pyglet.gl import glPopMatrix
from pyglet.window import key

from draw.Box.Box3DDraw import Box3DDraw
from draw.Box.BoxDraw import BoxDraw
from draw.Box.Palette import Palette
from draw.Box.Spectator import Spectator
from draw.Window.Window import Window


class Window3D(Window):
    def __init__(self, boxes, x_width, y_width, z_width, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(300, 200)
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        pyglet.clock.schedule(self.update)
        self.palette = Palette()
        self.boxes = []
        self.spectator = Spectator((60, 100, 120), (-35, 0))
        self.box_pointer = 0
        for box in boxes:
            self.boxes.append(Box3DDraw(box))

    def on_mouse_motion(self, x, y, dx, dy):
        if self.mouse_lock:
            self.spectator.mouse_motion(dx, dy)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.mouse_lock: self.spectator.mouse_motion(dx, dy)

    def on_key_press(self, KEY, MOD):
        if KEY == key.ESCAPE:
            self.close()
        elif KEY == key.E:
            self.mouse_lock = not self.mouse_lock
        elif KEY == key.UP:
            if self.box_pointer < len(self.boxes)-1:
                print(self.boxes[self.box_pointer].box)
                print(self.boxes[self.box_pointer].box.box_type.identifier)
                self.box_pointer += 1
        elif KEY == key.DOWN:
            if self.box_pointer > 0:
                self.box_pointer -= 1

    def on_draw(self):
        self.clear()
        self.set3d()
        self.push(self.spectator.pos, self.spectator.rot)
        for i in range(0, self.box_pointer):
            self.boxes[i].draw()
        self.palette.draw()
        glPopMatrix()
