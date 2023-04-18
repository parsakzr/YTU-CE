# !/usr/bin/env python3
import random

# inherit the Individual class from the GA class


class Individual:
    def __init__(self, chromosome) -> None:
        self.chromosome = chromosome
        self.fitness = self.calculate_fitness()

    @classmethod
    def mutated_genes(self, genes):
        # create random genes for mutation
        gene = random.choice(genes)
        return gene

    @classmethod
    def create_genome(self, target):
        # create chromosome or string of genes
        genome_len = len(target)
        return [self.mutated_genes() for _ in range(genome_len)]

    def mate(self, otherParent):
        # perform mating and produce new offspring
        child_chromosome = []
        for gp1, gp2 in zip(self.chromosome, otherParent.chromosome):
            prob = random.random()
            if prob < 0.45:
                child_chromosome.append(gp1)
            elif prob < 0.90:
                child_chromosome.append(gp2)
            else:
                child_chromosome.append(self.mutated_genes())
        return Individual(child_chromosome)

    def calculate_fitness(self):
        # calculate fittness score, it is the number of characters
        # in string which differ from target string.
        global TARGET

        fitness = 0
        for gs, gt in zip(self.chromosome, TARGET):
            if gs != gt:
                fitness += 1
        return fitness


class GeneticAlgorithm:

    def __init__(self, genes, target, population_size=100):
        self.genes = genes
        self.target = target
        self.population_size = population_size

    def run(self):
        # Driver code
        found = False
        generation = 1

        # create initial population
        population = []
        for _ in range(self.population_size):
            genome = Individual.create_genome()
            population.append(Individual(genome))

        while not found:
            # sort the population in increasing order of fitness score
            population = sorted(population, key=lambda x: x.fitness)

            # if the individual having lowest fitness score ie.
            # 0 then we know that we have reached to the target
            # and break the loop
            if population[0].fitness <= 0:
                found = True
                break

            # Otherwise generate new offsprings for new generation
            new_generation = []

            # Perform Elitism, that mean 10% of fittest population
            # goes to the next generation
            s = int((10 * self.population_size) / 100)
            new_generation.extend(population[:s])

            # From 50% of fittest population, Individuals
            # will mate to produce offspring
            s = int((90 * self.population_size) / 100)
            for _ in range(s):
                parent1 = random.choice(population[:50])
                parent2 = random.choice(population[:50])
                child = parent1.mate(parent2)
                new_generation.append(child)

            population = new_generation

            print("Generation: {}\tString: {}\tFitness: {}".format(
                generation, "".join(population[0].chromosome),
                population[0].fitness))

            generation += 1

        print("Generation: {}\tString: {}\tFitness: {}".format(
            generation, "".join(population[0].chromosome),
            population[0].fitness))


if __name__ == '__main':
    # Target string to be generated
    TARGET = "Hello World"

    # Gene Pool
    GENES = '''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOP
    QRSTUVWXYZ 1234567890, .-;:_!"#%&/()=?@${[]}'''

    # Number of individuals in each generation
    POPULATION_SIZE = 100

    ga = GeneticAlgorithm(GENES, TARGET, POPULATION_SIZE)
    ga.run()
