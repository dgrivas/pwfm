# import random
from __future__ import print_function
from class_db import *
from math import *

WORKTIME = 420
TRAVELTIME = 15

"""
    def randint(self, a, b):
        ""Return random integer in range [a, b], including both end points.
        ""

    def choice(self, seq):
        ""Choose a random element from a non-empty sequence.""

    def shuffle(self, x, random=None):
        ""x, random=random.random -> shuffle list x in place; return None.
        Optional arg random is a 0-argument function returning a random
        float in [0.0, 1.0); by default, the standard random.random.
        ""

    def sample(self, population, k):
        ""Chooses k unique random elements from a population sequence.

        Returns a new list containing elements from the population while
        leaving the original population unchanged.  The resulting list is
        in selection order so that all sub-slices will also be valid random
        samples.  This allows raffle winners (the sample) to be partitioned
        into grand prize and second place winners (the subslices).

        Members of the population need not be hashable or unique.  If the
        population contains repeats, then each occurrence is a possible
        selection in the sample.

        To choose a sample in a range of integers, use xrange as an argument.
        This is especially fast and space efficient for sampling from a
        large population:   sample(xrange(10000000), 60)
        ""

    def normalvariate(self, mu, sigma):
        ""Normal distribution.

        mu is the mean, and sigma is the standard deviation.
        ""

    def gauss(self, mu, sigma):
        ""Gaussian distribution.

        mu is the mean, and sigma is the standard deviation.  This is
        slightly faster than the normalvariate() function.

        Not thread-safe without a lock around calls.
        ""
"""

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
    _generation = None          # Current generation
    _jobid_key = []             # Job index to id array (key index)
    _engid_key = []             # Engineer index to id array (key index)
    _total_jobs_nr = 0          # Number of total jobs
    _total_engineer_nr = 0      # Number of total engineers
    _duration_dictionary = {}   # Dictionary with {job_id : job_duration}
    _jobs_data = []             # Jobs from db
    _engineers_data = []        # Engineers from db

    def __init__(self, optimal, lifetime, popsize):
        self._max_generations = lifetime
        self._optimal_fitness = optimal
        self._pop_size = popsize

    def prepare_pop(self):
        """
        Get data:
            total jobs
            total engineers.

        Create key arrays for Job's & Engineer's id
        :return: False if no records found, True otherwise
        """

        self._pop_fitness = [0 for x in range(self._pop_size)]  # Init fitness array
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
        print ("Population size: %s" % self._pop_size)
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
                duration = self._duration_dictionary[jid] + TRAVELTIME
                self._generation[ind].worktime[eng_idx] += duration
            print("ind: %s, assignment: %s" % (ind, self._generation[ind].assignment))
            print("         worktime  : %s" % self._generation[ind].worktime)


    def selection(self, pop_rejection):
        """

        :param pop_rejection: population rejection percent
        :return:
        """
        pass

    def evaluate(self, working_time=80, overtime_weight=1):
        """
        Evaluate population fitness.

        cost = SUM(overtime) x overtime_weight + dispersion
        dispersion = SUM|x-X|/n
        :return: max fitness
        """
        # overtime = []
        mean_worktime = 0

        # _pop_fitness

        for ind in range(len(self._generation)):
            self._generation[ind].evaluate(working_time, overtime_weight)
            '''
            mean_worktime = sum(self._generation[ind].worktime)/self._total_engineer_nr
            dispersion = 0
            overtime = 0
            print ("ind: %s, mean wt: %s, swift:%s" % (ind, mean_worktime, working_time), end='\t')
            for eng in self._generation[ind].worktime:
                # Calculate dispersion for each engineer
                dispersion += abs(eng-mean_worktime)
                # print (abs(eng-mean_worktime),  end='-')
                print (eng,  end='-')
                # calculate overtime
                overtime += 0 if eng < working_time else eng - working_time
                # print (overtime, end=', ')
            dispersion /= self._total_engineer_nr
            fitness = overtime_weight * overtime + dispersion
            print ("\tengineers: %s,\tmad: %s,\tot:%s,\tfit:%s" % (self._total_engineer_nr, dispersion, overtime,\
                                                                   fitness))
            '''

    def roulette(self, fitness_scores):
        # TODO: 'roulette' method
        pass
        '''
        index = 0
        cumalativeFitness = 0.0
        r = random.random()

        for i in range(len(fitnessScores)): # for each chromosome's fitness score
            cumalativeFitness += fitnessScores[i] # add each chromosome's fitness score to cumalative fitness

        if cumalativeFitness > r: # in the event of cumalative fitness becoming greater than r, return index of that chromo
            return i
'''
    def crossover(self, father, mother):
        # TODO: 'crossover' method
        pass

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
