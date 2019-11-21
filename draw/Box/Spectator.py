import math

from pyglet.window import key


class Spectator:
    def __init__(self, pos=(0, 0, 0), rot=(0, 0)):
        self.pos = list(pos)
        self.rot = list(rot)

    def update(self, dt, keys):
        s = dt * 100
        rot_y = -self.rot[1] / 180 * math.pi
        dx, dz = s * math.sin(rot_y), s * math.cos(rot_y)
        if keys[key.W]:
            self.pos[0] += dx
            self.pos[2] -= dz
        if keys[key.S]:
            self.pos[0] -= dx
            self.pos[2] += dz
        if keys[key.A]:
            self.pos[0] -= dz
            self.pos[2] -= dx
        if keys[key.D]:
            self.pos[0] += dz
            self.pos[2] += dx

        if keys[key.SPACE]:
            self.pos[1] += s
        if keys[key.LSHIFT]:
            self.pos[1] -= s
