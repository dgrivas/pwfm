from __future__ import print_function
from class_galib import *
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.size'] = 8.0

OPTIMAL_FITNESS = 70
LIFETIME = 300  # Max GA iterations
POPSIZE = 20  # Population size
REJECTION = 0.1  # Population rejection ratio
MUTATION_PROBABILITY = 0.1  # Mutation probability
TRAVELTIME = 15
WORKING_TIME = 80
OVERTIME_WEIGHT = 1.5

# TODO: return best chromosome at the end
# TODO: mutate only offsprings
def main():
    pop_fit = []
    max_fit = []
    mean_fit = []
    # Create main GA object
    ga = GeAl(OPTIMAL_FITNESS, LIFETIME, POPSIZE)
    ga.set_travel_time(TRAVELTIME)

    # Prepare data for population (get total jobs, engineers from db):
    ga.prepare_pop()
    # Generate new population of random chromosomes:
    ga.generate_pop()
    # print("Initial population ok!")

    # Evaluate population:
    best_fitness = ga.evaluate_population(WORKING_TIME, OVERTIME_WEIGHT)
    # pop_fit = [x for x in ga._pop_fitness]
    pop_fit.append(ga._pop_fitness[:])
    max_fit.append(best_fitness)
    mean_fit.append(sum(ga._pop_fitness)/len(ga._pop_fitness))

    # Evolution loop:
    for g in range(LIFETIME):
        # TODO: check improvement
        if best_fitness < OPTIMAL_FITNESS:
            g -= 1
            break
        #
        # Selection:
        ga.prepare_selection()
        offsprings_nr = int(round(REJECTION * POPSIZE))
        offsprings = ga.individuals2replace(offsprings_nr)  # get individuals to replace
        # print("\nIndividuals to replace: %s" % offsprings)
        #
        # Crossover:
        # print ("\nCrossover data:")
        # for i in range(len(ga._pop_fitness)):
        #     print("i: %s, fit:%s" % (i, ga._pop_fitness[i]))
        # Get parents and do crossover:
        for offspring in offsprings:
            parents = ga.select()
            # print("ind: %s, parents: %s" % (offsprings.index(offspring), parents))
            ga.crossover(parents[0], parents[1], offspring)
        # ga.print_nebula()

        # Mutation:
        ga.apply_mutation(MUTATION_PROBABILITY)

        # Integrate offsprings into next generation:
        ga.update_generation()

        # Evaluate population:
        # TODO: get max fitness & mean fitness
        best_fitness = ga.evaluate_population(WORKING_TIME, OVERTIME_WEIGHT)
        max_fit.append(best_fitness)    # Collect max fitness data for diagram
        pop_fit.append(ga._pop_fitness[:]) # Collect generation fitness for diagram
        mean_fit.append(sum(ga._pop_fitness)/len(ga._pop_fitness))
        # ga.print_generation()
        # ga.print_pop_fitness()
        pass
    # print (pop_fit)
    print("\n\nMaximum fitness: %s, after %s life cycles" % (best_fitness, g))
    plot_result(pop_fit, mean_fit, max_fit)


def plot_result(population, mean, best):

    fig = plt.figure()

    # use individual values for the parameters this time
    # these values will be used for all data sets (except lineoffsets2, which
    # sets the increment between each data set in this usage)
    colors = [[0, 0, 0]]
    lineoffsets = 1
    linelengths = 0.5

    # create a horizontal plot
    #ax1 = fig.add_subplot(211)
    #ax1.eventplot(data2, colors=colors2, lineoffsets=lineoffsets2,
    #              linelengths=linelengths2)

    # create a vertical plot
    ax1 = fig.add_subplot(211)
    ax1.eventplot(population, colors=colors, lineoffsets=lineoffsets,
                  linelengths=linelengths, orientation='vertical')
    ax1.plot(mean)

    ax2 = fig.add_subplot(212)
    ax2.plot(best)

    # ax3 = fig.add_subplot(212)
    # ax3.vlines(range(len(best)), [0], best)

    plt.show()

    # iterations = 0


if __name__ == "__main__":
    main()
