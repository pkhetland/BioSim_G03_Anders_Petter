# -*- coding: utf-8 -*-

"""
Lowland class for the simulation.
"""

import numpy as np


class Lowland:
    """
    Args...
    """
    def __init__(self, f_max=800.0, location=None):
        self.f_max = f_max  # Set fodder amount for each new year
        self.fodder = f_max  # Set starting fodder amount to f_max
        self.population = []  # List containing information about all animals in cell
        if location:
            self.location = location

    def add_animal(self, animal_species, age, weight):
        animal_dict = {'species': animal_species, 'age': age, 'weight': weight}
        self.population.append(animal_dict)  # Append new animal to population dict

    @property
    def herb_count(self):
        return np.sum([animal_dict['species'] == 'Herbivore' for animal_dict in self.population])

    @property
    def carn_count(self):
        return np.sum([animal_dict['species'] == 'Carnivore' for animal_dict in self.population])

    @property
    def population_count(self):
        return len(self.population)
