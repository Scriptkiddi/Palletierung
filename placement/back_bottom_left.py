def back_bottom_left(box, empty_maximal_spaces):
    # Back-Bottom-Left procedure
    ems_opt = None
    for ems in empty_maximal_spaces:
        # print("for every ems {} and box {}".format(ems, box))
        # if ems.height >= 1500 or ems.width >= 1200 or ems.depth >= 800:
        #    continue
        if ems.width >= box.width and ems.depth >= box.depth and ems.height >= box.height:
            # print("box fits into ems")
            if ems_opt == None:
                ems_opt = ems
            if ems.z < ems_opt.z or \
                    ems.z == ems_opt.z and ems.x < ems_opt.x or \
                    ems.z == ems_opt.z and ems.x == ems_opt.x and ems.y < ems_opt.y:
                # print("---EMS {}x{}x{}".format(ems.width, ems.depth, ems.height))
                ems_opt = ems

    # print("--Opt ems {} for box {}".format(ems_opt, box))
    return ems_opt
