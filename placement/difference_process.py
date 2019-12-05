import itertools
from copy import deepcopy

from placement.objects.EmptyMaximumSpace import EmptyMaximumSpace

def difference_process(layer, space):
    x3, y3, z3 = layer.llc()
    x4, y4, z4 = layer.urc()
    intervals = []
    x1, y1, z1 = space.llc()
    x2, y2, z2 = space.urc()
    assert x1 <= x3 <= x4 <= x2
    assert y1 <= y3 <= y4 <= y2
    assert z1 <= z3 <= z4 <= z2
    intervals = [
        EmptyMaximumSpace(x1, y1, z1, x3, y2, z2),
        EmptyMaximumSpace(x4, y1, z1, x2, y2, z2),
        EmptyMaximumSpace(x1, y1, z1, x2, y3, z2),
        EmptyMaximumSpace(x1, y4, z1, x2, y2, z2),
        EmptyMaximumSpace(x1, y1, z1, x4, y4, z3),  # this is always 0 if you are not placing thing into the air
        EmptyMaximumSpace(x1, y1, z4, x4, y4, z2)
        # oder x1,y1,z4,x2,y2,z2 falls kein support von unten benötigt wird
    ]

    # Taken from "Developing a simulated annealing algorithm for the cutting stock problem" K.K.LaiJimmy W.M.Chan 1997
    # Get bottom left corner of our space and upper right corner
    #print("Intervals before Removal: {}".format(intervals))

    # Removing intervals that are inside another interval
    intervals_to_remove = []
    for interval_a, interval_b in itertools.combinations(intervals, 2):
        x1, y1, z1 = interval_a.llc()
        x2, y2, z2 = interval_a.urc()
        x3, y3, z3 = interval_b.llc()
        x4, y4, z4 = interval_b.urc()
        if x1 >= x3 and y1 >= y3 and z1 >= z3 and x2 <= x4 and y2 <= y4 and z2 <= z4:
            # print("Removing {} it overlaps with {}".format(interval_a, interval_b))
            intervals_to_remove.append(interval_a)
            if interval_a in intervals:
                intervals.remove(interval_a)

    # Removing "thin" intervals
    for interval in intervals:
        x1, y1, z1 = interval.llc()
        x2, y2, z2 = interval.urc()
        if x1 == x2 or y1 == y2 or z1 == z2:
            #print("Removing because its thin: {}".format(interval))
            intervals_to_remove.append(interval)
            #intervals.remove(interval)

    for interval in intervals_to_remove:
        if interval in intervals:
            #print("remove {}".format(interval))
            intervals.remove(interval)
    # Removing out of bound intervals
    for interval in intervals:
        x2, y2, z2 = interval.urc()
        if x2 > 1200 or y2 > 800 or z2 > 1500:
            # print("removing because boundary")
            assert False
            intervals.remove(interval)
    # print("Intervals after Removal: {}".format(intervals))
    # print("--------------")
    return intervals
    #if x1 == x2 or y1 == y2 or z1 == z2:
    #    continue
    #if not (x2 <= x3 or x1 >= x4 or y1 <= y3 or y1 >= y4 or z2 <= z3 or z1 >= z4):
    #    print("overlapp {} {}".format(space, layer))
    #    # if layer in space:
    #    layer_part = deepcopy(layer)
    #    if not x1 <= x3:
    #        print("fixing x3")
    #        layer_part.width = (x4 - x1)
    #        layer_part.x = x1
    #    if not x4 <= x2:
    #        print("fixing x4")
    #        layer_part.width = x2 - x3
    #    if not x1 <= x3 and not x4 <= x2:
    #        print("fixingxz3 & x4")
    #        layer_part.x = x1
    #        layer_part.width = x2 - x1
    #    if not y1 <= y3:
    #        print("fixing y3")
    #        layer_part.depth = (y4 - y1)
    #        layer_part.y = y1
    #    if not y4 <= y2:
    #        print("fixing y4")
    #        layer_part.depth = y2 - y3
    #    if not y1 <= y3 and not y4 <= y2:
    #        print("fixing y3 & y4")
    #        layer_part.y = y1
    #        layer_part.depth = y2 - y1
    #    if not z1 <= z3:
    #        print("fixing z3")
    #        layer_part.height = (z4 - z1)
    #        layer_part.z = z1
    #    if not z4 <= z2:
    #        print("fixing z4")
    #        layer_part.height = z2 - z3
    #    if not z1 <= z3 and not z4 <= z2:
    #        print("fixing z3 & z4")
    #        layer_part.z = z1
    #        layer_part.height = z2 - z1
    #    print(layer_part)
    #    intervals += dp_split(layer_part, space)
    #elif x2 - x1 >= layer.width and y2 - y1 >= layer.depth and z2 - z1 >= layer.height and x1 <= x3 and x4 <= x2 and y1 <= y3 and y4 <= y2 and z1 <= z3 and z4 <= z2:
    #    print("no overlapp")
    #    intervals += dp_split(layer, space)

