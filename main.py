import random
import csv
import json
import timeit
import os
import pyglet
from pyglet.gl import glClearColor, GL_DEPTH_TEST, glEnable

from database import Result, db
from genetics.genetics import run_genetics
from placement.objects.Box import Box

from draw.Window.Window2D import Window2D
from draw.Window.Window3D import Window3D
from placement.objects.BoxType import BoxType
from placement.placement import placement
import configparser


def read_input(filename):
    """
    Reads a csv file as input to gather information what products are supposed to be packed onto the palette
    :param filename: Filepath to the csv file
    :return:
    """
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
            # Disable rotation along z axis
            rotate_xz = False
            rotate_yz = False

            box_type = BoxType(type_id)
            weight = int(row["Masse [g]"]) / 1000  # transform g to kg
            for i in range(0, int(row['Quantity'])):
                box = (Box(width, depth, height, type_id, box_type, weight, rotate_xy=rotate_xy, rotate_xz=rotate_xz,
                           rotate_yz=rotate_yz))
                boxes_to_pack.append(box)
                box_type.add_box(box)

            if int(row['Quantity']) > 0:
                box_types.append(box_type)
        return boxes_to_pack, box_types


def save_results(test_name, start_time, end_time, population_size, number_of_generations, pop, stats):
    """
    Saves results into a sqlite db for comparison later
    :param test_name:
    :param start_time:
    :param end_time:
    :param population_size:
    :param number_of_generations:
    :param pop:
    :param stats:
    :return:
    """
    record = stats.compile(pop)
    config = configparser.ConfigParser()
    config.read("config.ini")
    palette_width = int(config["palette"]["width"])
    palette_depth = int(config["palette"]["depth"])
    palette_height = int(config["palette"]["height"])
    palette_max_weight = int(config["palette"]["weight"])
    print(record)
    fitness_max = record['max']
    fitness_min = record['min']
    fitness_avg = record['avg']
    Result.create(test_name=test_name, start_time=start_time, end_time=end_time,
                  number_of_generations=number_of_generations, population_size=population_size,
                  max_fitness=fitness_max, min_fitness=fitness_min, average_fitness=fitness_avg,
                  palette_max_weight=palette_max_weight,
                  palette_width=palette_width, palette_height=palette_height, palette_depth=palette_depth)


def get_packed_boxes_from_ind(ind, boxes_to_pack, box_types):
    """
    Extract boxes packed from an individual used to get actual x,y,z coordinates

    :param ind:
    :param boxes_to_pack:
    :param box_types:
    :return:
    """
    random_keys = ind[0:len(boxes_to_pack)]
    btps_unsorted = map(lambda x: (x, boxes_to_pack[random_keys.index(x)]), random_keys)
    btps = sorted(btps_unsorted, key=lambda x: x[0])
    boxes = list(map(lambda x: x[1], btps))

    vector_layer_types = ind[len(box_types):]
    print(boxes)
    boxes_packed, emss = placement(boxes, vector_layer_types, debug=True)
    return boxes_packed


def get_packing_order(ind, boxes_to_pack, box_types, test_name="default"):
    """
    Generate a packing order from an individual and write it as json output
    :param ind:
    :param boxes_to_pack:
    :param box_types:
    :param test_name:
    :return:
    """
    layers_packed = get_packed_boxes_from_ind(ind, boxes_to_pack, box_types)
    packing_order = []
    for layer in layers_packed:
        for box in layer.boxes:
            x, y, z = box.llc()
            packing_order.append({"id": box.box_type.identifier, "x": x, "y": y, "z": z, "rotate": box.rotate})
            print(f"{box.box_type.identifier} at {box.llc()}")
    with open(f"packing_order_{test_name}.json", 'w') as json_file:
        json.dump(packing_order, json_file, indent=4)


def run_tests():
    """
    Runs different test scenarios
    :return:
    """
    db.connect()
    db.create_tables([Result])

    config = configparser.ConfigParser()
    config.read("config.ini")
    number_of_generations = int(config["genetics"]["number_of_generations"])

    test_file_paths = []

    for file in os.listdir("resources/tests/umpalettierung"):
        if file.endswith(".csv"):
            test_file_paths.append(os.path.join("resources/tests/umpalettierung", file))

    for path in test_file_paths:
        start = timeit.default_timer()
        boxes_to_pack, box_types = read_input(path)
        size_of_population = int(config["genetics"]["population_multiplier"]) * len(boxes_to_pack)
        test_name_list = []
        for box_type in box_types:
            test_name_list.append(f"{box_type.identifier[:5]}_{box_type.quantity()}")
        test_name_list.sort()
        test_name = '.'.join(test_name_list)
        print(
            f"Running {test_name} with {number_of_generations} generations with a population size of {size_of_population}")
        print(box_types)
        pop, stats, hof = run_genetics(boxes_to_pack, box_types, number_of_generations, size_of_population)
        get_packing_order(hof[0], boxes_to_pack, box_types, test_name=test_name)
        stop = timeit.default_timer()
        save_results(test_name, start, stop, len(pop), number_of_generations, pop, stats)


if __name__ == "__main__":
    run_tests()
    exit(0)
    config = configparser.ConfigParser()
    config.read("config.ini")
    start = timeit.default_timer()
    boxes_to_pack, box_types = read_input("resources/tests/umpalettierung/umpalettierung8.csv")
    size_of_population = int(config["genetics"]["population_multiplier"]) * len(boxes_to_pack)
    number_of_generations = int(config["genetics"]["number_of_generations"])
    pop, stats, hof = run_genetics(boxes_to_pack, box_types, number_of_generations, size_of_population)
    stop = timeit.default_timer()
    print('Time: ', stop - start)
    width = int(config["palette"]["width"])
    depth = int(config["palette"]["depth"])
    height = int(config["palette"]["height"])
    print(stats.compile(pop))
    boxes_packed = get_packed_boxes_from_ind(hof[0], boxes_to_pack, box_types)
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

## emss = difference_process(items[0], palette)
## print(emss)
