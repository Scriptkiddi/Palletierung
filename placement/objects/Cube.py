class Cube:
    def __init__(self, x, y, z, width, depth, height, rotate_xy=False, rotate_xz=False, rotate_yz=False):
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.depth = depth
        self.height = height
        self.rotate = (rotate_xy, rotate_xz, rotate_yz)

    def llc(self):  # Lower Left Corner
        return self.x, self.y, self.z

    def urc(self):  # Upper Right Corner
        return self.x + self.width, self.y + self.depth, self.z + self.height

    def place(self, x, y, z):
        print("Placing at {}x{}x{}".format(x, y, z))
        self.x = x
        self.y = y
        self.z = z
        self.packed = True

    def __str__(self):
        string = "{}x{}x{}".format(self.width, self.depth, self.height)
        if self.x and self.y and self.z:
            string += " placed at: {}x{}x{}".format(self.x, self.y, self.z)
        return string

    def __repr__(self):
        return self.__str__()
