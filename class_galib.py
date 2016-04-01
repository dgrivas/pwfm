# coding=utf-8
# import random
from __future__ import print_function
from class_db import *
from math import *


CROSSOVER_ENGINEERS = 4
CROSSOVER_JOBS = 2

########################################################################################################################
class GeAl:
    """
    Main Genetic Algorithm Methods.

    """
    # Class variables:
    _db = None
    _pop_size = 0               # Population size
    _max_generations = 0        # Maximum generations to run GA
    _optimal_fitness = 0        # Optimal fitness to stop GA
    _pop_fitness = []           # Population fitness array (len = pop_size)
    _selection_pi = []          # Population selection probability
    _generation = None          # Current generation
    _jobid_key = []             # Job index to id array (key index)
    _engid_key = []             # Engineer index to id array (key index)
    _total_jobs_nr = 0          # Number of total jobs
    _total_engineer_nr = 0      # Number of total engineers
    _duration_dictionary = {}   # Dictionary with {job_id : job_duration}
    _jobs_data = []             # Jobs from db
    _engineers_data = []        # Engineers from db
    _travel_time = 0            # Travel time to add on each job duration

    def __init__(self, optimal, lifetime, popsize):
        self._max_generations = lifetime
        self._optimal_fitness = optimal
        self._pop_size = popsize

    def set_travel_time(self, traveltime):
        self._travel_time = traveltime

    def prepare_pop(self):
        """
        Get data:
            total jobs
            total engineers.

        Create key arrays for Job's & Engineer's id
        :return: False if no records found, True otherwise
        """

        self._pop_fitness = [0 for x in range(self._pop_size)]  # Init fitness array
        self._selection_pi = [0 for x in range(self._pop_size)]  # Init selection probability array
        self._db = DataBase()
        self._total_jobs_nr = self._db.query("Select * from job")
        self._jobs_data = self._db.fetch()
        # print self._jobs_data
        self._jobid_key = [jid[0] for jid in self._jobs_data]  # get job id for key array
        for job in self._jobs_data:
            self._duration_dictionary[job[0]] = job[2]  # get job_id:duration in dictionary
        self._total_engineer_nr = self._db.query("Select * from engineer")
        self._engineers_data = self._db.fetch()
        self._engid_key = [eid[0] for eid in self._engineers_data]  # get engineer id for key array
        if (self._total_jobs_nr and self._total_engineer_nr) == 0:
            return False
        else:
            return True

    def generate_pop(self):
        """
        Generate initial population.

        :return:
        """
        # Generate empty population
        self._generation = [Chromosome(self._total_engineer_nr, self._total_jobs_nr)
                            for x in range(self._pop_size)]
        print ("\nPopulation (size: %s):" % self._pop_size)
        for ind in range(len(self._generation)):
            for gene in range(len(self._generation[ind].assignment)):
                # get job id from index
                jid = self._jobid_key[gene]
                # select random engineer from job's CanDo list
                engineer = self._db.get_random_eng(jid)
                # set engineer for job
                self._generation[ind].assignment[gene] = engineer
                # get engineer index, increment worktime to job's duration + travel time penalty
                eng_idx = self._engid_key.index(engineer)
                duration = self._duration_dictionary[jid] + self._travel_time
                self._generation[ind].worktime[eng_idx] += duration
            print("ind: %s, assignment: %s" % (ind, self._generation[ind].assignment))
            print("         worktime  : %s" % self._generation[ind].worktime)

    def evaluate_population(self, working_time, overtime_weight):
        """
        Evaluate population fitness.

        cost = SUM(overtime) x overtime_weight + dispersion
        dispersion = SUM|x-X|/n
        :param working_time: normal working time
        :param overtime_weight: weight to multiply overtime in fitness function
        :return: max fitness (min cost)
        """
        print("\nEvaluate population:")
        for ind in range(len(self._generation)):
            self._pop_fitness[ind] = self._generation[ind].evaluate(working_time, overtime_weight)
        return min(self._pop_fitness)

    def prepare_selection(self):
        """
        Calculate selection probability.

        :param pop_rejection: population rejection percent
        :return: Individuals selected for crossover
        """
        print("\nSelection probability:")
        # prepare selection probability for population
        fitness_sum = sum(self._pop_fitness)
        x2 = 0
        for ind in range(len(self._generation)):
            x1 = float(self._pop_fitness[ind]) / float(fitness_sum)
            x2 += x1
            print("x1: %s, x2: %s" % (x1, float(x2)))
            self._selection_pi[ind] = x2
        print(self._selection_pi)

    def select(self):
        """
        select parents.

        :return list of two parents sorted by fitness
        """
        parentA = parentB = self._roulette()
        while (parentA == parentB):  # parents should be different!
            parentB = self._roulette()
        parents = (parentA, self._pop_fitness[parentA]), (parentB, self._pop_fitness[parentB])
        parents = sorted(parents, key=lambda f: f[1])  # sort parents by fitness
        # return parents
        return [x[0] for x in parents]

    def _roulette(self):
        """
        Select random individual.

        """
        r = random.random()
        for i in range(len(self._selection_pi)):
            if self._selection_pi[i] > r:
                return i

    def individuals2replace(self, inds_nr):
        """
        Identify individuals to replace on next generation (worst n individuals).

        :param inds_nr: number of individuals to replace
        :return list of individuals to replace
        """
        return self._index_sort(self._pop_fitness, inds_nr)
        # inds = [(ind, self._pop_fitness[ind]) for ind in range(self._pop_size)]
        # print(inds)
        # inds = sorted(inds, key=lambda f: f[1], reverse=True)  # sort individuals by fitness
        # print(inds)
        # return [x[0] for x in inds[:inds_nr]]

    def crossover(self, father, mother, offspring):
        # TODO: 'crossover' method
        '''
        Crossover father & mother, generate offspring.

        CROSSOVER_ENGINEERS = 4
        CROSSOVER_JOBS = 4

        Από τον γονέα Α, θα επιλέγονται οι n τεχνικοί με το μεγαλύτερο worktime. Από
αυτούς θα επιλέγονται x εργασίες, οι οποίες θα αφαιρούνται και θα ανατίθενται σε άλλον
τεχνικό του γονέα Α. Η επιλογή του τεχνικού θα γίνεται με βάση τις αναθέσεις που
υπάρχουν στον γονέα Β. Το νέο χρωμόσωμα που θα προκύπτει με τις αλλαγές στις
αναθέσεις θα περνά στην επόμενη γενιά.
        '''
        print("father:%s, mother:%s, kid:%s" % (father, mother, offspring))

        # father will become offspring after crossover:
        offspring_assignment = [x for x in self._generation[father].assignment]
        offspring_worktime = [0 for x in range(self._total_engineer_nr)]

        # Get CROSSOVER_ENGINEERS with highest worktime from father:
        engineers = self._index_sort(offspring_worktime, top=CROSSOVER_ENGINEERS)
        print("\tengs: %s" % engineers)
        engineers = [self._engid_key[x] for x in engineers]  # get engineer id from index
        print("\tengs(id): %s" % engineers)

        # Select CROSSOVER_JOBS for chosen engineers from father & replace assignments according to mother's
        for eng in engineers:
            # get jobs index for engineer (eng)
            jobs = [x[0] for x in filter(lambda (i,e): e == eng, enumerate(offspring_assignment))]
            # print("jobs1:%s" % jobs)
            # get random CROSSOVER_JOBS jobs
            k = min(CROSSOVER_JOBS, len(jobs))
            jobs = random.sample(jobs,k)
            print("jobs:%s" % jobs)
            # Replace job assignments according to mother's assignments:
            for job in jobs:
                offspring_assignment[job] = self._generation[mother].assignment[job]

        # Update worktime
        for job, eng in enumerate(offspring_assignment):
            duration = self._duration_dictionary[self._jobid_key[job]] + self._travel_time
            offspring_worktime[self._engid_key.index(eng)] += duration
        print("new offspring_worktime: %s" % offspring_worktime)
        # print ("offspring: %s" % offspring_assignment)
        print("mother   : %s" % self._generation[mother].assignment)
        print("father   : %s" % self._generation[father].assignment)
        print("offspring: %s" % offspring_assignment)
        # Update offspring individual in generation:
        self._generation[offspring].assignment = offspring_assignment
        self._generation[offspring].worktime = offspring_worktime
        pass

    def _index_sort(self, unsorted, top, key=1, rev=True):
        """
        Sort list with index, return top values.

        # engineers = [(eng, self._generation[father].worktime[eng]) for eng in range(self._total_engineer_nr)]
        # engineers = sorted(engineers, key=lambda f: f[1], reverse=True)  # sort engineers by worktime
        # engineers = [x[0] for x in engineers[:CROSSOVER_ENGINEERS]]
        """
        sorted_list = [(i, unsorted[i]) for i in range(len(unsorted))]
        sorted_list = sorted(sorted_list, key=lambda f: f[key], reverse=rev)  # sort sorted_list by key
        sorted_list = [x[0] for x in sorted_list[:top]]
        return sorted_list

########################################################################################################################
class Chromosome:
    """
    chromosome structure definition.

    Chromosome elements: array assignment, len = No of Jobs, value = assignment to engineer
                        array worktime,    len = No of engineers, value = engineers total worktime
                        # array fitness,     len = No of engineers, value = fitness of chromosome
                        # array selection_p  len = No of engineers, value = selection probability
    """
    assignment = []
    worktime = []
    # fitness = 0
    selection_p = []

    def __init__(self, workforce, jobs):
        # Main chromosome array. Contains selected engineer for each job
        # Each position in array represents a job, indexed in Job index to id array (key index)
        self.assignment = [0 for x in range(jobs)]
        # Array to hold engineer's worktime; updated after each assignment
        self.worktime = [0 for x in range(workforce)]
        # self.fitness = [0 for x in range(workforce)]
        # self.selection_p = [0 for x in range(workforce)]

    def evaluate(self, working_time, overtime_weight):
        """
        Evaluate Chromosome fitness.

        cost = SUM(overtime) x overtime_weight + dispersion
        dispersion = SUM|x-X|/n
        :return: max fitness
        """
        eng_nr = len(self.worktime)
        mean_worktime = sum(self.worktime)/eng_nr
        dispersion = 0
        overtime = 0
        for eng in self.worktime:
            # Calculate dispersion for each engineer
            dispersion += abs(eng-mean_worktime)
            # print (abs(eng-mean_worktime),  end='-')
            print (eng,  end='-')
            # calculate overtime
            overtime += 0 if eng < working_time else eng - working_time
            # print (overtime, end=', ')
        dispersion /= eng_nr
        fitness = overtime_weight * overtime + dispersion
        print ("\tengineers: %s,\tmad: %s,\tot:%s,\tfit:%s" % (eng_nr, dispersion, overtime, fitness))
        return fitness

    def mutate(self, chromosome):
        # TODO: 'mutate' method
        pass
########################################################################################################################
