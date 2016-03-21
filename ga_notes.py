#init
calculate mean freetime

#chromosome:
int.engineerId
int.array.[1..36]
0: unassigned \/ jobId,locked
	#locked: time limited job, do not move

#	WORKTIME = 420
	TIMESLOTS = 28

		class chromosome:
		    def __init__(self, eng):
		    self.eng = eng
		    self.ft = TIMESLOTS
		    self.jobs = [0 for x in range(TIMESLOTS)]
		    self.locked_jobs = [0 for x in range(TIMESLOTS)]


		class chromosome:
		    def __init__(self, workforce, jobs):
		    self.jobs = [0 for x in range(jobs)]
		    self.engineers = [0 for x in range(workforce + 1)]


#initial population:
for each time_limited_job, rand(canDo)
	if precentence>1 insert in last slot
	else insert in first slot
for each other_job, rand(canDo)
	if precentence>1 insert in last slot
	else insert in first slot

#Evaluation:
min(freetime) unassigned worktime slots
min(freetime variation)
min(unassignedJobs) overtime slots (assigned to dummy Eng)
eval precentence ??
eval time limited jobs


#Selection:
overlapping population


#########################################################################################

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

#########################################################################################

def test():
    d = DataBase()
    rows = d.query("Select * from customer")
    data = d._db_cur.fetchmany(2)
    print("Total rows: %s\nData:\t%s" % (rows, data[1]))

#########################################################################################
