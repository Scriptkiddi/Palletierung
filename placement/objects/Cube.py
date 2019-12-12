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
        #print("Placing at {}x{}x{}".format(x, y, z))
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

    def in_ems(self, ems):
        x1, y1, z1 = ems.llc()
        x2, y2, z2 = ems.urc()
        x3, y3, z3 = self.llc()
        x4, y4, z4 = self.urc()
        if not (x2 < x3 or x1 > x4 or y2 < y3 or y1 > y4 or z2 < z3 or z1 > z4): # Intersecting volumes
            #print("Layer {} is part in EMS: {}".format(self, ems))
            return True
        elif x1 <= x3 and x4 <= x2 and y1 <= y3 and y4 <= y2 and z1 <= z3 and z4 <= z2: # surrounded volume
            #print("Layer {} is completly part in EMS: {}".format(self, ems))
            return True
        return False

    def is_thin(self):
        x1, y1, z1 = self.llc()
        x2, y2, z2 = self.urc()
        if x1 == x2 or y1 == y2 or z1 == z2:
            #print("Layer {} is thin".format(self))
            return True
        return False
