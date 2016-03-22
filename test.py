WORKTIME = 420

class Chromosome:
    _total_duration = 0
    _total_jobs = 0

    def __init__(self, workforce=5, jobs=10):
        self.jobs = [0 for x in range(jobs)]
        self.engineers = [WORKTIME for x in range(workforce)]
        self.dummy_engineer = [self._total_jobs, self._total_duration]


class Ga:
    generation = None
    key = range(10)

    def start(self):
        pop_size = 10
        # Generate empty population
        self.generation = [Chromosome() for x in range(pop_size)]
        generation = self.generation

        # chromos, chromo = [], []
        for individual in generation:
            for id, job in zip(self.key, individual.jobs):
                print("id: %s,\tjob: %s\n" % (id, job))

        # [[row[i] for row in matrix] for i in range(4)]
        # for x, y in zip(a, b):

def main():
    ga = Ga()
    ga.start()
    print ga.generation[0].engineers


if __name__ == "__main__":
    main()
