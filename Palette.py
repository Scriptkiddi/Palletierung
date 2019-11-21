class Palette:
    def __init__(self, x, y, z, width, depth, height):
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.depth = depth
        self.height = height

    def llc(self):  # Lower Left Corner
        return self.x, self.y, self.z

    def urc(self):  # Upper Right Corner
        return self.width, self.depth, self.height

    def place(self, x, y, z):  # Upper Right Corner
        print("placing at {}x{}x{}".format(x, y, z))
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return str(self.llc()) + str(self.urc())

    def __repr__(self):
        return self.__str__()
