from db import *
import random

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
                pass
                # print("id: %s,\tjob: %s\n" % (id, job))

        # [[row[i] for row in matrix] for i in range(4)]
        # for x, y in zip(a, b):

def main():
    ga = Ga()
    ga.start()
    db = DataBase()
    # print ga.generation[0].engineers
    db.query("Select * from job")
    jobs_data = db.fetch()
    jobid_key = [jid[0] for jid in jobs_data]  # get job id for key array

    # jobid_key = jobs_data[0]  # get job id for key array
    print jobs_data
    print jobid_key

def main1():
    db = DataBase()
    data = []
    data = db.get_random_eng(2)
    #data = [x[0] for x in engs]
    rnd = random.choice(data)
    print data
    print("Random eng: %s" % rnd)


if __name__ == "__main__":
    main()
