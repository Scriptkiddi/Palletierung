import random
import csv
import timeit
import pyglet
from pyglet.gl import glClearColor, GL_DEPTH_TEST, glEnable

from genetics.genetics import run_genetics
from placement.objects.Box import Box

from draw.Window.Window2D import Window2D
from draw.Window.Window3D import Window3D
from placement.objects.BoxType import BoxType
from placement.placement import placement


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

            if int(row['Quantity']) > 0:
                box_types.append(box_type)
        return boxes_to_pack, box_types


if __name__ == "__main__":
    start = timeit.default_timer()
    boxes_to_pack, box_types = read_input("resources/Maße_aldi.csv")
    print(box_types)
    pop, stats, hof = run_genetics(boxes_to_pack, box_types)
    stop = timeit.default_timer()
    print('Time: ', stop - start)
    # TODO move this to a config file
    width = 1200
    depth = 800
    height = 1500
    random_keys = hof[0][0:len(boxes_to_pack)]
    btps_unsorted = map(lambda x: (x, boxes_to_pack[random_keys.index(x)]), random_keys)
    btps = sorted(btps_unsorted, key=lambda x: x[0])
    boxes = list(map(lambda x: x[1], btps))

    vector_layer_types = hof[0][len(box_types):]
    print(boxes)
    boxes_packed = placement(boxes, vector_layer_types)
    window3d = Window3D(boxes_packed, width, depth, height, width=854, height=480, caption='Palettierung',
                        resizable=True)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.5, 0.7, 1, 1)
    debug_2d = False
    if debug_2d:
        windowXY = Window2D(boxes_packed, width, depth, height, True, True, False, width=854, height=480, caption='XY',
                            resizable=True)
        glClearColor(0.5, 0.7, 1, 1)
        windowXZ = Window2D(boxes_packed, width, depth, height, True, False, True, width=854, height=480, caption='XZ',
                            resizable=True)
        glClearColor(0.5, 0.7, 1, 1)
        windowYZ = Window2D(boxes_packed, width, depth, height, False, True, True, width=854, height=480, caption='YZ',
                            resizable=True)
        glClearColor(0.5, 0.7, 1, 1)
    pyglet.app.run()

    # emss = difference_process(items[0], palette)
    # print(emss)
