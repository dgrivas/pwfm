# coding=utf-8
#!/usr/bin/env python
from __future__ import print_function
from class_galib import *
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.size'] = 10.0
import timeit
import os
import sys

MUTATION_DECREASE = 0.001   # Mutation reduction value
MUTATION_ADAPT_POINT = 0.3    # Mutation correction start (percent of generations)
FINAL_MUTATION = 0.001
CROSSOVER_ENGINEERS = 0.4
CROSSOVER_JOBS = 0.3


pop_fit = []
optimum_fit = []
mean_fit = []


def main():
    # Get parameters from menu:
    optimal_fitness, lifetime, popsize, rejection, mutation_probability, \
           traveltime, surplus_weight, overtime_weight = main_menu()

    print("Initializing...", end='\r')
    sys.stdout.flush()

    # Initialize timer
    start = timeit.default_timer()

    # Create main GA object
    ga = GeAl(optimal_fitness, lifetime, popsize, traveltime)
    # ga.set_travel_time(TRAVELTIME)
    #
    # Prepare data for population (get total jobs, engineers from db):
    ga.prepare_pop(CROSSOVER_ENGINEERS, CROSSOVER_JOBS)
    # Generate new population of random chromosomes:
    ga.generate_pop()
    #
    # Evaluate population:
    (fitness, assignment, worktime, surplus, overtime, dispersion) = \
        ga.evaluate_population(surplus_weight, overtime_weight)
    update_plot_data(ga, fitness)
    #
    # Evolution loop:
    for g in range(lifetime):
        print("Evolution: %s" % g, end='\r')
        sys.stdout.flush()
        if fitness < optimal_fitness:
            g -= 1
            break
        #
        # Selection:
        ga.prepare_selection()  # prepare cumulative probability list
        offsprings_nr = int(round(rejection * popsize))
        offsprings = ga.individuals2replace(offsprings_nr)  # get individuals to replace
        # print("\nIndividuals to replace: %s" % offsprings)
        #
        # Crossover:
        # Get parents and do crossover:
        for offspring in offsprings:
            parents = ga.select()
            # print("kid: %s, parents: %s" % (offspring, parents))
            ga.crossover(parents[0], parents[1], offspring)
            pass
        # ga.print_nebula()
        #
        # Mutation:
        ga.apply_mutation(mutation_probability, newborn=True)
        # Mutation correction
        if g > (MUTATION_ADAPT_POINT * lifetime):
            mutation_probability = max(mutation_probability - MUTATION_DECREASE, FINAL_MUTATION)
        print("%s, %s" % (g, mutation_probability))
        #
        # Integrate offsprings into next generation, update worktime:
        ga.update_generation()
        #
        # Clear nebula for next generation
        ga.clear_nebula()
        #
        # Evaluate population:
        (fitness, assignment, worktime, surplus, overtime, dispersion) = \
            ga.evaluate_population(surplus_weight, overtime_weight)
        # (fitness, assignment, worktime) = ga.evaluate_population(WORKING_TIME, OVERTIME_WEIGHT)
        update_plot_data(ga, fitness)
        pass
    # Print optimum solution
    stop = timeit.default_timer()
    runtime = round(stop - start, 2)
    print("\n\nRuntime: %ssec" % runtime)
    print("Optimum fitness: %s, after %s life cycles" % (fitness, g+1))
    print("Mean worktime: %smin" % (sum(worktime)/len(worktime)))
    print("Optimum solution:\nAssigment:\n%s\nEngineer Worktime:\n%s" % (assignment, worktime))
    #
    plot_result(pop_fit, mean_fit, optimum_fit, surplus, overtime, dispersion, runtime)


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


def plot_result(population, mean, best, surplus, overtime, dispersion, runtime):
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
    textstr = 'Best fitness: %s\nSurplus: %smin\nOvertime: %smin\nDispersion: %s\nRuntime: %ssec' % \
              (min(best), surplus, overtime, dispersion, runtime)

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

def main_menu():
    optimal_fitness = 16
    lifetime = 200  # Max GA iterations
    popsize = 40  # Population size
    rejection = 0.4  # Population rejection ratio
    mutation_probability = 0.06  # Mutation probability
    traveltime = 15
    surplus_weight = 1.0
    overtime_weight = 2.0
    while True:
        os.system('clear')
        print (70 * '-')
        print ("     Π Α Ρ Α Μ Ε Τ Ρ Ο Ι   Γ Ε Ν Ε Τ Ι Κ Ο Υ   Α Λ Γ Ο Ρ Ι Θ Μ Ο Υ")
        print (70 * '-')
        print("\n\t[1]  Optimal Fitness (%s)"
              "\n\t[2]  Lifetime (%s)"
              "\n\t[3]  Population Size (%s)"
              "\n\t[4]  Mutation Probability (%s)"
              "\n\t[5]  Rejection Ratio (%s)"
              "\n\t[6]  Travel Time (%s)"
              "\n\t[7]  Surplus Weight (%s)"
              "\n\t[8]  Overtime Weight (%s)"
              "\n\n\t[0]  Εκτέλεση αλγορίθμου" % (optimal_fitness, lifetime, popsize, mutation_probability, rejection,
                                                  traveltime, surplus_weight, overtime_weight))
        try:
            selection = raw_input("\nΕπιλέξτε παράμετρο: ")
            if selection =='1':
                optimal_fitness = int(raw_input("Optimal Fitness: "))
            elif selection == '2':
              lifetime = int(raw_input("Lifetime: "))
            elif selection == '3':
              popsize = int(raw_input("Population Size: "))
            elif selection == '4':
              mutation_probability = float(raw_input("Mutation Probability: "))
            elif selection == '5':
              rejection = float(raw_input("Rejection Ratio: "))
            elif selection == '6':
              traveltime = int(raw_input("Travel Time: "))
            elif selection == '7':
              surplus_weight = float(raw_input("Surplus Weight: "))
            elif selection == '8':
              overtime_weight = float(raw_input("Overtime Weight: "))
            elif selection == '0':
                print("\n\n...Ο αλγόριθμος εκτελείται... Παρακαλώ περιμένετε!!!")
                break
            else:
              print("Άγνωστη επιλογή!")
        except ValueError:
            print("Oops!  That was no valid number.  Try again...")
    return optimal_fitness, lifetime, popsize, rejection, mutation_probability, \
           traveltime, surplus_weight, overtime_weight


if __name__ == "__main__":
    main()
