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
        self.geogr = None
        self.animals = [{'species': 'Herbivore',
                         'age': 5,
                         'weight': 20}
                        for _ in range(150)]

        self.year = 0

    # def add_landscape(self, landscape_str):
    #     for placement, cell in enumerate(landscape_str):
    #         if cell == 'L':
    #             self.landscape.append(Lowland(location=placement))
    #         else:
    #             pass

    def add_animals(self, animals):
        for animal in animals:
            self.animals.append(animal)

    # def run_year_cycle(self):
    #     #  1. Feeding
    #     for animal in self.animals:
    #         #  Sort animals by fitness
    #
    #         #
    #         animal.feed(self.landscape.fodder)
    #         self.landscape.fodder

        #  2. Procreation
        #  3. Migration
        #  4. Aging
        #  5. Loss of weight
        #  6. Death

        # self.year += 1

    # def run_simulation(self, num_years):
    #     for year in num_years:
    #         if year % 10 == 0:  # Print every tenth year for progress
    #             print(f'Simulation has been run for {year} years.')
    #         self.run_year_cycle()


if __name__ == '__main__':

    sim = Simulation()  # Create simple simulation instance

    sim.animals


    # sim.run_simulation(num_years=200)
