import itertools

from placement.objects.EmptyMaximumSpace import EmptyMaximumSpace


def difference_process(box, spaces):
    # Taken from "Developing a simulated annealing algorithm for the cutting stock problem" K.K.LaiJimmy W.M.Chan 1997
    # Get bottom left corner of our space and upper right corner
    intervals = []
    for space in spaces:
        x1, y1, z1 = space.llc()
        x2, y2, z2 = space.urc()
        # print("--------------")
        # print("Space: {}".format(space))
        # print("Box: {}".format(box))
        # get bottom left corner of our box and upper right corner
        x3, y3, z3 = box.llc()
        x4, y4, z4 = box.urc()
        if (x1 <= x3 and x4 <= x2 and y1 <= y3 and y4 <= y2 or
                x1 <= x3 and x4 <= x2 and z1 <= z3 and z4 <= y2 or
                y1 <= y3 and y4 <= y2 and z1 <= z3 and z4 <= y2):
            # assert x1 <= x3 <= x4 <= x2
            # assert y1 <= y3 <= y4 <= y2
            # assert z1 <= z3 <= z4 <= z2
            intervals += [
                EmptyMaximumSpace(x1, y1, z1, x3, y2, z2),
                EmptyMaximumSpace(x4, y1, z1, x2, y2, z2),
                EmptyMaximumSpace(x1, y1, z1, x2, y3, z2),
                EmptyMaximumSpace(x1, y4, z1, x2, y2, z2),
                EmptyMaximumSpace(x1, y1, z1, x2, y2, z3),
                EmptyMaximumSpace(x1, y1, z4, x4, y4, z2)
                # oder x1,y1,z4,x2,y2,z2 änderung weil support von unten benötigt
            ]
            # print("Intervals before Removal: {}".format(intervals))

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

    # Removing "thin" intervals
    for interval in intervals:
        x1, y1, z1 = interval.llc()
        x2, y2, z2 = interval.urc()
        if x1 == x2 or y1 == y2 or z1 == z2:
            # print("Removing because its thin: {}".format(interval))
            intervals.remove(interval)

    # Removing out of bound intervals
    for interval in intervals:
        x1, y1, z1 = interval.llc()
        x2, y2, z2 = interval.urc()
        if x2 > 1200 or y2 > 800 or z2 > 1500:
            # print("removing because boundary")
            intervals.remove(interval)
    # print("Intervals after Removal: {}".format(intervals))
    # print("--------------")
    return intervals