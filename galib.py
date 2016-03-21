import random
from db import *

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
        self._generation = [Chromosome() for x in range(popsize)]


    def prepare_pop(self):
        """
        Get data:
            total jobs
            total engineers
        :return:-1 if no records found, 0 otherwise
        """
        db = DataBase()

        self._total_jobs_nr = db.query("Select * from jobs")
        self._jobs_data = db.fetch()

        self._total_engineer_nr = db.query("Select * from engineers")
        self._engineers_data = db.fetch()

        if (self._total_jobs_nr and self._total_engineer_nr) == 0:
            return -1
        else:
            return 0

    def generate_pop(self):
        chromos, chromo = [], []
        for each_individual in

        for eachChromo in range(self._pop_size):
            chromo = []
        for bit in range(genesPerCh * 4):
            chromo.append(random.randint(0,1))
            chromos.append(chromo)
        return chromos

    def roulette(self, fitness_scores):
        index = 0
        cumalativeFitness = 0.0
        r = random.random()

        for i in range(len(fitnessScores)): # for each chromosome's fitness score
            cumalativeFitness += fitnessScores[i] # add each chromosome's fitness score to cumalative fitness

        if cumalativeFitness > r: # in the event of cumalative fitness becoming greater than r, return index of that chromo
            return i

    def crossover(self):
        pass


class Chromosome:
    """
    chromosome structure definition
    """
    _total_duration = 0
    _total_jobs = 0

    def __init__(self, workforce, jobs):
        self.jobs = [0 for x in range(jobs)]
        self.engineers = [0 for x in range(workforce)]
        self.dummy_engineer = [self._total_jobs, self._total_duration]

    def evaluate(self):
        pass

    def mutate(self):
        pass






for ggeneration in range(MAX_GENERATIONS):
    # calculate fitness values and put these values, along with
    # the individuals, in a new "weighted" list
    weighted_population = []
    for individual in population:
        fitness_val = fitness(individual)
        weighted_population.append((individual, fitness_val))

    # select two individuals to breed; individuals with higher
    # fitness values are more likely to be selected
    ind1 = weighted_choice(weighted_population)
    ind2 = weighted_choice(weighted_population)

    ind3 = crossover(ind1, ind2) # breed, creating a new individual
    mutate(ind3) # do some random mutating
    population.append(ind3)

    # maybe the parents die? this is just one of many parameters in a
    # GA algorithm
    population.remove(ind1)
    population.remove(ind2)

# generations are completed; find maximum fitness individual
max_fit = fitness(population[0])
max_fit_individual = population[0]
for individual in population:
    fitness_val = fitness(individual)
    if fitness_val > max_fit:
        max_fit = fitness_val
        max_fit_individual = individual
print max_fit_individual