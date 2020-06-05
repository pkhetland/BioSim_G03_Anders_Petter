# -*- coding: utf-8 -*-

"""
A basic interface file containing the minimum requirements for running a simulation
with one animal in one cell.
"""


class Simulation:
    def __init__(self, landscape):
        pass

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


if __name__ == '__main__':
    sim = Simulation('W')
    sim.add_landscape()
    sim.add_animals(['Carnivore'])
