from __future__ import print_function
from class_db import *
from class_galib import *
import matplotlib.pyplot as plt

OPTIMAL_FITNESS = 70
LIFETIME = 1000  # Max GA iterations
POPSIZE = 20  # Population size
REJECTION = 0.4  # Population rejection ratio
MUTATION_PROBABILITY = 0.01  # Mutation probability
TRAVELTIME = 15
WORKING_TIME = 80
OVERTIME_WEIGHT = 1

def main():
    plot_data = []
    max_plot = []
    # Create main GA object
    ga = GeAl(OPTIMAL_FITNESS, LIFETIME, POPSIZE)

    ga.set_travel_time(TRAVELTIME)
    # Prepare data for population (get total jobs, engineers from db):
    ga.prepare_pop()
    # Generate new population of random chromosomes:
    ga.generate_pop()
    # print("Initial population ok!")
    # Evaluate population:
    max_fit = ga.evaluate_population(WORKING_TIME, OVERTIME_WEIGHT)
    # plot_data = [x for x in ga._pop_fitness]
    max_plot.append(max_fit)
    # print("max fitness for population: %s\n" % max_fit)
    # Evolutionary loop:
    for g in range(LIFETIME):
        # Selection:
        ga.prepare_selection()
        offsprings_nr = int(round(REJECTION * POPSIZE))
        offsprings = ga.individuals2replace(offsprings_nr)  # get individuals to replace
        # print("\nIndividuals to replace: %s" % offsprings)
        # Crossover:
        # print ("\nCrossover data:")
        # for i in range(len(ga._pop_fitness)):
        #     print("i: %s, fit:%s" % (i, ga._pop_fitness[i]))
        # Get parents and do crossover:
        for offspring in offsprings:
            parents = ga.select()
            # print("ind: %s, parents: %s" % (offsprings.index(offspring), parents))
            ga.crossover(parents[0], parents[1], offspring)
            pass
        # ga.print_nebula()
        ga.update_generation()

        # for x in ga._generation:
        #     print (x.assignment)
        #     print (x.worktime)

        # Mutation:
        # TODO: Mutate
        ga.apply_mutation(MUTATION_PROBABILITY)
        # Evaluate population:
        # TODO: get max fitness & mean fitness
        max_fit = ga.evaluate_population(WORKING_TIME, OVERTIME_WEIGHT)
        # ga.print_generation()
        ga.print_pop_fitness()
        max_plot.append(max_fit)
        # for x in ga._pop_fitness:
        #     plot_data.append(x)
        if max_fit < OPTIMAL_FITNESS: break
    # print (max_plot)
    print("\n\nMaximum fitness: %s, after %s life cycles" % (max_fit, g))
    plt.plot(max_plot, 'bo')
    # plt.plot(plot_data, 'bo')
    plt.show()



    # iterations = 0
'''
    while iterations != LIFETIME and solution_found != True:
        # take the pop of random chromos and rank them based on their fitness score/proximity to target output
        rankedPop = rankPop(chromos)

        print '\nCurrent iterations:', iterations

        if solution_found != True:
            # if solution is not found iterate a new population from previous ranked population
            chromos = []
            chromos = iteratePop(rankedPop)

            iterations += 1
        else:
            break
'''

if __name__ == "__main__":
    main()
