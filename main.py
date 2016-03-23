#from __future__ import print_function
from db import *
from galib import *

OPTIMAL_FITNESS = 100
LIFETIME = 100  # max GA iterations
POPSIZE = 20  # population size

def main():
    # Create main GA object
    ga = GeAl(OPTIMAL_FITNESS, LIFETIME, POPSIZE)

    ga.prepare_pop()   # get total jobs, engineers from db
    ga.generate_pop()  # generate new population of random chromosomes
    # print ga._generation

    print("Initial population ok!")

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
