def back_bottom_left(box, empty_maximal_spaces):
    """
    Back Bottom Left procedure decides where a box should be placed and if it can be placed
    :param box:
    :param empty_maximal_spaces:
    :return:
    """
    # Back-Bottom-Left procedure
    ems_opt = None
    for ems in empty_maximal_spaces:
        if ems.width >= box.width and ems.depth >= box.depth and ems.height >= box.height:
            if ems_opt == None:
                ems_opt = ems
            if ems.z < ems_opt.z or \
                    ems.z == ems_opt.z and ems.x < ems_opt.x or \
                    ems.z == ems_opt.z and ems.x == ems_opt.x and ems.y < ems_opt.y:
                ems_opt = ems

    # print("--Opt ems {} for box {}".format(ems_opt, box))
    return ems_opt
