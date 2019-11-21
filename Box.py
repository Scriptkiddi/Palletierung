class Box:
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
