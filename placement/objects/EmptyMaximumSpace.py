from copy import deepcopy

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

    def crop_layer(self, layer):
        layer_cropped = deepcopy(layer)
        x1, y1, z1 = self.llc()
        x2, y2, z2 = self.urc()
        x3, y3, z3 = layer.llc()
        x4, y4, z4 = layer.urc()

        if not x1 <= x3:
            print("fixing x3")
            layer_cropped.width = (x4 - x1)
            layer_cropped.x = x1
        if not x4 <= x2:
            print("fixing x4")
            layer_cropped.width = x2 - x3
        if not x1 <= x3 and not x4 <= x2:
            print("fixingxz3 & x4")
            layer_cropped.x = x1
            layer_cropped.width = x2 - x1
        if not y1 <= y3:
            print("fixing y3")
            layer_cropped.depth = (y4 - y1)
            layer_cropped.y = y1
        if not y4 <= y2:
            print("fixing y4")
            layer_cropped.depth = y2 - y3
        if not y1 <= y3 and not y4 <= y2:
            print("fixing y3 & y4")
            layer_cropped.y = y1
            layer_cropped.depth = y2 - y1
        if not z1 <= z3:
            print("fixing z3")
            layer_cropped.height = (z4 - z1)
            layer_cropped.z = z1
        if not z4 <= z2:
            print("fixing z4")
            layer_cropped.height = z2 - z3
        if not z1 <= z3 and not z4 <= z2:
            print("fixing z3 & z4")
            layer_cropped.z = z1
            layer_cropped.height = z2 - z1
        return layer_cropped

