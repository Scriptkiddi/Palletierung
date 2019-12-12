import random
from copy import deepcopy

import numpy
from deap import base, algorithms
from deap import creator
from deap import tools
from scoop import futures

from placement.placement import placement

toolbox = base.Toolbox()


def random_list(length):
    random_numbers = []
    for i in range(0, length):
        random_numbers.append(random.uniform(0, 1))
    return random_numbers


def eval_palette(individual, boxes):
    # Deepcopy boxes otherwise eval changes all boxes
    boxes = deepcopy(boxes)
    # get box types out of boxes
    box_types = list(set(map(lambda box: box.get_type(), boxes)))
    # We diverge from the classic algorithm since we want to always place each product next to each other
    # So instead of having len(boxes) genes we only have len(box_types)
    # genes so we only swap stacking order of each box type
    random_keys = individual[0:len(box_types)]
    btps_unsorted = map(lambda x: (x, box_types[random_keys.index(x)]), random_keys)
    btps = sorted(btps_unsorted, key=lambda x: x[0])
    # For each box_type we get the boxes and do a flatten on the resulting list of lists
    boxes_to_pack = [item for sublist in list(map(lambda x: x[1].boxes, btps)) for item in sublist]

    vector_layer_types = individual[len(box_types):]
    future = futures.submit(placement, boxes_to_pack, vector_layer_types)
    boxes_packed = future.result()
    # print(len(boxes_packed))
    number_of_boxes_packed = 0
    maximal_height = 0
    for layer in boxes_packed:
        number_of_boxes_packed += layer.quantity
        # maximal_height += layer.urc()[2]

        # if maximal_height < layer.urc()[2]:
        #    maximal_height = layer.urc()[2]

    fitness = number_of_boxes_packed * 2 - maximal_height

    return fitness,


def cxSet(ind1, ind2):
    for i in range(len(ind1)):
        decision = random.uniform(0, 1)
        if decision > 0.7:
            ind1[i] = ind2[i]
    return ind1, ind2


def mutSet(individual):
    return toolbox.individual(),


# toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=IND_SIZE)

def run_genetics(boxes_to_pack, box_types):
    # To assure reproductibility, the RNG seed is set prior to the items
    # dict initialization. It is also seeded in main().
    random.seed(64)
    IND_SIZE = len(box_types) + len(boxes_to_pack)

    # Creating Fitness Class, and set the Objective to maximize
    creator.create("Fitness", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.Fitness)
    # toolbox.register("attr_float", random.uniform, 0, 1)
    toolbox.register("indices", random_list, IND_SIZE)
    toolbox.register("individual", tools.initIterate, creator.Individual,
                     toolbox.indices)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("select", tools.selBest)
    toolbox.register("evaluate", eval_palette, boxes=boxes_to_pack)
    toolbox.register("mate", cxSet)
    toolbox.register("mutate", mutSet)

    NGEN = 10
    MU = 50 # * len(boxes_to_pack)
    LAMBDA = 100
    CXPB = 0.7
    MUTPB = 0.2

    pop = toolbox.population(n=MU)
    hof = tools.HallOfFame(3)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean, axis=0)
    stats.register("std", numpy.std, axis=0)
    stats.register("min", numpy.min, axis=0)
    stats.register("max", numpy.max, axis=0)

    algorithms.eaMuPlusLambda(pop, toolbox, MU, LAMBDA, CXPB, MUTPB, NGEN, stats,
                              halloffame=hof)

    print(hof)
    return pop, stats, hof
