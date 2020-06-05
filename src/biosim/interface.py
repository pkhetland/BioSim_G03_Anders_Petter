# -*- coding: utf-8 -*-

"""
A basic interface file containing the minimum requirements for running a simulation
with one animal in one cell.
"""


class Simulation:
    def __init__(self):
        self.landscape = None
        self.animals = None

    def add_landscape(self, landscape):
        if type(landscape) == str:
            self.landscape = landscape
        else:
            print('landscape variable needs to be a string')
            self.landscape = ""

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
    sim = Simulation()
    print(sim.landscape, sim.animals)

    sim.add_landscape('L')
    sim.add_animals(['Carnivore'])
    print(sim.landscape, sim.animals)

