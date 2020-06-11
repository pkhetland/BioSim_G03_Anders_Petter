# -*- coding: utf-8 -*-

"""
Lowland class for the simulation.
"""

import numpy as np
import operator
import random


class Island:
    """
    Island collects all landscape cells in the map
    """

    def __init__(self, map_str):
        self.landscape = self.map_from_str(map_str)
        self.map_str = map_str
        self._land_cells = None

        self.herb_pop_matrix = [[0 for col in self.unique_cols] for row in self.unique_rows]
        self.carn_pop_matrix = [[0 for col in self.unique_cols] for row in self.unique_rows]

        self._herb_fitness_list = []
        self._carn_fitness_list = []


    @property
    def land_cells(self):
        if self._land_cells is None:
            self._land_cells = self.get_land_cells
        return self._land_cells

    @property
    def get_land_cells(self):
        return {loc: cell for loc, cell in self.landscape.items() if cell.is_mainland}

    @property
    def unique_rows(self):
        return list(set([coord[0] for coord in self.landscape]))

    @property
    def unique_cols(self):
        return list(set([coord[1] for coord in self.landscape]))

    def add_animals(self, animal_list):
        pass

    @property
    def all_animals(self):
        """
        :return: A list containing all animals in the mainland cells
        :rtype: list
        """
        return [cell.animals for cell in self.land_cells.values()]

    @property
    def all_herbivores(self):
        """
        :return: A list containing all animals in the mainland cells
        :rtype: list
        """
        return [cell.herbivores for cell in self.land_cells.values()]

    @property
    def all_carnivores(self):
        """
        :return: A list containing all animals in the mainland cells
        :rtype: list
        """
        return [cell.carnivores for cell in self.land_cells.values()]

    @staticmethod
    def map_from_str(map_str):
        """The sim takes in a map str and converts it into a dictionary of
        coord keys and class values

        :param map_str: A multi-line string representing cell classes and coordinates
        :type map_str: str
        ...
        :return: The landscape for the simulation with initiated landscape classes
        :rtype: dict
        """
        map_dict = {}

        for row_coord, cell_row in enumerate(map_str.splitlines()):
            for col_coord, cell in enumerate(cell_row.strip()):
                coord = (row_coord + 1, col_coord + 1)
                if cell == 'W':
                    map_dict[coord] = Water()
                elif cell == 'L':
                    map_dict[coord] = Lowland()
                elif cell == 'H':
                    map_dict[coord] = Highland()
                elif cell == 'D':
                    map_dict[coord] = Desert()
                else:
                    print("Map strings need to be either W, L, H or D! Try setting map again.")
        return map_dict

    def update_pop_matrix(self):
        for row in self.unique_rows[1:-1]:  # First and last cell is water
            for col in self.unique_cols[1:-1]:  # First and last cell is water
                cell = self.landscape[(row, col)]
                if cell.is_mainland:
                    # print(cell)
                    self.herb_pop_matrix[row - 1][col - 1] = cell.herb_count
                    self.carn_pop_matrix[row - 1][col - 1] = cell.carn_count

    @property
    def animal_weights(self):
        herb_weights = []
        carn_weights = []
        for cell in self.land_cells.values():
            for herb in cell.herbivores:
                herb_weights.append(herb.weight)
            for carn in cell.carnivores:
                carn_weights.append(carn.weight)

        return [herb_weights, carn_weights]

    @property
    def animal_ages(self):
        herb_ages = []
        carn_ages = []
        for cell in self.land_cells.values():
            for herb in cell.herbivores:
                herb_ages.append(herb.age)
            for carn in cell.carnivores:
                carn_ages.append(carn.age)
        return [herb_ages, carn_ages]

    @property
    def animal_fitness(self):
        herb_fits = []
        carn_fits = []
        for cell in self.land_cells.values():
            for herb in cell.herbivores:
                herb_fits.append(herb.fitness)
            for carn in cell.carnivores:
                carn_fits.append(carn.fitness)

        return [herb_fits, carn_fits]


class LandscapeCell:
    """
    Parent class for landscape cells
    """

    def __init__(self, f_max):
        self._f_max = f_max  # Set fodder amount for each new year
        self._fodder = f_max  # Set starting fodder amount to f_max
        self._is_mainland = True

        self.herbivores = []
        self.carnivores = []

        np.random.seed(123)

    def __repr__(self):
        return '{}(f_max: {})'.format(self.__class__.__name__, self._f_max)

    def __str__(self):
        return '{}(f_max: {})'.format(self.__class__.__name__, self._f_max)

    @property
    def f_max(self):
        return self._f_max

    @f_max.setter
    def f_max(self, f_max):
        if f_max >= 0:
            self._f_max = f_max

    @property
    def fodder(self):
        return self._fodder

    @fodder.setter
    def fodder(self, fodder):
        if fodder >= 0:
            self._fodder = fodder

    @property
    def is_mainland(self):
        return self._is_mainland

    def add_animals(self, animal_list):
        """Adds a list of animals to the cell class

        :param animal_list: A list containing animal objects
        :type animal_list: list
        """
        for animal in animal_list:  # Iterate through animals in list
            if animal.species == "Herbivore":
                self.herbivores.append(animal)
            elif animal.species == "Carnivore":
                self.carnivores.append(animal)

    def remove_animals(self, animal_list):
        """Removes a list of animal objects from the cell class

        :param animal_list: A list containing animal objects
        :type animal_list: list
        """
        for animal in animal_list:  # Iterate through animals in list
            if animal.species == "Herbivore":
                self.herbivores.remove(animal)
            elif animal.species == "Carnivore":
                self.carnivores.remove(animal)

    def randomize_herbs(self):
        """Shuffles the self.herbivores list
        """
        random.shuffle(self.herbivores)

    @property
    def animals(self):
        """Combines herbivores list and carnivores list

        :return: Animal count
        :rtype: int
        """
        return self.herbivores + self.carnivores

    @property
    def animal_count(self):
        """Counts the number of animals in the cell

        :return: Animal count
        :rtype: int
        """
        return len(self.animals)

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
    def sorted_carnivores(self):  # Will probably be moved to landscape classes
        """Sorts all `carnivores` by `fitness` from higher to lower

        :return: Sorted carnivores
        :rtype: list
        """
        fitness_dict = dict([(carn, carn.fitness) for carn in self.carnivores])
        sorted_carnivores = [
            pair[0]
            for pair in sorted(
                fitness_dict.items(), key=operator.itemgetter(1), reverse=True
            )
        ]
        return sorted_carnivores

    @property
    def sorted_herbivores(self):
        """Sorts all `herbivores` by `fitness` from lower to higher

        :return: Sorted carnivores
        :rtype: list
        """
        fitness_dict = dict([(herb, herb.fitness) for herb in self.herbivores])
        sorted_herbivores = [
            pair[0]
            for pair in sorted(
                fitness_dict.items(), key=operator.itemgetter(1), reverse=False
            )
        ]
        return sorted_herbivores

    @property
    def is_empty(self):
        """Checks if the cell is out of fodder

        :return: True if fodder is zero
        :rtype: bool
        """
        return self.fodder == 0


class Lowland(LandscapeCell):
    """
    Lowland class for cells
    """

    def __init__(self, f_max=800.0, location=None):
        super().__init__(f_max)  # Initialise landscape class


class Highland(LandscapeCell):
    """
    Highland class for cells
    """

    def __init__(self, f_max=300.0, location=None):
        super().__init__(f_max)  # Initialise landscape class


class Desert(LandscapeCell):
    """
    Desert class for cells.
    No fodder available for herbivores, but carnivores may kill herbivores
    """

    def __init__(self):
        super().__init__(f_max=0.0)  # Forces fodder to be 0


class Water:
    """
    Water class for cells
    """

    def __init__(self):
        self.is_mainland = False

    def __repr__(self):
        return 'Water cell'

    def __str__(self):
        return 'Water cell'
