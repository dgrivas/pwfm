# import random
from db import *

WORKTIME = 420

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


class GeAl:
    """
    Main Genetic Algorithm Methods.

    """
    # Class variables:
    _db = None
    _pop_size = 0               # Population size
    _max_generations = 0        # Maximum generations to run GA
    _optimal_fitness = 0        # Optimal fitness to stop GA
    _generation = None          # Current generation
    _jobid_key = []             # Job inxed to id array (key index)
    _total_jobs_nr = 0          # Number of total jobs
    _total_engineer_nr = 0      # Number of total engineers
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

        Create Job's id key array
        :return:-1 if no records found, 0 otherwise
        """

        self._db = DataBase()
        self._total_jobs_nr = self._db.query("Select * from job")
        self._jobs_data = self._db.fetch()
        self._jobid_key = [jid[0] for jid in self._jobs_data]  # get job id for key array
        # self._jobid_key = self._jobs_data[0]  # get job id for key array
        self._total_engineer_nr = self._db.query("Select * from engineer")
        self._engineers_data = self._db.fetch()
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
        # print [[x.jobs[i] for x in self._generation] for i in range(20)]
        # chromos, chromo = [], []
        # for individual in self._generation:
        #     for jid, job_assign in zip(self._jobid_key, individual.jobs):
        #         print("id: %s,\tjob_eng: %s\n" % (jid, job_assign))
        #         job_assign = self._db.get_random_eng(jid)
        #         print("Assignment: id: %s,\tjob_eng: %s\n" % (jid, job_assign))

        for ind in range(len(self._generation)):
            for gene in range(len(self._generation[ind].assignment)):
                # get job id from index
                jid = self._jobid_key[gene]
                # select random engineer from job's CanDo list
                engineer = self._db.get_random_eng(jid)
                # set engineer for job
                self._generation[ind].assignment[gene] = engineer

        print [[x.assignment[i] for x in self._generation] for i in range(20)]

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
    def crossover(self):
        # TODO: 'crossover' method
        pass


class Chromosome:
    """
    chromosome structure definition.

    Chromosome elements: array assignment, len = No of Jobs, value = assignment to engineer
                        array worktime, len = No of engineers, value = engineers total worktime
    """
    _total_duration = 0
    _total_jobs = 0

    def __init__(self, workforce, jobs):
        # Main chromosome array. Contains selected engineer for each job
        # Each position in array represents a job, indexed in Job index to id array (key index)
        self.assignment = [0 for x in range(jobs)]
        # Array to hold engineer's worktime; updated after each assignment
        self.worktime = [WORKTIME for x in range(workforce)]
        self.dummy_engineer = [self._total_jobs, self._total_duration]

    def evaluate(self):
        # TODO: 'evaluate' method
        pass

    def mutate(self):
        # TODO: 'mutate' method
        pass
