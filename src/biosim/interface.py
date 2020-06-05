# -*- coding: utf-8 -*-

"""
A basic interface file containing the minimum requirements for running a simulation
with one animal in one cell.
"""

from src.biosim.animal import Animal, Herbivore
from src.biosim.landscape import Lowland


class Simulation:
    def __init__(self):
        self.landscape = []
        self.animals = []

    def add_landscape(self, landscape_str):
        for placement, cell in enumerate(landscape_str):
            if cell is 'W':
                self.landscape.append(Lowland(location=placement))
            else:
                pass


    def add_animals(self, animals):
        if type(animals) == list:
            self.animals = animals
        else:
            print('animals variable needs to be a list')
            self.animals = []

    def year_cycle(self):
        pass

    def run_simulation(self, num_years):
        pass


if __name__ == '__main__':
    sim = Simulation()  # Create simple simulation instance
    print(sim.landscape, sim.animals)  # Test init attribute values

    sim.add_landscape('L')  # Add landscape
    sim.add_animals(['Carnivore'])  # Add animals
    print(sim.landscape, sim.animals)  # Print updated values

    sim.run_simulation(num_years=200)
