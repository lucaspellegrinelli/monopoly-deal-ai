import random
import operator

class Individual:
  def __init__(self):
    self.fitness = 0
    self.gene_size = 5
    self.genes = [random.random() for _ in range(self.gene_size)]
    self.mutation_rate = 0.005

  def mutate(self):
    for i in range(len(self.genes)):
      if random.random() <= self.mutation_rate:
        self.genes[i] = random.random()

  def __repr__(self):
    s = "Fitness: " + str(self.fitness) + "\n"
    for gene in self.genes:
      s += str(gene) + " "
    return s

class Population:
  def __init__(self, fit_func, individuals=[]):
    self.population_size = 100
    self.tournament_size = 5
    self.elitism = True
    self.individuals = individuals
    self.fit_func = fit_func

  def initilizePopulation(self):
    self.individuals = [Individual() for _ in range(self.population_size)]
    self.computeFitness()

  def addIndividual(self, indv):
    self.individuals.append(indv)

  def evolve(self):
    new_pop = Population(self.fit_func)

    if self.elitism:
      new_pop.addIndividual(self.getFittest())

    for i in range(1 if self.elitism else 0, self.population_size):
      indv1 = self.tournamentSelection()
      indv2 = self.tournamentSelection()
      new_pop.addIndividual(self.crossoverIndividuals(indv1, indv2))

    for indv in new_pop.individuals:
      indv.mutate()

    new_pop.computeFitness()
    return new_pop

  def getFittest(self):
    return max(self.individuals, key=operator.attrgetter("fitness"))

  def tournamentSelection(self):
    tourn_partic = []
    for _ in range(self.tournament_size):
      index = random.randint(0, self.population_size - 1)
      tourn_partic.append(self.individuals[index])

    tourn_pop = Population(self.fit_func, tourn_partic)
    return tourn_pop.getFittest()

  def crossoverIndividuals(self, indv1, indv2):
    crossovered = Individual()
    for i in range(indv1.gene_size):
      crossovered.genes[i] = indv1.genes[i] if random.random() <= 0.5 else indv2.genes[i]
    return crossovered

  def computeFitness(self):
    for indv in self.individuals:
      indv.fitness = self.fit_func(indv)

  def __repr__(self):
    avg = 0
    for indv in self.individuals:
      avg += indv.fitness
    avg /= len(self.individuals)
    s = "Population Size: " + str(self.population_size) + "\n"
    s += "Average Fitness: " + str(avg) + "\n"
    s += "Best Fitness: " + str(self.getFittest()) + "\n"
    return s
