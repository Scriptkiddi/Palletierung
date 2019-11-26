from Palette import Palette


class Box:
    def __init__(self, x, y, z, width, depth, height, type_id, rotate_x, rotate_y, rotate_z):
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.depth = depth
        self.height = height
        self.type_id = type_id
        self.packed = False
        self.rotate = (rotate_x, rotate_y, rotate_z)

    def get_layers(self, ems, quantity):
        ems.x + self.width
        layers = []
        max_i_x = 0
        for i in range(0, quantity):
            if ems.urc()[0] >= ems.x + self.width * i:
                max_i_x = i
            else:
                break
        max_i_z = 0
        for i in range(0, quantity):
            if ems.urc()[2] >= ems.z + self.height * i:
                max_i_z = i

        if max_i_z > 0 and max_i_x > 0:
            max_i = max_i_z * max_i_x


    Palette(ems.x, ems.y, ems.z, ems.x, self.width, self.height),
    layers.append({'x': self.width, 'z': self.height})
    layers.append({'x': self.width, 'z': self.height})
    # layer("x,z)
    # layer(z,x)
    # layer(x,y)
    # layer(y,x)
    # layer(y,z)
    # layer(z,y)
    # todo maße bei nichts

    if self.rotate[0]:

    return []


def is_packed(self):
    return self.packed


def type_id(self):
    return self.type_id


def llc(self):  # Lower Left Corner
    return self.x, self.y, self.z


def urc(self):  # Upper Right Corner
    return self.x + self.width, self.y + self.depth, self.z + self.height


def place(self, x, y, z):
    print("placing at {}x{}x{}".format(x, y, z))
    self.x = x
    self.y = y
    self.z = z


def __str__(self):
    return str(self.llc()) + str(self.urc())


def __repr__(self):
    return self.__str__()
