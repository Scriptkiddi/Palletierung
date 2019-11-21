import pyglet
from pyglet.gl import glPushMatrix, glRotatef, glTranslatef, glMatrixMode, GL_PROJECTION, glLoadIdentity, GL_MODELVIEW, \
    gluOrtho2D, gluPerspective, glPopMatrix

from draw.Box.BoxDraw import BoxDraw


class Window(pyglet.window.Window):

    def addBox(self, box):
        self.boxes.append(BoxDraw(box))
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

    lock = False
    mouse_lock = property(lambda self: self.lock, setLock)


    def update(self, dt):
        self.spectator.update(dt, self.keys)

