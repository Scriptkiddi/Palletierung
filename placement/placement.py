import itertools
from math import ceil

from placement.difference_process import difference_process
from placement.objects.EmptyMaximumSpace import EmptyMaximumSpace
from placement.back_bottom_left import back_bottom_left


def placement(boxes_to_pack, box_types, vector_layer_types, full_support=True):
    emss = [EmptyMaximumSpace(0, 0, 0, 1200, 800, 1500)]  # Empty bin Maximal Space
    layers = []
    while not_all_skipped(box_types):
        # print(len(list(filter(lambda x: x.skip, box_types))))
        i = 0
        # get index of first box that is not skipped or packed
        for j, box in enumerate(boxes_to_pack):
            if not box.is_packed() and not box.get_type().skip:
                i = j
        box = boxes_to_pack[i]
        box_type = box.get_type()
        ems = back_bottom_left(box, emss)
        if ems is None:
            print("Cannot fit box {} of  {}".format(box, box_type))
            box.get_type().skip = True
        else:
            print("Packing box {} of {}".format(box, box_type))
            print("-Generating Layers")
            layers_with_quantity = box.get_layers(ems, box_type.quantity())
            max_layers = len(layers_with_quantity)
            layer = layers_with_quantity[ceil(vector_layer_types[i] * max_layers) - 1]  # -1 because index offset
            print("-Layer: {}, quant: {} {}-{}".format(layer, layer.quantity, layer.direction[0], layer.direction[1]))
            print("-Placed {}/{} boxes of {}".format(layer.quantity, box_type.quantity(), box_type.identifier))
            box_type.update_quantity(box_type.quantity() - layer.quantity)
            assert box_type.quantity() >= 0
            print("-Place Layer")
            layer.place(ems.x, ems.y, ems.z)
            layers.append(layer)
            # update s
            print("-Update S")
            # TODo this is broken
            # TODo  is this the correct processes? do the boundaries align
            print(emss)
            emss = difference_process(layer, emss)  # Apply DP process from Lai and Chan (1997)
            print(emss)
            emss = remove_overlapping(ems, emss)
            print("-Number of emss {}".format(len(emss)))
            # print(emss)
            if full_support:
                for ems in emss:
                    if ems.height == layer.urc()[2]:
                        print("run max join")
                        pass
                        # ems = maxjoin(ems) TODo implement
                pass
            # print(box)
    return layers
    # Apply Max Join procedure


def not_all_skipped(box_types):
    for box_type in box_types:
        if not box_type.skip:
            return True
    return False


def remove_overlapping(opt_ems, intervals):
    # Removing intervals that are inside another interval
    for interval_a, interval_b in itertools.combinations(intervals, 2):
        x1, y1, z1 = interval_a.llc()
        x2, y2, z2 = interval_a.urc()
        x3, y3, z3 = interval_b.llc()
        x4, y4, z4 = interval_b.urc()
        if x1 >= x3 and y1 >= y3 and z1 >= z3 and x2 <= x4 and y2 <= y4 and z2 <= z4:
            # print("Removing {} it overlaps with {}".format(interval_a, interval_b))
            if interval_a in intervals:
                intervals.remove(interval_a)
    #for interval in intervals:
    #    x1, y1, z1 = interval.llc()
    #    x2, y2, z2 = interval.urc()
    #    x3, y3, z3 = opt_ems.llc()
    #    x4, y4, z4 = opt_ems.urc()
    #    if x1 >= x3 and y1 >= y3 and z1 >= z3 and x2 <= x4 and y2 <= y4 and z2 <= z4:
    #        print("Removing {} it overlaps with {}".format(interval, opt_ems))
    #        try:
    #            intervals.remove(interval)
    #        except ValueError:
    #            pass
    return intervals
