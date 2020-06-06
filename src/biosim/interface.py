# -*- coding: utf-8 -*-

"""
A basic interface file containing the minimum requirements for running a simulation
with one animal in one cell.
"""

from src.biosim.animal import Herbivore
from src.biosim.landscape import Lowland

import textwrap

import random as random


class Simulation:

    def __init__(self, seed=123, randomize_animals=True):
        self.cell = Lowland(f_max=800)
        self.animals = [Herbivore(age=0, weight=20) for _ in range(3)]
        self.year = 0
        random.seed(seed)
        self.randomize_animals = randomize_animals

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
        n_herb = self.animal_count
        for animal in self.animals:
            give_birth, birth_weight = animal.give_birth(self.cell, n_herb)
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
        for year in range(num_years):
            print(f'Simulation has been run for {year+1} years.')
            self.run_year_cycle()

    @property
    def animal_count(self):
        return len(self.animals)


if __name__ == '__main__':

    sim = Simulation()  # Create simple simulation instance

    sim.run_simulation(num_years=100)

