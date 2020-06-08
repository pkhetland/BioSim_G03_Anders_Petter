# -*- coding: utf-8 -*-

"""
Lowland class for the simulation.
"""

import numpy as np
import operator
import random


class Landscape:
    """
    Parent class for landscape cells
    """

    def __init__(self, f_max):
        self.f_max = f_max  # Set fodder amount for each new year
        self.fodder = f_max  # Set starting fodder amount to f_max

        self.animals = []

    def add_animals(self, animal_list):
        for animal in animal_list:
            self.animals.append(animal)

    def randomize(self):
        """
        Defining a function to randomize animals
        """
        random.shuffle(self.animals)

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
        return [animal for animal in self.animals if animal.__class__.__name__ == "Herbivore"]

    @property
    def carnivore_list(self):
        return [animal for animal in self.animals if animal.__class__.__name__ == "Carnivore"]

    @property
    def sorted_carnivores(self):  # Will probably be moved to landscape classes
        fitness_dict = dict([(animal, animal.fitness) for animal in self.carnivore_list])
        sorted_carn_list = [
            pair[0]
            for pair in sorted(fitness_dict.items(), key=operator.itemgetter(1), reverse=True)
        ]
        return sorted_carn_list

    @property
    def sorted_herbivores(self):  # Will probably be moved to landscape classes
        fitness_dict = dict([(animal, animal.fitness) for animal in self.herbivore_list])
        sorted_herb_list = [
            pair[0]
            for pair in sorted(fitness_dict.items(), key=operator.itemgetter(1), reverse=False)
        ]
        return sorted_herb_list


class Lowland(Landscape):
    """
    Lowland class for cells
    """

    def __init__(self, f_max=800.0, location=None):
        super().__init__(f_max)


class Highland(Landscape):
    """
    Highland class for cells
    """

    def __init__(self, f_max=300.0, location=None):
        super().__init__(f_max)


class Desert(Landscape):
    pass


class Water():
    pass
