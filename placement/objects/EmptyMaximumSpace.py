from placement.objects.Cube import Cube


class EmptyMaximumSpace(Cube):
    def __init__(self, x1, y1, z1, x2, y2, z2):
        width = x2 - x1
        depth = y2 - y1
        height = z2 - z1
        super(EmptyMaximumSpace, self).__init__(x1, y1, z1, width, depth, height)

    def __str__(self):
        return "({},{})x({},{})x({},{})".format(self.x, self.x + self.width, self.y, self.y + self.depth, self.z,
                                                self.z + self.height)

    def __repr__(self):
        return self.__str__()
