def back_bottom_left(box, empty_maximal_spaces):
    # Back-Bottom-Left procedure
    ems_opt = None
    for ems in empty_maximal_spaces:
        # if ems.height >= 1500 or ems.width >= 1200 or ems.depth >= 800:
        #    continue
        if ems.width >= box.width and ems.depth >= box.depth and ems.height >= box.height:
            if ems_opt == None:
                ems_opt = ems
            if ems.x < ems_opt.x or \
                    ems.x == ems_opt.x and ems.y < ems_opt.y or \
                    ems.x == ems_opt.x and ems.y == ems_opt.y and ems.z < ems_opt.z:
                #print("---EMS {}x{}x{}".format(ems.width, ems.depth, ems.height))
                ems_opt = ems

    print("--Opt ems {} for box {}".format(ems_opt, box))
    return ems_opt
