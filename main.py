#from __future__ import print_function
from class_db import *
from class_galib import *

OPTIMAL_FITNESS = 100
LIFETIME = 100  # max GA iterations
POPSIZE = 20  # population size

def main():
    # Create main GA object
    ga = GeAl(OPTIMAL_FITNESS, LIFETIME, POPSIZE)

    ga.prepare_pop()   # get total jobs, engineers from db
    ga.generate_pop()  # generate new population of random chromosomes
    print("Initial population ok!")
    max_fit = ga.evaluate()
    print("max fitness for population: %s\n" % max_fit)
    ga.selection()
    # TODO: Calculate population rejection ratio to get nr of offsprings
    # TODO: loop 'offspring' times to get parents from ga.selection
    # TODO:   and call crossover


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
