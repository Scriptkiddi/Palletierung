from placement.objects.Cube import Cube


class Layer(Cube):
    def __init__(self, x1, y1, z1, width, depth, height, box_type, quantity_in_layer, direction):
        boxes = list(filter(lambda x: x.layer is None, box_type.get_boxes()))
        assert len(boxes) >= quantity_in_layer, "Trying to place more boxes than available"
        self.box_type = box_type
        self.boxes = []
        for box in boxes[:quantity_in_layer]:
            self.boxes.append(box)
        self.quantity = quantity_in_layer
        self.direction = direction
        super(Layer, self).__init__(x1, y1, z1, width, depth, height)

    def in_ems(self, ems):
        x1, y1, z1 = ems.llc()
        x2, y2, z2 = ems.urc()
        x3, y3, z3 = self.llc()
        x4, y4, z4 = self.urc()
        if not (x2 < x3 or x1 > x4 or y2 < y3 or y1 > y4 or z2 < z3 or z1 > z4): # Intersecting volumes
            print("Layer {} is part in EMS: {}".format(self, ems))
            return True
        elif x1 <= x3 and x4 <= x2 and y1 <= y3 and y4 <= y2 and z1 <= z3 and z4 <= z2: # surrounded volume
            print("Layer {} is completly part in EMS: {}".format(self, ems))
            return True
        return False

    def is_thin(self):
        x1, y1, z1 = self.llc()
        x2, y2, z2 = self.urc()
        if x1 == x2 or y1 == y2 or z1 == z2:
            print("Layer {} is thin".format(self))
            return True
        return False

    def place(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        for j in range(0, self.direction[1][1]):
            for i in range(0, self.direction[0][1]):
                index = self.direction[0][1] * j + i
                box = self.boxes[index]
                x = self.x
                y = self.y
                z = self.z
                if self.direction[0][0] == "x":
                    x = self.x + i * box.width
                elif self.direction[0][0] == "y":
                    y = self.y + i * box.depth
                elif self.direction[0][0] == "z":
                    z = self.z + i * box.height

                if self.direction[1][0] == "x":
                    x = self.x + j * box.width
                elif self.direction[1][0] == "y":
                    y = self.y + j * box.depth
                elif self.direction[1][0] == "z":
                    z = self.z + j * box.height
                box.place(x, y, z)
                box.layer = self

    def __str__(self):
        if self.x is not None and self.y is not None and self.z is not None:
            return "({},{})x({},{})x({},{})".format(self.x, self.x + self.width, self.y, self.y + self.depth, self.z,
                                                    self.z + self.height)
        else:
            return "{}x{}x{}".format(self.width, self.depth, self.height)

    def __repr__(self):
        return self.__str__()
