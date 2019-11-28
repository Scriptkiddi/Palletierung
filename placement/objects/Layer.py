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

