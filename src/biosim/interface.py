# -*- coding: utf-8 -*-

"""
A basic interface file containing the minimum requirements for running a simulation
with one animal in one cell.
"""

from src.biosim.animal import Herbivore, Carnivore
from src.biosim.landscape import Lowland

import textwrap

import random as random
import operator


class Simulation:

    def __init__(self, seed=123, randomize_animals=True):
        self.cell = Lowland(f_max=800)
        self.animals = []
        self.year = 0
        random.seed(seed)
        self.randomize_animals = randomize_animals

        for _ in range(200):  # Add animals
            self.animals.append(Herbivore(age=0, weight=20))
            self.animals.append(Carnivore(age=0, weight=20))

    def randomize(self):
        """
        Defining a function to randomize animals
        """
        if self.randomize_animals:
            random.shuffle(self.animals)

    def run_year_cycle(self):
        #  1. Feeding
        self.cell.fodder = self.cell.f_max
        # Randomize animals before feeding
        self.randomize()
        while self.cell.fodder > 0:
            for animal in self.animals:
                animal.eat_fodder(self.cell)  # Feed animal

        #  2. Procreation
        for animal in self.animals:
            if animal.__class__.__name__ == 'Herbivore':
                give_birth, birth_weight = animal.give_birth(self.cell, self.herb_count)

                if give_birth:
                    self.animals.append(Herbivore(weight=birth_weight, age=0))

            else:
                give_birth, birth_weight = animal.give_birth(self.cell, self.carn_count)

                if give_birth:
                    self.animals.append(Herbivore(weight=birth_weight, age=0))



        #  3. Migration

        #  4. Aging
        for animal in self.animals:
            animal.aging()

        #  5. Loss of weight

        #  6. Death
        for animal in self.animals:
            if animal.death():
                self.animals.remove(animal)

        print(sim.animal_count)
        self.year += 1  # Add year to simulation

    def run_simulation(self, num_years):
        if self.animal_count > 0:
            for year in range(num_years):
                print(f'Simulation has been run for {year+1} years.')
                self.run_year_cycle()
        else:
            pass
        print('Simulation complete.')

    @property
    def animal_count(self):
        return len(self.animals)

    @property
    def herb_count(self):
        return len([animal for animal in self.animals if animal.__class__.__name__ == 'Herbivore'])

    @property
    def carn_count(self):
        return len([animal for animal in self.animals if animal.__class__.__name__ == 'Carnivore'])

    @property
    def sorted_carnivores(self):  # Will probably be moved to landscape classes
        fitness_dict = dict([
            (animal, animal.fitness) for animal in self.animals
            if animal.__class__.__name__ == 'Carnivore'
        ])
        sorted_carn_list = [
            pair[0] for pair in sorted(fitness_dict.items(),
                                       key=operator.itemgetter(1),
                                       reverse=True)
        ]
        return sorted_carn_list

    @property
    def sorted_herbivores(self):  # Will probably be moved to landscape classes
        fitness_dict = dict([
            (animal, animal.fitness) for animal in self.animals
            if animal.__class__.__name__ == 'Herbivore'
        ])
        sorted_herb_list = [
            pair[0] for pair in sorted(fitness_dict.items(),
                                       key=operator.itemgetter(1),
                                       reverse=False)
        ]
        return sorted_herb_list


if __name__ == '__main__':

    sim = Simulation()  # Create simple simulation instance

    # sim.run_simulation(num_years=10)

    print([herb.fitness for herb in sim.sorted_herbivores])
    print([carn.fitness for carn in sim.sorted_carnivores])

    # for animal in sim.animals:
    #     print(animal.birth_weight())
