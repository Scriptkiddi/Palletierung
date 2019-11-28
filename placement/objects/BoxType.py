class BoxType:
    def __init__(self, identifier):
        self.identifier = identifier
        self.skip = False
        self.__quantity = 0
        self.boxes = []

    def add_box(self, box):
        self.__quantity += 1
        self.boxes.append(box)

    def quantity(self):
        return self.__quantity

    def update_quantity(self, quantity):
        self.__quantity = quantity
        if self.__quantity == 0:
            self.skip = True

    def get_boxes(self):
        return self.boxes

    def __str__(self):
        return "type: {}, quant: {}, skip: {}".format(self.identifier[:5], self.__quantity, self.skip)

    def __repr__(self):
        return self.__str__()
