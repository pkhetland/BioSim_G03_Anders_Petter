# -*- coding: utf-8 -*-

"""
A basic interface file containing the minimum requirements for running a simulation
with one animal in one cell.
"""

from src.biosim.animal import Animal, Herbivore
from src.biosim.landscape import Lowland


class Simulation:
    def __init__(self):
        self.landscape = Lowland()  # Create a hardcoded cell
        self.animals = []
        self.year = 0

    # def add_landscape(self, landscape_str):
    #     for placement, cell in enumerate(landscape_str):
    #         if cell == 'L':
    #             self.landscape.append(Lowland(location=placement))
    #         else:
    #             pass

    def add_animals(self, animals):
            self.animals = animals

    def run_year_cycle(self):

        self.year += 1

    def run_simulation(self, num_years):
        for year in num_years:
            if year % 10 == 0:  # Print every tenth year for progress
                print(f'Simulation has been run for {year} years.')
            self.run_year_cycle()


if __name__ == '__main__':
    sim = Simulation()  # Create simple simulation instance

    sim.add_animals([Herbivore(age=0, weight=10)])  # Add a single herbivore
    print(sim.landscape, sim.animals)  # Print updated values

    print(sim.landscape.fodder)

    # sim.run_simulation(num_years=200)
