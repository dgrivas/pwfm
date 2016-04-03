from __future__ import print_function
from class_galib import *
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.size'] = 10.0

OPTIMAL_FITNESS = 75
LIFETIME = 300  # Max GA iterations
POPSIZE = 20  # Population size
REJECTION = 0.2  # Population rejection ratio
MUTATION_PROBABILITY = 0.15  # Mutation probability
TRAVELTIME = 15
WORKING_TIME = 80
OVERTIME_WEIGHT = 1.5

pop_fit = []
optimum_fit = []
mean_fit = []


def main():
    # Create main GA object
    ga = GeAl(OPTIMAL_FITNESS, LIFETIME, POPSIZE, TRAVELTIME)
    # ga.set_travel_time(TRAVELTIME)
    #
    # Prepare data for population (get total jobs, engineers from db):
    ga.prepare_pop()
    # Generate new population of random chromosomes:
    ga.generate_pop()
    #
    # Evaluate population:
    (fitness, assignment, worktime) = ga.evaluate_population(WORKING_TIME, OVERTIME_WEIGHT)
    update_plot_data(ga, fitness)
    #
    # Evolution loop:
    for g in range(LIFETIME):
        # TODO: check improvement
        if fitness < OPTIMAL_FITNESS:
            g -= 1
            break
        #
        # Selection:
        ga.prepare_selection()  # prepare cumulative probability list
        offsprings_nr = int(round(REJECTION * POPSIZE))
        offsprings = ga.individuals2replace(offsprings_nr)  # get individuals to replace
        # print("\nIndividuals to replace: %s" % offsprings)
        #
        # Crossover:
        # Get parents and do crossover:
        for offspring in offsprings:
            parents = ga.select()
            # print("kid: %s, parents: %s" % (offspring, parents))
            ga.crossover(parents[0], parents[1], offspring, update_wt=False)
            pass
        # ga.print_nebula()
        #
        # Mutation:
        ga.apply_mutation(MUTATION_PROBABILITY, newborn=True)
        #
        # Integrate offsprings into next generation, update worktime:
        ga.update_generation()
        #
        # Clear nebula for next generation
        ga.clear_nebula()
        #
        # Evaluate population:
        (fitness, assignment, worktime) = ga.evaluate_population(WORKING_TIME, OVERTIME_WEIGHT)
        update_plot_data(ga, fitness)
        pass
    # Print optimum solution
    print("\n\nOptimum fitness, after %s life cycles: %s" % (fitness, g+1))
    print("\nOptimum solution:\nAssigment:\n%s\nEngineer Worktime:\n%s" % (assignment, worktime))
    #
    plot_result(pop_fit, mean_fit, optimum_fit)


def update_plot_data(ga, fitness):
    """
    Update plot data.

    :param ga: GA object
    :param fitness: best fitness of generation
    :return:
    """
    pop_fit.append(ga._pop_fitness[:])  # Collect generation fitness for diagram
    optimum_fit.append(fitness)    # Collect max fitness data for diagram
    mean_fit.append(sum(ga._pop_fitness)/len(ga._pop_fitness))  # Calculate mean fitness


def plot_result(population, mean, best):
    """
    Plot GA data.

    :param population:
    :param mean:
    :param best:
    :return:
    """
    fig = plt.figure()
    #
    # lineoffsets2 sets the increment between each data set
    colors = [[0, 0, 0]]
    lineoffsets = 1
    linelengths = 0.5
    #
    # create vertical population fitness plot
    pf = fig.add_subplot(211)
    pf.set_xlim(0, len(population))
    pf.eventplot(population, colors=colors, lineoffsets=lineoffsets,
                  linelengths=linelengths, orientation='vertical')
    # Plot mean fitness
    pf.plot(mean, label='Mean Fitness')
    pf.legend(loc='best', fancybox=True, framealpha=0.5)
    pf.set_ylabel('Fitness')
    pf.set_xlabel('Generations')
    pf.set_title('Population Fitness Evolution', fontweight='bold', fontsize=12)
    #
    # Create best fitness plot
    textstr = 'Best fitness: %s' % min(best)
    bf = fig.add_subplot(212)
    bf.set_xlim(0, len(population))
    bf.set_ylabel('Fitness')
    bf.set_xlabel('Generations')
    bf.set_title('Best Fitness', fontweight='bold', fontsize=12)
    # place a text box in upper left in axes coords
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    bf.text(0.95, 0.95, textstr, transform=bf.transAxes, fontsize=10,
        va='top', ha='right',  bbox=props)
    bf.plot(best)
    #
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
