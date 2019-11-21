class Palette:
    def __init__(self, x1, y1, z1, x2, y2, z2):
        self.x = x1
        self.y = y1
        self.z = z1
        self.width = x2-x1
        self.depth = y2-y1
        self.height = z2-z1

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
