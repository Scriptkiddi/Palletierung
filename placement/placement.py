import itertools
from copy import deepcopy
from math import ceil

from placement.difference_process import difference_process
from placement.objects.EmptyMaximumSpace import EmptyMaximumSpace
from placement.back_bottom_left import back_bottom_left
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

palette_width = int(config["palette"]["width"])
palette_depth = int(config["palette"]["depth"])
palette_height = int(config["palette"]["height"])
palette = EmptyMaximumSpace(0, 0, 0, palette_width, palette_depth, palette_height)


def difference_process_wrapper(empty_maximal_spaces, layer):
    new_emss = []
    emss_to_remove = []  # Changing a list while iterating over it does not work in python
    for ems in empty_maximal_spaces:
        if layer.in_ems(ems):
            layer_tmp = ems.crop_layer(layer)  # A layer object that is cropped to the current ems used
            if not layer_tmp.is_thin():
                new_emss = new_emss + difference_process(layer_tmp, ems)
                emss_to_remove.append(ems)
    # Removing empty maximal spaces that have been divided by the new placed layer
    for ems in emss_to_remove:
        if ems in empty_maximal_spaces:
            empty_maximal_spaces.remove(ems)
    # Merging the new spaces with our old empty_maximal_spaces
    return remove_included(new_emss + empty_maximal_spaces)


def placement(boxes_to_pack, vector_layer_types, debug=False, full_support=True):
    #print("{} need to be packed".format(len(boxes_to_pack)))
    ITER = 0
    empty_maximal_spaces = [deepcopy(palette)]  # Empty bin Maximal Space
    layers = []
    box_types = map(lambda box: box.get_type(), boxes_to_pack)
    while not_all_skipped(box_types):
        if debug:
            print("Iteration {}".format(ITER))
        ITER += 1
        i = 0
        # get index of first box that is not skipped or packed
        for j, box in enumerate(boxes_to_pack):
            if not box.is_packed() and not box.get_type().skip:
                i = j
        box = boxes_to_pack[i]
        box_type = box.get_type()
        ems = back_bottom_left(box, empty_maximal_spaces)
        if ems is None:
            if debug:
                print("Cannot fit box {} of  {}".format(box, box_type))
            box.get_type().skip = True
        else:
            if debug:
                print("Packing box {} of {}".format(box, box_type))
                print("EMS: {}".format(ems))
                print("-Generating Layers")
            layers_with_quantity = box.get_layers(ems, box_type.quantity())
            max_layers = len(layers_with_quantity)
            layer = layers_with_quantity[ceil(vector_layer_types[i] * max_layers) - 1]  # -1 because index offset
            if debug:
                print("-Layer: {}, quant: {} {}-{}".format(layer, layer.quantity, layer.direction[0], layer.direction[1]))
                print("-Placed {}/{} boxes of {}".format(layer.quantity, box_type.quantity(), box_type.identifier))
            box_type.update_quantity(box_type.quantity() - layer.quantity)
            assert box_type.quantity() >= 0
            if debug:
                print("-Place Layer")
            layer.place(ems.x, ems.y, ems.z)
            layers.append(layer)
            # update s
            if debug:
                print("-Update S")
            # emss = empty_maximal_spaces
            empty_maximal_spaces = difference_process_wrapper(empty_maximal_spaces, layer)
            if full_support:
                empty_maximal_spaces = max_join(layer, empty_maximal_spaces)
        if debug:
            print("-----")
    return layers, empty_maximal_spaces
    # Apply Max Join procedure


def max_join(layer, empty_maximal_spaces):
    """
    This function implements the maxjoin procedure from http://mauricio.resende.info/doc/brkga-pack3d.pdf

    :param layer: layer that was just placed
    :param empty_maximal_spaces:  list of empty maximal spaces that resulted from placing said layer
    :return: new list where spaces that have the same height are joined together
    """
    emss_with_same_height = []
    for ems in empty_maximal_spaces:
        if ems.llc()[2] == layer.urc()[2]:
            emss_with_same_height.append(ems)
    if len(emss_with_same_height) <= 1:
        return empty_maximal_spaces
    #print(emss_with_same_height)
    emss_first_round = [deepcopy(palette)]
    for ems in emss_with_same_height:
        empty_maximal_spaces.remove(ems)
        emss_first_round = difference_process_wrapper(emss_first_round, ems)
    #print(emss_first_round)
    emss_second_round = [deepcopy(palette)]
    for ems in emss_first_round:
        emss_second_round = difference_process_wrapper(emss_second_round, ems)
    empty_maximal_spaces += emss_second_round
    return empty_maximal_spaces


def not_all_skipped(box_types):
    for box_type in box_types:
        if not box_type.skip:
            return True
    return False


def remove_included(intervals):
    # Removing intervals that are inside another interval
    for interval_a, interval_b in itertools.combinations(intervals, 2):
        x1, y1, z1 = interval_a.llc()
        x2, y2, z2 = interval_a.urc()
        x3, y3, z3 = interval_b.llc()
        x4, y4, z4 = interval_b.urc()
        if x1 >= x3 and y1 >= y3 and z1 >= z3 and x2 <= x4 and y2 <= y4 and z2 <= z4:
            # print("Removing {} it is included from {}".format(interval_a, interval_b))
            if interval_a in intervals:
                intervals.remove(interval_a)
    return intervals
