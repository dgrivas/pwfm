# coding=utf-8
from __future__ import print_function
from class_db import *


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
    _nebula = []                # Placeholder for offsprings before they enter next generation
    _jobid_key = []             # Job index to id array (key index)
    _engid_key = []             # Engineer index to id array (key index)
    _total_jobs_nr = 0          # Number of total jobs
    _total_engineer_nr = 0      # Number of total engineers
    _duration_dictionary = {}   # Dictionary with {job_id : job_duration}
    _skills = []                # Engineers skill
    _travel_time = 0            # Travel time to add on each job duration
    _crossover_engs = 0         # (CROSSOVER_ENGINEERS * self._total_engineer_nr) / 2
    _crossover_jobs = 0         # (CROSSOVER_JOBS * self._total_jobs_nr)
    _overtime = []
    _workhours = []

    def __init__(self, optimal, lifetime, popsize, traveltime):
        self._max_generations = lifetime
        self._optimal_fitness = optimal
        self._pop_size = popsize
        self._travel_time = traveltime
        self._pop_fitness = [0 for x in range(self._pop_size)]  # Init fitness array
        self._selection_pi = [0 for x in range(self._pop_size)]  # Init selection probability array

    def prepare_pop(self, x_over_engineers, x_over_jobs):
        """
        Get data:
            total jobs
            total engineers.

        Create key arrays for Job's & Engineer's id
        :return: False if no records found, True otherwise
        """
        self._db = DataBase()
        self._total_jobs_nr = self._db.query("Select * from job")
        jobs_data = self._db.fetch()
        # print self._jobs_data
        self._jobid_key = [jid[0] for jid in jobs_data]  # get job id for key array
        for job in jobs_data:
            self._duration_dictionary[job[0]] = job[2]  # get job_id:duration in dictionary
        self._total_engineer_nr = self._db.query("Select * from engineer")
        engineers_data = self._db.fetch()
        self._engid_key = [eid[0] for eid in engineers_data]  # get engineer id for key array
        self._skills = [eid[1] for eid in engineers_data]  # get engineers skills
        self._workhours = [eid[3]-eid[2] for eid in engineers_data]  # get engineers working time
        self._overtime = [eid[4] for eid in engineers_data]  # get engineers overtime limit
        #
        self._crossover_engs = int(round((x_over_engineers * self._total_engineer_nr) / 2))
        self._crossover_jobs = int(round(x_over_jobs * self._total_jobs_nr))
        #
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
        # Update Chromosomes engineers workhours & overtime limits (Class variables for all instances
        self._generation[0].append_eng_data(self._workhours, self._overtime):
        # print ("\nPopulation (size: %s):" % self._pop_size)
        for ind in range(self._pop_size):
            for gene in range(len(self._generation[ind].assignment)):
                # get job id from index
                jid = self._jobid_key[gene]
                # select random engineer from job's CanDo list
                engineer = self._db.get_random_eng(jid)
                # set engineer for job
                self._generation[ind].assignment[gene] = engineer
                pass
            pass
        # Calculate worktime for generation
        self._update_generation_worktime()

    def evaluate_population(self, surplus_weight, overtime_weight):
        """
        Evaluate population fitness.

        cost = SUM(overtime) x overtime_weight + dispersion
        dispersion = SUM|x-X|/n
        :param surplus_weight: weight to multiply overtime in fitness function
        :return: max fitness (min cost)
        """
        # print("\nEvaluate population:")
        best_wt = [(0, 0) for x in range(self._pop_size)]
        # surplus_labor = dispersion = 0
        for ind in range(self._pop_size):
            # self._pop_fitness[ind] = self._generation[ind].evaluate(working_time, overtime_weight)
            surplus_labor, overtime, dispersion = self._generation[ind].evaluate()
            self._pop_fitness[ind] = surplus_weight * surplus_labor + overtime_weight * overtime + dispersion
            best_wt[ind] = (surplus_labor, overtime, dispersion)
            # print("overtime: %s, Dispersion: %s" % (overtime, dispersion))
            pass
        best_fit = min(self._pop_fitness)
        best_ind_idx = self._pop_fitness.index(best_fit)
        best_assignment = self._generation[best_ind_idx].assignment
        best_worktime = self._generation[best_ind_idx].worktime
        (sl, ot, dp) = best_wt[best_ind_idx]
        # print(best_wt)
        print("\t\tsurplus:%s, overtime:%s, dispersion:%s" % (sl, ot, dp))
        return [best_fit, best_assignment, best_worktime, sl, ot, dp]

    def prepare_selection(self):
        """
        Calculate selection probability.

        :param pop_rejection: population rejection percent
        :return: Individuals selected for crossover
        """
        # Prepare selection probability for population
        # Invert fitness value to calculate selection probability
        inv_fitness = [1/(1+x) for x in self._pop_fitness]
        fitness_sum = sum(inv_fitness)
        x2 = 0
        for ind in range(self._pop_size):
            x1 = float(inv_fitness[ind]) / float(fitness_sum)
            x2 += x1
            # print("x1: %s, x2: %s" % (x1, float(x2)))
            self._selection_pi[ind] = x2
            pass

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
        # p = [x[0] for x in parents]
        # print("parents: %s" % p)
        return [x[0] for x in parents]

    def _roulette(self):
        """
        Select random individual.

        """
        r = random.random()
        for i in range(len(self._selection_pi)):
            if self._selection_pi[i] > r:
                return i
            pass

    def individuals2replace(self, inds_nr):
        """
        Identify individuals to replace on next generation (worst n individuals).

        :param inds_nr: number of individuals to replace
        :return list of individuals to replace
        """
        return self._index_sort(self._pop_fitness, inds_nr)

    def crossover(self, father, mother, offspring):
        """
        Crossover father & mother, generate offspring.

        Από τον γονέα Α, θα επιλέγονται οι n τεχνικοί με το μεγαλύτερο και το μικρότερο worktime. Από
        αυτούς με το μεγαλύτερο worktime, θα επιλέγονται x εργασίες απο τον γονέα Α, οι οποίες θα αφαιρούνται
        και θα ανατίθενται σε άλλον τεχνικό σύμφωνα με τις αναθέσεις του γονέα Β. Γι'αυτούς με το μικρότερο worktime,
        η επιλογή θα γίνεται απο τον γονέα Β.
        Το νέο χρωμόσωμα που θα προκύπτει με τις αλλαγές στις αναθέσεις θα περνά στην επόμενη γενιά.
        """
        # Father will become offspring after crossover:
        offspring_assignment = [x for x in self._generation[father].assignment]
        offspring_worktime = [x for x in self._generation[father].worktime]  # range(self._total_engineer_nr)]
        # print("\nassignment:\n%s\nworktime:\n%s" % (offspring_assignment, offspring_worktime))
        #
        # Get CROSSOVER_ENGINEERS/2 with highest worktime from father:
        engineers_h = self._index_sort(offspring_worktime,
                                     top=self._crossover_engs)
        # Get CROSSOVER_ENGINEERS/2 with lowest worktime from father:
        engineers_l = (self._index_sort(offspring_worktime,
                                     top=self._crossover_engs, rev=False))
        # print("\tengs: %s" % engineers)
        engineers_h = [self._engid_key[x] for x in engineers_h]  # get engineer id from index
        engineers_l = [self._engid_key[x] for x in engineers_l]  # get engineer id from index
        # print("\tengs(id): %s" % engineer)
        #
        # Select CROSSOVER_JOBS for chosen engineers from father & replace assignments according to mother's
        for eng in engineers_h:
            # Get jobs index for each engineer (eng) from father
            jobs = [x[0] for x in filter(lambda (i, e): e == eng, enumerate(offspring_assignment))]
            # print("jobs1:%s for engineer:%s" % (jobs, eng))
            # Get random CROSSOVER_JOBS jobs from total engineer's jobs
            k = min(self._crossover_jobs, len(jobs))
            jobs = random.sample(jobs, k)
            # print("jobs:%s" % jobs)
            # Replace job assignments according to mother's assignments:
            for job in jobs:
                offspring_assignment[job] = self._generation[mother].assignment[job]
                pass
            pass
        # Select CROSSOVER_JOBS for chosen engineers from mother & insert into offspring assignments
        for eng in engineers_l:
            # Get jobs index for each engineer (eng) from mother
            jobs = [x[0] for x in filter(lambda (i, e): e == eng, enumerate(self._generation[mother].assignment))]
            # print("jobs:%s for engineer:%s" % (jobs, eng))
            # Get random CROSSOVER_JOBS jobs from total engineer's jobs
            k = min(self._crossover_jobs, len(jobs))
            jobs = random.sample(jobs, k)
            # print("selected jobs:%s" % jobs)
            # Replace job assignments according to mother's assignments:
            for job in jobs:
                offspring_assignment[job] = self._generation[mother].assignment[job]
                pass
            pass
        #
        # Append offspring in nebula:
        self._nebula.append((offspring, offspring_assignment, offspring_worktime))

    def update_generation(self):
        """
        Integrate generated offsprings into generation.

        """
        # Integrate offsprings
        for (x,y,z) in self._nebula:
            self._generation[x].assignment = y
            self._generation[x].worktime = z
            pass
        # Update Worktime:
        self._update_generation_worktime()

    def clear_nebula(self):
        """
        Clear nebula for next generation.

        :return:
        """
        self._nebula = []

    def apply_mutation(self, mutation_p, newborn):
        """
        Apply mutation on generation.

        Θα επιλέγονται τυχαίες εργασίες, με πιθανότητα mutation_p, για τις οποίες θα αλλάζει η ανάθεση
        σε κάποιον άλλο από τους διαθέσιμους για την κάθε εργασία, με τυχαίο τρόπο.
        :param newborn: if True, apply mutation on newborn offsprings else mutate whole generation
        :param mutation_p: mutation probability
        """
        if newborn:
            for (ind,asg,wt) in self._nebula:
                for gene in range(self._total_jobs_nr):
                    r = random.random()
                    if r < mutation_p:
                        asg[gene] = self._db.get_random_eng(self._jobid_key[gene])
                    pass
                pass
        else:
            for ind in self._generation:
                for gene in range(self._total_jobs_nr):
                    r = random.random()
                    if r < mutation_p:
                        # Select random engineer from job's CanDo list
                        ind.assignment[gene] = self._db.get_random_eng(self._jobid_key[gene])
                    pass
            pass

# ---------------------------------------------------------------
    def _update_generation_worktime(self):
        for (i, ind) in enumerate(self._generation):
            # print("\nind: %s\nduration_dictionary: %s" % (i, self._duration_dictionary))
            # print("old jobs: %s\nworktime:\t\t%s" % (ind.assignment, ind.worktime))
            ind.worktime = [0 for x in range(self._total_engineer_nr)]  # reset current worktime
            for job, eng in enumerate(ind.assignment):
                eng_idx = self._engid_key.index(eng)
                skill = float(self._skills[eng_idx])
                # duration = self._duration_dictionary[self._jobid_key[job]] + self._travel_time
                # print("job: %s, Duration: %s" % (job, self._duration_dictionary[self._jobid_key[job]]), end="  -  ")
                duration = self._duration_dictionary[self._jobid_key[job]] * skill
                # print("Skill: %s, New Duration: %s, Round: %s" % (skill, duration, round(duration)))
                duration += self._travel_time
                ind.worktime[eng_idx] += int(round(duration))
                pass
            pass
            # print("new worktime:\t%s" % ind.worktime)

    def print_nebula(self):
        print("\nNebula:")
        for (x,y,z) in self._nebula:
            print("Offspring:%s, %s\n\t%s" % (x,y,z))
            pass
        print ("\n")

    def print_generation(self):
        print("\nGeneration:")
        for i,x in enumerate(self._generation):
            print("%s\t%s" % (i, x.assignment))
            print("\t%s" % x.worktime)
            pass

    def print_pop_fitness(self):
        print("\nGeneration fitness:")
        print("\t%s" % self._pop_fitness)

    def _index_sort(self, unsorted, top, s_key=1, rev=True):
        """
        Sort list with index, return top values.

        # engineers = [(eng, self._generation[father].worktime[eng]) for eng in range(self._total_engineer_nr)]
        # engineers = sorted(engineers, key=lambda f: f[1], reverse=True)  # sort engineers by worktime
        # engineers = [x[0] for x in engineers[:CROSSOVER_ENGINEERS]]
        """
        sorted_list = [(i, unsorted[i]) for i in range(len(unsorted))]
        sorted_list = sorted(sorted_list, key=lambda f: f[s_key], reverse=rev)  # sort sorted_list by key
        sorted_list = [x[0] for x in sorted_list[:top]]
        return sorted_list

########################################################################################################################


class Chromosome:
    """
    chromosome structure definition.

    Chromosome elements: array assignment, len = No of Jobs, value = assignment to engineer
                        array worktime,    len = No of engineers, value = engineers total worktime
                        # array fitness,     len = No of engineers, value = fitness of chromosome
    """
    assignment = []
    worktime = []
    workhours = []
    overtime = []

    def __init__(self, workforce, jobs):
        # Main chromosome array. Contains selected engineer for each job
        # Each position in array represents a job, indexed in Job index to id array (key index)
        self.assignment = [0 for x in range(jobs)]
        # Array to hold engineer's worktime; updated after each assignment
        self.worktime = [0 for x in range(workforce)]

    def append_eng_data(self, eng_workhours, eng_overtime):
        self.workhours = eng_workhours
        self.overtime = eng_overtime

    def evaluate(self):
        """
        Evaluate Chromosome fitness.

        cost = SUM(overtime) x overtime_weight + dispersion
        dispersion = SUM|x-X|/n
        :return: max fitness
        """
        eng_nr = len(self.worktime)
        mean_worktime = sum(self.worktime)/eng_nr
        dispersion = 0
        total_surplus_labor = 0
        total_overtime = 0
        for assigned_workload, wh, ot in zip(self.worktime, self.workhours, self.overtime):
            # Calculate dispersion for each engineer
            dispersion += abs(assigned_workload-mean_worktime)
            # Calculate overtime
            total_surplus_labor += 0 if assigned_workload < wh else min(assigned_workload - wh, ot)
            total_overtime += 0 if assigned_workload < (wh + ot) else assigned_workload - (wh + ot)
            # print("eng:%s, wh:%s, ot:%s, overtime:%s, Surplus:%s" % (assigned_workload, wh, ot, overtime, surplus_labor))
            pass
        dispersion /= eng_nr
        # fitness = overtime_weight * total_overtime + dispersion
        # print ("\tengineers: %s,\tmad: %s,\tot:%s,\tfit:%s" % (eng_nr, dispersion, overtime, fitness))
        # return fitness
        # print(self.worktime)
        # print ("\tengineers: %s,\tmad: %s,\tot:%s,\tsl:%s" % (eng_nr, dispersion, overtime, surplus_labor))
        return total_surplus_labor, total_overtime, dispersion
########################################################################################################################
