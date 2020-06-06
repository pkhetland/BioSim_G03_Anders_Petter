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

        for _ in range(100:  # Add animals
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
            for herb in self.herbivore_list:  # Herbivores eat first
                herb.eat_fodder(self.cell)

        for carn in self.carnivore_list:  # Carnivores eat last
            herbs_killed = carn.kill_prey(self.sorted_herbivores)  # Carnivore hunts for herbivores
            for herb in herbs_killed:
                self.animals.remove(herb)

        #  2. Procreation
        for herb in self.herbivore_list:  # Herbivores give birth
            give_birth, birth_weight = herb.give_birth(self.cell, self.herb_count)

            if give_birth:
                self.animals.append(Herbivore(weight=birth_weight, age=0))

        for carn in self.carnivore_list:  # Carnivores give birth
            give_birth, birth_weight = carn.give_birth(self.cell, self.carn_count)

            if give_birth:
                self.animals.append(Carnivore(weight=birth_weight, age=0))


        #  3. Migration

        #  4. Aging
        for animal in self.animals:
            animal.aging()

        #  5. Loss of weight

        #  6. Death
        for animal in self.animals:
            if animal.death():
                self.animals.remove(animal)

        self.year += 1  # Add year to simulation

    def run_simulation(self, num_years):
        for year in range(num_years):
            print(f'Year: {year+1}.')
            print(f'Carnivore count: {self.carn_count}')
            print(f'Herbivore count: {self.herb_count}')
            self.run_year_cycle()
        print('Simulation complete.')

    @property
    def animal_count(self):
        return len(self.animals)

    @property
    def herb_count(self):
        return len(self.herbivore_list)

    @property
    def carn_count(self):
        return len(self.carnivore_list)

    @property
    def herbivore_list(self):
        return [animal for animal in self.animals if animal.__class__.__name__ == 'Herbivore']

    @property
    def carnivore_list(self):
        return [animal for animal in self.animals if animal.__class__.__name__ == 'Carnivore']

    @property
    def sorted_carnivores(self):  # Will probably be moved to landscape classes
        fitness_dict = dict([
            (animal, animal.fitness) for animal in self.carnivore_list
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
            (animal, animal.fitness) for animal in self.herbivore_list
        ])
        sorted_herb_list = [
            pair[0] for pair in sorted(fitness_dict.items(),
                                       key=operator.itemgetter(1),
                                       reverse=False)
        ]
        return sorted_herb_list


if __name__ == '__main__':

    sim = Simulation()  # Create simple simulation instance

    sim.run_simulation(num_years=100)

    # for animal in sim.animals:
    #     print(animal.birth_weight())
