from __future__ import print_function
from class_db import *
from class_galib import *

OPTIMAL_FITNESS = 100
LIFETIME = 100  # max GA iterations
POPSIZE = 20  # population size
REJECTION = 0.4  # population rejection ratio
TRAVELTIME = 15
WORKING_TIME = 80
OVERTIME_WEIGHT = 1

def main():
    # Create main GA object
    ga = GeAl(OPTIMAL_FITNESS, LIFETIME, POPSIZE)

    ga.set_travel_time(TRAVELTIME)
    ga.prepare_pop()   # get total jobs, engineers from db
    ga.generate_pop()  # generate new population of random chromosomes
    print("Initial population ok!")
    max_fit = ga.evaluate_population(WORKING_TIME, OVERTIME_WEIGHT)
    print("max fitness for population: %s\n" % max_fit)
    ga.prepare_selection()
    offsprings_nr = int(round(REJECTION * POPSIZE))
    offsprings = ga.individuals2replace(offsprings_nr)  # get individuals to replace
    print("\nIndividuals to replace: %s" % offsprings)
    print ("\nCrossover data:")
    # for i in range(len(ga._pop_fitness)):
    #     print("i: %s, fit:%s" % (i, ga._pop_fitness[i]))
    # Get parents and do crossover:
    for offspring in offsprings:
        parents = ga.select()
        # print("ind: %s, parents: %s" % (offsprings.index(offspring), parents))
        ga.crossover(parents[0], parents[1], offspring)
        pass

    for x in ga._generation:
        print (x.assignment)
        print (x.worktime)

    # TODO: Mutate



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
