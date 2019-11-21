import random
import csv
import numpy
import itertools

import pyglet
from pyglet.gl import glClearColor, GL_DEPTH_TEST, glEnable

from Box import Box
from Palette import Palette

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

from draw.Window.Window2D import Window2D
from draw.Window.Window3D import Window3D

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


def bbl(box, empty_maximal_spaces):
    # Backk-Bottom-Left procedure

    ems_opt = empty_maximal_spaces[0]
    for ems in empty_maximal_spaces:
        #if ems.height >= 1500 or ems.width >= 1200 or ems.depth >= 800:
        #    continue
        if ems.width >= box.width and ems.depth >= box.depth and ems.height >= box.height:
            if ems.x < ems_opt.x or \
                    ems.x == ems_opt.x and ems.y < ems_opt.y or \
                    ems.x == ems_opt.x and ems.y == ems_opt.y and ems.z < ems_opt.z:
                ems_opt = ems

    return ems_opt


def difference_process(box, space):
    # Taken from "Developing a simulated annealing algorithm for the cutting stock problem" K.K.LaiJimmy W.M.Chan 1997
    # Get bottom left corner of our space and upper right corner
    x1, y1, z1 = space.llc()
    x2, y2, z2 = space.urc()
    print("--------------")
    print("Space: {}".format(space))
    print("Box: {}".format(box))
    # get bottom left corner of our box and upper right corner
    x3, y3, z3 = box.llc()
    x4, y4, z4 = box.urc()
    intervals = [
        Palette(x1, y1, z1, x3, y2, z2),
        Palette(x4, y1, z1, x2, y2, z2),
        Palette(x1, y1, z1, x2, y3, z2),
        Palette(x1, y4, z1, x2, y2, z2),
        Palette(x1, y1, z1, x2, y2, z3),
        Palette(x1, y1, z4, x2, y2, z2)
    ]
    print("Intervals before Removal: {}".format(intervals))

    # Removing intervals that are inside another interval
    for interval_a, interval_b in itertools.combinations(intervals, 2):
        x1, y1, z1 = interval_a.llc()
        x2, y2, z2 = interval_a.urc()
        x3, y3, z3 = interval_b.llc()
        x4, y4, z4 = interval_b.urc()
        if x1 >= x3 and y1 >= y3 and z1 >= z3 and x2 <= x4 and y2 <= y4 and z2 <= z4:
            print("Removing {} it overlaps with {}".format(interval_a, interval_b))
            intervals.remove(interval_a)

    # Removing "thin" intervals
    for interval in intervals:
        x1, y1, z1 = interval.llc()
        x2, y2, z2 = interval.urc()
        if x1 == x2 or y1 == y2 or z1 == z2:
            print("Removing because its thin: {}".format(interval))
            intervals.remove(interval)

    # Removing out of bound intervals
    for interval in intervals:
        x1, y1, z1 = interval.llc()
        x2, y2, z2 = interval.urc()
        print("{} {} {}".format(x2,y2,z2))
        if x2 > 1200 or y2 > 800 or z2 > 1500:
            print("removing because boundary")
            intervals.remove(interval)
    print("Intervals after Removal: {}".format(intervals))
    print("--------------")
    return intervals


def fitness(individual):
    return 0


def evalKnapsack(individual):
    weight = 0.0
    value = 0.0
    for item in individual:
        weight += items[item][0]
        value += items[item][1]
    if len(individual) > MAX_ITEM or weight > MAX_WEIGHT:
        return 10000, 0  # Ensure overweighted bags are dominated
    return weight, value


def cxSet(ind1, ind2):
    """Apply a crossover operation on input sets. The first child is the
    intersection of the two sets, the second child is the difference of the
    two sets.
    """
    temp = set(ind1)  # Used in order to keep type
    ind1 &= ind2  # Intersection (inplace)
    ind2 ^= temp  # Symmetric Difference (inplace)
    return ind1, ind2


def mutSet(individual):
    """Mutation that pops or add an element."""
    if random.random() < 0.5:
        if len(individual) > 0:  # We cannot pop from an empty set
            individual.remove(random.choice(sorted(tuple(individual))))
    else:
        individual.add(random.randrange(NBR_ITEMS))
    return individual,


# toolbox.register("evaluate", evalKnapsack)
# toolbox.register("mate", cxSet)
# toolbox.register("mutate", mutSet)
# toolbox.register("select", tools.selNSGA2)


def main():
    random.seed(64)
    NGEN = 50
    MU = 50
    LAMBDA = 100
    CXPB = 0.7
    MUTPB = 0.2

    pop = toolbox.population(n=MU)
    hof = tools.ParetoFront()
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean, axis=0)
    stats.register("std", numpy.std, axis=0)
    stats.register("min", numpy.min, axis=0)
    stats.register("max", numpy.max, axis=0)

    algorithms.eaMuPlusLambda(pop, toolbox, MU, LAMBDA, CXPB, MUTPB, NGEN, stats,
                              halloffame=hof)

    return pop, stats, hof


if __name__ == "__main__":

    palette = Box(0, 0, 0, 1200, 800, 1500)

    # Reading in products and storing them into the item variable
    items = []
    with open("resources/Maße_aldi.csv") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=";")
        for row in csv_reader:
            for i in row['Quantity']:
                width = int(row['Width'])
                height = int(row['Height'])
                depth = int(row['Depth'])
                weight = 5
                items.append(Box(0, 0, 0, width, depth, height))
    # init empty palette
    emss = [Palette(0, 0, 0, 1200, 800, 1500)]  # Empty bin Maximal Space
    # items[0].place(opt_ems.x, opt_ems.y, opt_ems.z)
    for item in items:
        opt_ems = bbl(item, emss)
        item.place(opt_ems.x, opt_ems.y, opt_ems.z)
        emss.remove(opt_ems)
        new_emss = difference_process(item, opt_ems)
        emss += new_emss
    window3d = Window3D(items, width, depth, height, width=854, height=480, caption='Palettierung', resizable=True)
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
