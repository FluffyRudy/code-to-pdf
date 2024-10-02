# title: 11
# aim: Program to implement Genetics Algorithm using Python.


import random


class GeneticAlgorithm:
    def __init__(self, population_size, gene_length):
        self.population_size = population_size
        self.gene_length = gene_length
        self.population = self.initialize_population()

    def initialize_population(self):
        return [
            [random.randint(0, 1) for _ in range(self.gene_length)]
            for _ in range(self.population_size)
        ]

    def fitness(self, individual):
        return sum(individual)

    def selection(self):
        sorted_population = sorted(self.population, key=self.fitness, reverse=True)
        return sorted_population[: self.population_size // 2]

    def crossover(self, parent1, parent2):
        point = random.randint(1, self.gene_length - 1)
        return parent1[:point] + parent2[point:]

    def mutate(self, individual):
        for i in range(len(individual)):
            if random.random() < 0.01:
                individual[i] = 1 - individual[i]

    def evolve(self):
        selected = self.selection()
        next_generation = []
        while len(next_generation) < self.population_size:
            parent1, parent2 = random.sample(selected, 2)
            child = self.crossover(parent1, parent2)
            self.mutate(child)
            next_generation.append(child)
        self.population = next_generation


ga = GeneticAlgorithm(10, 5)
for _ in range(10):
    ga.evolve()
print(ga.population)
