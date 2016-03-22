import random
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
    Main Genetic Algorithm Methods
    """
    _pop_size = 0
    _max_generations = 0
    _optimal_fitness = 0
    _generation = None
    _total_jobs_nr = 0
    _total_engineer_nr = 0
    _jobs_data = []
    _engineers_data = []

    def __init__(self, optimal, lifetime, popsize):
        self._max_generations = lifetime
        self._optimal_fitness = optimal
        self._pop_size = popsize


    def prepare_pop(self):
        """
        Get data:
            total jobs
            total engineers
        :return:-1 if no records found, 0 otherwise
        """
        pass
        '''
        db = DataBase()
        self._total_jobs_nr = db.query("Select * from jobs")
        self._jobs_data = db.fetch()
        self._total_engineer_nr = db.query("Select * from engineers")
        self._engineers_data = db.fetch()
        if (self._total_jobs_nr and self._total_engineer_nr) == 0:
            return -1
        else:
            return 0
        '''


    def generate_pop(self):
        """
        Generate initial population
        :return:
        """
        # Generate empty population
        self._generation = [Chromosome(self._total_engineer_nr, self._total_jobs_nr)
                            for x in range(self._pop_size)]
        generation = self._generation

        chromos, chromo = [], []
        for individual in generation:
            for job in individual.jobs:

        '''
        chromos, chromo = [], []
        for each_individual in generation[].

        for eachChromo in range(self._pop_size):
            chromo = []
        for bit in range(genesPerCh * 4):
            chromo.append(random.randint(0,1))
            chromos.append(chromo)
        return chromos
        '''

    def roulette(self, fitness_scores):
        #TODO: 'roulette' method
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
        #TODO: 'crossover' method
        pass


class Chromosome:
    """
    chromosome structure definition
    """
    _total_duration = 0
    _total_jobs = 0

    def __init__(self, workforce, jobs):
        self.jobs = [0 for x in range(jobs)]
        self.engineers = [WORKTIME for x in range(workforce)]
        self.dummy_engineer = [self._total_jobs, self._total_duration]

    def evaluate(self):
        #TODO: 'evaluate' method
        pass

    def mutate(self):
        #TODO: 'mutate' method
        pass
