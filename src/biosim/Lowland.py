# -*- coding: utf-8 -*-

"""
Lowland class for the simulation.
"""

import numpy as np


class Lowland:
    """
    Args...
    """
    def __init__(self, f_max=800.0):
        self.f_max = f_max  # Set fodder amount for each new year
        self.fodder = f_max  # Set starting fodder amount to f_max
        self.population = []  # List containing information about all animals in cell
        self.population_count = len(self.population)  # Total population in cell

    def add_animal(self, animal_class, attribute_values):
        animal = animal_class
        values = attribute_values
        animal_dict = dict(animal, values)
        self.population.append(animal_dict)  # Append new animal to population dict

    @property
    def herb_count(self):
        return np.sum[animal_key=='herb' for animal_key.keys in self.population]
