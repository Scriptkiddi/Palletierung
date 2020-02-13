from math import floor

from placement.objects.Cube import Cube
from placement.objects.EmptyMaximumSpace import EmptyMaximumSpace
from placement.objects.Layer import Layer


class Box(Cube):
    def __init__(self, width, depth, height, type_id, box_type, weight, x=None, y=None, z=None, rotate_xy=False,
                 rotate_xz=False, rotate_yz=False):
        self.x = x
        self.y = y
        self.z = z
        self.box_type = box_type
        self.weight = weight
        self.width = width
        self.depth = depth
        self.height = height
        self.type_id = type_id
        self.packed = False
        self.layer = None
        self.rotate = (rotate_xy, rotate_xz, rotate_yz)

    def get_type(self):
        return self.box_type

    def get_layer(self, ems, quantity, direction):
        max_boxes_direction_1 = 0
        for i in range(0, quantity):
            if direction[0][0] >= direction[0][1] + direction[0][2] * (i + 1):
                max_boxes_direction_1 = i + 1
        if max_boxes_direction_1 == 0:
            # print("Box {}".format(self))
            # print("EMS {}".format(ems))
            return None
        max_boxes_direction_2 = 0
        for i in range(0, floor(quantity / max_boxes_direction_1 - 1) + 1):
            if direction[1][0] >= direction[1][1] + direction[1][2] * (i + 1):
                max_boxes_direction_2 = i + 1
        max_boxes = 0
        if max_boxes_direction_2 > 0 and max_boxes_direction_1 > 0:
            max_boxes = max_boxes_direction_2 * max_boxes_direction_1

        # Reduce number of boxes to a number that forms a square
        if max_boxes > quantity:
            max_boxes = quantity - (quantity % max_boxes_direction_1)

        # print("EMS {}".format(ems))
        # print("width {}, depth {}".format(self.width, self.depth))
        layer = Layer(ems.x, ems.y, ems.z, self.width, self.depth,
                      self.height, self.get_type(), max_boxes,
                      ((direction[0][3], max_boxes_direction_1), (direction[1][3], max_boxes_direction_2)))
        if direction[0][3] == "x":
            layer.width = self.width * max_boxes_direction_1
        elif direction[0][3] == "y":
            layer.depth = self.depth * max_boxes_direction_1
        elif direction[0][3] == "z":
            layer.height = self.height * max_boxes_direction_1

        if direction[1][3] == "x":
            layer.width = self.width * max_boxes_direction_2
        elif direction[1][3] == "y":
            layer.depth = self.depth * max_boxes_direction_2
        elif direction[1][3] == "z":
            layer.height = self.height * max_boxes_direction_2
        return layer

    def get_layers(self, ems, quantity):
        """
        This function only generates layers for rotation on x, y axis since the robot arm can not flip boxes
        Extend this function as soon as this is required

        :param ems:
        :param quantity:
        :return:
        """
        layers_with_quantity = []
        layers_with_quantity.append(self.get_layer(ems, quantity,
                                                   [(ems.urc()[0], ems.x, self.width, "x"),
                                                    (ems.urc()[1], ems.y, self.depth, "y")]))
        layers_with_quantity.append(self.get_layer(ems, quantity,
                                                   [(ems.urc()[0], ems.x, self.width, "x"),
                                                    (ems.urc()[2], ems.z, self.height, "z")]))
        layers_with_quantity.append(self.get_layer(ems, quantity,
                                                   [(ems.urc()[1], ems.y, self.depth, "y"),
                                                    (ems.urc()[2], ems.z, self.height, "z")]))
        layers_with_quantity.append(self.get_layer(ems, quantity,
                                                   [(ems.urc()[1], ems.y, self.depth, "y"),
                                                    (ems.urc()[0], ems.x, self.width, "x")]))
        layers_with_quantity.append(self.get_layer(ems, quantity,
                                                   [(ems.urc()[2], ems.z, self.height, "z"),
                                                    (ems.urc()[0], ems.x, self.width, "x")]))
        layers_with_quantity.append(self.get_layer(ems, quantity,
                                                   [(ems.urc()[2], ems.z, self.height, "z"),
                                                    (ems.urc()[1], ems.y, self.depth, "y")]))
        if self.rotate[0]:
            # For this section width and depth are switched
            tmp_original_width = self.width
            tmp_original_depth = self.depth
            self.width = tmp_original_depth
            self.depth = tmp_original_width
            if ems.width >= self.width and ems.depth >= self.depth and ems.height >= self.height:
                layers_with_quantity.append(self.get_layer(ems, quantity,
                                                           [(ems.urc()[0], ems.x, self.width, "x"),
                                                            (ems.urc()[1], ems.y, self.depth, "y")]))
                layers_with_quantity.append(self.get_layer(ems, quantity,
                                                           [(ems.urc()[0], ems.x, self.width, "x"),
                                                            (ems.urc()[2], ems.z, self.height, "z")]))
                layers_with_quantity.append(self.get_layer(ems, quantity,
                                                           [(ems.urc()[1], ems.y, self.depth, "y"),
                                                            (ems.urc()[2], ems.z, self.height, "z")]))
                layers_with_quantity.append(self.get_layer(ems, quantity,
                                                           [(ems.urc()[1], ems.y, self.depth, "y"),
                                                            (ems.urc()[0], ems.x, self.width, "x")]))
                layers_with_quantity.append(self.get_layer(ems, quantity,
                                                           [(ems.urc()[2], ems.z, self.height, "z"),
                                                            (ems.urc()[0], ems.x, self.width, "x")]))
                layers_with_quantity.append(self.get_layer(ems, quantity,
                                                           [(ems.urc()[2], ems.z, self.height, "z"),
                                                            (ems.urc()[1], ems.y, self.depth, "y")]))
                self.width = tmp_original_width
                self.depth = tmp_original_depth

            elif self.rotate[1] or self.rotate[2]:
                print(self.rotate)
                # this code should never be reached since we can not rotate our boxes this way
                assert False

            layers_to_remove = []
            for x in layers_with_quantity:
                if x is None:
                    layers_to_remove.append(x)
            for x in layers_to_remove:
                layers_with_quantity.remove(x)
        return layers_with_quantity

    def is_packed(self):
        return self.packed

    def get_type_id(self):
        return self.type_id

    def place(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        assert self.packed == False, "trying to pack a box again"
        self.packed = True
