import random


class Individual:
    def __init__(self, genes):
        self.genes = genes
        self.fitness = 0

    def calculate_fitness(self, target):
        # calculate the fitness of the individual based on how close it is to the target
        self.fitness = sum(1 for expected, actual in zip(
            target, self.genes) if expected == actual)

    def mate(self, other, mutation_rate=0.01, gene_set=None):
        # perform crossover and mutation to produce a new individual
        child_genes = []
        for i in range(len(self.genes)):
            if random.random() < 0.5:
                child_genes.append(self.genes[i])
            else:
                child_genes.append(other.genes[i])

        for i in range(len(child_genes)):
            if random.random() < mutation_rate:
                child_genes[i] = random.choice(gene_set)

        return Individual(child_genes)


class GeneticAlgorithm:
    def __init__(self, genes, target, population_size):
        self.genes = genes
        self.target = target
        self.population_size = population_size
        self.population = []
        self.found = False

    def generate_random_individual(self):
        # create a new random individual
        genes = [random.choice(self.genes) for _ in range(len(self.target))]
        return Individual(genes)

    def run(self, mutation_rate=0.01, elitism_rate=0.1):
        gene_set = set(self.genes)

        # create the initial population
        self.population = [self.generate_random_individual()
                           for _ in range(self.population_size)]

        while not self.found:
            # calculate the fitness of each individual
            for individual in self.population:
                individual.calculate_fitness(self.target)

            # check if we've found the target individual
            best_individual = max(
                self.population, key=lambda individual: individual.fitness)
            if best_individual.fitness == len(self.target):
                self.found = True
                break

            # select the parents for the next generation using tournament selection
            parents = []
            for _ in range(self.population_size - int(self.population_size * elitism_rate)):
                tournament = random.sample(self.population, 2)
                parents.append(
                    max(tournament, key=lambda individual: individual.fitness))

            # perform crossover and mutation to create the new generation
            new_population = [best_individual]
            while len(new_population) < self.population_size:
                parent1, parent2 = random.sample(parents, 2)
                child = parent1.mate(
                    parent2, mutation_rate=mutation_rate, gene_set=gene_set)
                new_population.append(child)

            self.population = new_population

        return best_individual.genes
