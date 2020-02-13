import random
from copy import deepcopy

import numpy
from deap import base, algorithms
from deap import creator
from deap import tools
from scoop import futures

from placement.placement import placement
import configparser

toolbox = base.Toolbox()
toolbox.register("map", futures.map)
creator.create("Fitness", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.Fitness)
config = configparser.ConfigParser()
config.read("config.ini")

palette_width = int(config["palette"]["width"])
palette_depth = int(config["palette"]["depth"])
palette_height = int(config["palette"]["height"])
palette_max_weight = int(config["palette"]["weight"])
CXPB = float(config["genetics"]["CXPB"])
MUTPB = float(config["genetics"]["MUTPB"])
MUTGPB = float(config["genetics"]["MUTGPB"])
elitist_percentage = float(config["genetics"]["elitist_size"])
bottom_percentage = float(config["genetics"]["bottom_size"])
break_std = float(config["genetics"]["break_std"])


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
    boxes_packed, emss = placement(boxes_to_pack, vector_layer_types)
    volume_used = 0

    palette_weight = 0
    for layer in boxes_packed:
        volume_used += layer.width * layer.height * layer.depth
        palette_weight = layer.quantity*layer.boxes[0].weight
    overloaded = 0
    if palette_weight > palette_max_weight:
        overloaded = -999999999999999999999

    volume_ratio = volume_used / (palette_width * palette_depth * palette_height)

    fitness = volume_ratio + overloaded
    return fitness,


def mutate(ind):
    for i, value in enumerate(ind):
        if random.random() < MUTGPB:
            ind[i] = random.random()
    return ind


def run_genetics(boxes_to_pack, box_types, ngen, size_of_population):
    """
    Runs genetic process
    can be stopped early by adjusting break std in the config

    :param boxes_to_pack: list of boxes to pack
    :param box_types: list of box types
    :param ngen: number of generations
    :param size_of_population: population size
    :return: returns the final population
    """
    IND_SIZE = len(box_types) + len(boxes_to_pack)

    # Creating Fitness Class, and set the Objective to maximize
    # toolbox.register("attr_float", random.uniform, 0, 1)
    toolbox.register("indices", random_list, IND_SIZE)
    toolbox.register("individual", tools.initIterate, creator.Individual,
                     toolbox.indices)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", eval_palette, boxes=boxes_to_pack)
    toolbox.register("mutate", mutate)
    elitist_size = int(elitist_percentage * size_of_population)
    bottom_size = int(bottom_percentage * size_of_population)

    pop = toolbox.population(n=size_of_population)
    hof = tools.HallOfFame(3)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean, axis=0)
    stats.register("std", numpy.std, axis=0)
    stats.register("min", numpy.min, axis=0)
    stats.register("max", numpy.max, axis=0)

    for g in range(ngen):
        # Select the next generation individuals
        # Select complete generation
        offspring = tools.selBest(pop, len(pop))
        # Clone the selected individuals so we can modify them
        offspring = list(map(toolbox.clone, offspring))
        # Select best 15% of the old generation
        elitist = tools.selBest(pop, elitist_size)
        # Apply crossover on the offspring between the new generation and
        # the best 15% of the old generation
        for ind in offspring:
            elite = elitist[random.randint(0, len(elitist) - 1)]
            for i in range(len(ind)):
                if random.random() < CXPB:
                    ind[i] = elite[i]
                del ind.fitness.values

        # Apply mutation on the offspring
        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values
        # Generate 15% of the population size new to introduce more choices
        bottom = toolbox.population(bottom_size)
        offspring = offspring + bottom

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        pop[:] = tools.selBest(pop + offspring, size_of_population)
        hof.update(pop)

        record = stats.compile(pop)
        if record['std'] < break_std:
            break

    futures.shutdown(True)
    return pop, stats, hof
