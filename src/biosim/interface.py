# -*- coding: utf-8 -*-

"""
A basic interface file containing the minimum requirements for running a simulation
with one animal in one cell.
"""

from src.biosim.animal import Animal, Herbivore
from src.biosim.landscape import Lowland

import textwrap


class Simulation:
    def __init__(self):
        self.cell = Lowland()
        self.animals = [Herbivore(age=5, weight=20) for _ in range(5)]

        self.year = 0

    def run_year_cycle(self):
        #  1. Feeding
        self.cell.fodder = self.cell.f_max
        for animal in self.animals:
            self.cell.fodder -= animal.p['beta'] * animal.p['F']  # Remove amount to be eaten
            animal.eat_fodder()  # Feed animal
            print(animal.fitness())
        print(self.cell.fodder)

        #  2. Procreation
        #  3. Migration
        #  4. Aging
        #  5. Loss of weight
        #  6. Death

        # self.year += 1

    def run_simulation(self, num_years):
        for year in range(num_years):
            print(f'Simulation has been run for {year+1} years.')
            self.run_year_cycle()


if __name__ == '__main__':

    sim = Simulation()  # Create simple simulation instance

    sim.run_simulation(num_years=5)
