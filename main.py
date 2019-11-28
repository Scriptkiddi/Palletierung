import random
import csv

import pyglet
from pyglet.gl import glClearColor, GL_DEPTH_TEST, glEnable

from placement.objects.Box import Box

from draw.Window.Window2D import Window2D
from draw.Window.Window3D import Window3D
from placement.objects.BoxType import BoxType
from placement.placement import placement

IND_INIT_SIZE = 5
MAX_ITEM = 50
MAX_WEIGHT = 50
NBR_ITEMS = 20

# To assure reproductibility, the RNG seed is set prior to the items
# dict initialization. It is also seeded in main().
random.seed(64)


# Creating Fitness Class, and set the Objective to maximize
# creator.create("Fitness", base.Fitness, weights=(1.0,))
# creator.create("Individual", list, fitness=creator.Fitness)
# IND_SIZE=10
#
# toolbox = base.Toolbox()
# toolbox.register("attr_float", random.uniform(0, 1))
# toolbox.register("individual", tools.initRepeat, creator.Individual,
#                 toolbox.attr_float, n=IND_SIZE)


# toolbox = base.Toolbox()
#
## Attribute generator
# toolbox.register("attr_item", random.randrange, NBR_ITEMS)
#
## Structure initializers
# toolbox.register("individual", tools.initRepeat, creator.Individual,
#                 toolbox.attr_item, IND_INIT_SIZE)
# toolbox.register("population", tools.initRepeat, list, toolbox.individual)


def remove_overlapping(opt_ems, emss):
    # Removing intervals that are inside another interval
    for interval in emss:
        x1, y1, z1 = interval.llc()
        x2, y2, z2 = interval.urc()
        x3, y3, z3 = opt_ems.llc()
        x4, y4, z4 = opt_ems.urc()
        if x1 >= x3 and y1 >= y3 and z1 >= z3 and x2 <= x4 and y2 <= y4 and z2 <= z4:
            print("Removing {} it overlaps with {}".format(interval, opt_ems))
            try:
                emss.remove(interval)
            except ValueError:
                pass
    return emss


def read_input(filename):
    boxes_to_pack = []
    box_types = []
    with open(filename) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=";")
        for row in csv_reader:
            width = int(row['Width'])
            height = int(row['Height'])
            depth = int(row['Depth'])
            type_id = row['Name']
            rotate_xy = bool(row['RotateXY'])
            rotate_xz = bool(row['RotateXZ'])
            rotate_yz = bool(row['RotateYZ'])
            box_type = BoxType(type_id)
            weight = 5
            for i in range(0, int(row['Quantity'])):
                box = (Box(width, depth, height, type_id, box_type, rotate_xy=rotate_xy, rotate_xz=rotate_xz,
                           rotate_yz=rotate_yz))
                boxes_to_pack.append(box)
                box_type.add_box(box)
            box_types.append(box_type)
        return boxes_to_pack, box_types


if __name__ == "__main__":
    # Reading in products and storing them into the item variable
    boxes_to_pack, box_types = read_input("resources/Maße_aldi.csv")
    vector_layer_types = []
    for i in boxes_to_pack:
        vector_layer_types.append(random.random())
    boxes_packed = placement(boxes_to_pack, box_types, vector_layer_types)
    print(boxes_packed)
    exit(0)
    # init empty palette
    # emss = [Palette(0, 0, 0, 1200, 800, 1500)]  # Empty bin Maximal Space
    ## items[0].place(opt_ems.x, opt_ems.y, opt_ems.z)
    # for item in items:
    #    opt_ems = bbl(item, emss)
    #    item.place(opt_ems.x, opt_ems.y, opt_ems.z)
    #    emss = remove_overlapping(opt_ems, emss)
    #    new_emss = difference_process(item, opt_ems)
    #    emss += new_emss
    width = 1200
    depth = 800
    height = 1500
    window3d = Window3D(boxes_packed, width, depth, height, width=854, height=480, caption='Palettierung', resizable=True)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.5, 0.7, 1, 1)
    debug_2d = False
    if debug_2d:
        windowXY = Window2D(items, width, depth, height, True, True, False, width=854, height=480, caption='XY',
                            resizable=True)
        glClearColor(0.5, 0.7, 1, 1)
        windowXZ = Window2D(items, width, depth, height, True, False, True, width=854, height=480, caption='XZ',
                            resizable=True)
        glClearColor(0.5, 0.7, 1, 1)
        windowYZ = Window2D(items, width, depth, height, False, True, True, width=854, height=480, caption='YZ',
                            resizable=True)
        glClearColor(0.5, 0.7, 1, 1)
    pyglet.app.run()

    # emss = difference_process(items[0], palette)
    # print(emss)
