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
        self.is_mainland = True

        self.herbivores = []
        self.carnivores = []

    def add_animals(self, animal_list):
        """Adds a list of animals to the cell class

        :param animal_list: A list containing animal objects
        :type animal_list: list
        """
        self.herbivores.extend([animal for animal in animal_list if animal.species == 'Herbivore'])
        self.herbivores.extend([animal for animal in animal_list if animal.species == 'Carnivore'])

    def remove_animals(self, animal_list):
        """Removes a list of animal objects from the cell class

        :param animal_list: A list containing animal objects
        :type animal_list: list
        """
        for animal in animal_list:  # Iterate through animals in list
            if animal.species == 'Herbivore':
                self.herbivores.remove(animal)
            else:
                self.carnivores.remove(animal)

    def randomize_herbs(self):
        """Shuffles the self.herbivores list
        """
        random.shuffle(self.herbivores)

    @property
    def animal_count(self):
        """Counts the number of animals in the cell

        :return: Animal count
        :rtype: int
        """
        return len(self.herbivores) + len(self.carnivores)

    @property
    def herb_count(self):
        """Counts the number of herbivores in cell

        :return: Herbivore count
        :rtype: int
        """
        return len(self.herbivores)

    @property
    def carn_count(self):
        """Counts the number of carnivores in cell

        :return: Carnivore count
        :rtype: int
        """
        return len(self.carnivores)

    @property
    def animals(self):
        """Combines herbivores list and carnivores list

        :return: Animal count
        :rtype: int
        """
        return self.herbivores + self.carnivores

    @property
    def sorted_carnivores(self):  # Will probably be moved to landscape classes
        """Sorts all `carnivores` by `fitness` from higher to lower

        :return: Sorted carnivores
        :rtype: list
        """
        fitness_dict = dict([(animal, animal.fitness) for animal in self.carnivores])
        sorted_carnivores = [
            pair[0]
            for pair in sorted(fitness_dict.items(), key=operator.itemgetter(1), reverse=True)
        ]
        return sorted_carnivores

    @property
    def sorted_herbivores(self):  # Will probably be moved to landscape classes
        """Sorts all `herbivores` by `fitness` from lower to higher

        :return: Sorted carnivores
        :rtype: list
        """
        fitness_dict = dict([(animal, animal.fitness) for animal in self.herbivore_list])
        sorted_herbivores = [
            pair[0]
            for pair in sorted(fitness_dict.items(), key=operator.itemgetter(1), reverse=False)
        ]
        return sorted_herbivores

    @property
    def is_empty(self):
        """Checks if the cell is out of fodder

        :return: True if fodder is zero
        :rtype: bool
        """
        return self.fodder == 0


class Lowland(Landscape):
    """
    Lowland class for cells
    """

    def __init__(self, f_max=800.0, location=None):
        super().__init__(f_max)  # Initialise landscape class


class Highland(Landscape):
    """
    Highland class for cells
    """

    def __init__(self, f_max=300.0, location=None):
        super().__init__(f_max)  # Initialise landscape class


class Desert(Landscape):
    """
    Desert class for cells.
    No fodder available for herbivores, but carnivores may kill herbivores.
    """
    def __init__(self):
        super().__init__(f_max=0.0)  # Forces fodder to be 0


class Water:
    """
    Water class for cells. Does not do anything.
    """
    def __init__(self):
        self.is_mainland = False
