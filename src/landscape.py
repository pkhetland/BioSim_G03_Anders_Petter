# -*- coding: utf-8 -*-

"""
Lowland class for the simulation.
"""

import numpy as np
import operator
import random
from src.animal import Herbivore, Carnivore


class Island:
    """
    Island collects all landscape cells in the map and keeps track of animals
    """

    def __init__(self, map_str):
        self.landscape = self.map_from_str(map_str)  # Create landscape from map_str
        self.map_str = map_str  # Save map_str as property
        self._land_cells = None  # Create placeholder for mainland cells
        self.check_border_cells()  # Initiate test of map borders e.g. that all are Water cells
        self.set_neighbors()  # Define neighbor cells for each cell and save for later

        self._num_herbs = 0  # Herbivore counter
        self._num_carns = 0  # Carnivore counter

        self.herb_pop_matrix = [[0 for _ in self.unique_cols] for _ in self.unique_rows]  # Herbivore population matrix
        self.carn_pop_matrix = [[0 for _ in self.unique_cols] for _ in self.unique_rows]  # Carnivore population matrix

    def count_animals(self, num_herbs=0, num_carns=0, animal_list=None):
        """Count animals for fast retrieval when needed

        :param num_herbs: Number of herbs to be counted
        :type num_herbs: int
        :param num_carns: Number of carns to be counted
        :type num_carns: int
        :param animal_list: List of animal instances with automatic counting
        :type animal_list: list
        """

        if num_herbs >= 0 and num_carns >= 0:
            self._num_herbs += num_herbs  # Count herbs
            self._num_carns += num_carns  # Count carns
        else:
            raise ValueError('num_herbs and num_carns need to be 0 or a positive integer.')

        if animal_list is not None:
            self._num_herbs += len(
                [animal for animal in animal_list if animal.species == "Herbivore"]
            )  # Count herbivores
            self._num_carns += len(
                [animal for animal in animal_list if animal.species == "Carnivore"]
            )  # Count carnivores

    def del_animals(self, num_herbs=0, num_carns=0, animal_list=None):
        """Remove animals from counters

        :param num_herbs: Number of herbs to be removed
        :type num_herbs: int
        :param num_carns: Number of carns to be removed
        :type num_carns: int
        :param animal_list: List of animal instances with automatic removal
        :type animal_list: list
        """
        if num_herbs >= 0 and num_carns >= 0:
            self._num_herbs -= num_herbs  # Remove herbs
            self._num_carns -= num_carns  # Remove carns
        else:
            raise ValueError('num_herbs and num_carns need to be 0 or a positive integer.')

        if animal_list is not None:
            self._num_herbs -= len(
                [animal for animal in animal_list if animal.species == "Herbivore"]
            )
            self._num_carns -= len(
                [animal for animal in animal_list if animal.species == "Carnivore"]
            )

    def set_neighbors(self):
        """Find and save mainland neighbor cells for all cells in Island instance"""
        for loc, cell in self._land_cells.items():
            neighbor_cells = [
                self.landscape[(loc[0] - 1, loc[1])],
                self.landscape[(loc[0], loc[1] + 1)],
                self.landscape[(loc[0] + 1, loc[1])],
                self.landscape[(loc[0], loc[1] - 1)],
            ]
            cell.land_cell_neighbors = [
                neighbor for neighbor in neighbor_cells if neighbor.type != "Water"
            ]

    @property
    def num_animals(self):
        """Total animal count of Island instance

        :return: Total animal count
        :rtype: int
        """
        return self._num_herbs + self._num_carns

    @property
    def num_herbs(self):
        """Herb count of Island instance

        :return: Herb count
        :rtype: int
        """
        return self._num_herbs

    @property
    def num_carns(self):
        """Carn count of Island instance

        :return: Carn count
        :rtype: int
        """
        return self._num_carns

    @staticmethod
    def set_landscape_params(landscape, params):
        """Update class parameters of Lowland or Highland class

        :param landscape: Indicator of either Lowland og Highland
        :type landscape: str
        :param params: New keys and values for class variables
        :type params: dict
        """
        if landscape == "L":
            Lowland.set_params(params)
        elif landscape == "H":
            Highland.set_params(params)
        else:
            raise ValueError(
                "Only params in Lowland and Highland can be changed! No params set."
            )

    @property
    def land_cells(self):
        """Getter function for _land_cells property

        :return: Coord and instance of mainland cells
        :rtype: dict
        """
        if self._land_cells is None:
            self._land_cells = self.get_land_cells
        return self._land_cells

    @property
    def get_land_cells(self):
        """ Check is_mainland property and discard Water cells. Only runs once.

        :return: Coord and instance of mainland cells
        :rtype: dict
        """
        return {loc: cell for loc, cell in self.landscape.items() if cell.is_mainland}

    @property
    def unique_rows(self):
        """Return unique row values

        :return: Row coordinate values
        :rtype: list
        """
        return list(set([coord[0] for coord in self.landscape]))

    @property
    def unique_cols(self):
        """Return unique col values

        :return: Col coordinate values
        :rtype: list
        """
        return list(set([coord[1] for coord in self.landscape]))

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

        # Test row lengths
        row_lengths = [len(row.strip()) for row in map_str.strip(" ").splitlines()]
        for i, row in enumerate(row_lengths[:-1]):
            if row_lengths[i] != row_lengths[i + 1]:
                raise ValueError("Map needs to have uniform row lengths!")

        for row_coord, cell_row in enumerate(map_str.splitlines()):
            for col_coord, cell in enumerate(cell_row.strip()):
                coord = (row_coord + 1, col_coord + 1)

                if cell == "W":
                    map_dict[coord] = Water()
                elif cell == "L":
                    map_dict[coord] = Lowland()
                elif cell == "H":
                    map_dict[coord] = Highland()
                elif cell == "D":
                    map_dict[coord] = Desert()
                else:
                    raise ValueError(
                        "Map strings need to be either W, L, H or D! " "Try setting map again."
                    )

        return map_dict

    def check_border_cells(self):
        """Iterate through land_cells and check that none have border coordinates"""
        for row, col in self.land_cells:
            if row == 1 or row == self.unique_rows[-1] or col == 1 or col == self.unique_cols[-1]:
                raise ValueError("Only water cells may be border cells!")

    def update_pop_matrix(self):
        """Update the population matrices for heatmap"""
        for row in self.unique_rows[1:-1]:  # First and last cell is water
            for col in self.unique_cols[1:-1]:  # First and last cell is water
                cell = self.landscape[(row, col)]
                if cell.is_mainland:
                    # print(cell)
                    self.herb_pop_matrix[row - 1][col - 1] = cell.herb_count
                    self.carn_pop_matrix[row - 1][col - 1] = cell.carn_count

    @property
    def animal_weights(self):
        """Find weights of current animals in Island instance for histograms

        :return: Herbivore weights and carnivore weights
        :rtype: List of lists
        """
        herb_weights = []
        carn_weights = []
        for cell in self.land_cells.values():
            for herb in cell.herbivores:
                herb_weights.append(herb.weight)
            for carn in cell.carnivores:
                carn_weights.append(carn.weight)

        if not herb_weights:
            return [carn_weights]
        elif not carn_weights:
            return [herb_weights]
        else:
            return [herb_weights, carn_weights]

    @property
    def animal_ages(self):
        """Find ages of current animals in Island instance for histograms

        :return: Herbivore ages and carnivore ages
        :rtype: List of lists
        """
        herb_ages = []
        carn_ages = []
        for cell in self.land_cells.values():
            for herb in cell.herbivores:
                herb_ages.append(herb.age)
            for carn in cell.carnivores:
                carn_ages.append(carn.age)
        if not herb_ages:
            return [carn_ages]
        elif not carn_ages:
            return [herb_ages]
        else:
            return [herb_ages, carn_ages]

    @property
    def animal_fitness(self):
        """Find fitness of current animals in Island instance for histograms

        :return: Herbivore fitness and carnivore fitness
        :rtype: List of lists
        """
        herb_fits = []
        carn_fits = []
        for cell in self.land_cells.values():
            for herb in cell.herbivores:
                herb_fits.append(herb.fitness)
            for carn in cell.carnivores:
                carn_fits.append(carn.fitness)
        if not herb_fits:
            return [carn_fits]
        elif not carn_fits:
            return [herb_fits]
        else:
            return [herb_fits, carn_fits]


class LandscapeCell:
    """
    Parent class for landscape cells
    """
    def __init__(self):
        self._fodder = self.f_max()
        self._is_mainland = True
        self.type = self.__class__.__name__

        self.herbivores = []
        self.carnivores = []
        self.land_cell_neighbors = []

    def __repr__(self):
        return "{}(f_max: {})".format(self.__class__.__name__, self.f_max())

    def __str__(self):
        return "{}(f_max: {})".format(self.__class__.__name__, self.f_max())

    @classmethod
    def set_params(cls, param_dict):
        """Set new values of class parameters for Herbivore or Carnivore

        :param param_dict: Keys and values for new param values
        :type param_dict: dict
        """
        for param in param_dict:
            if param in cls.params:
                cls.params[param] = param_dict[param]
            else:
                raise AttributeError("Invalid parameter dictionary! Format: {'<param>': <value>}")

    @classmethod
    def f_max(cls):
        """Getter method for _f_max property"""
        return cls.params["f_max"]

    @property
    def fodder(self):
        """Getter method for cell._fodder property"""
        return self._fodder

    @fodder.setter
    def fodder(self, new_fodder):
        """Setter method for fodder property"""
        self._fodder = new_fodder

    @property
    def is_mainland(self):
        """Getter method for is_mainland property"""
        return self._is_mainland

    def reset_animals(self):
        """Reset has_moved property of all animals after all animals in a cell has moved"""
        for animal in self.animals:
            animal.has_moved = False

    def add_animals(self, animal_list):
        """Adds a list of animals to the cell class

        :param animal_list: A list containing animal objects
        :type animal_list: list
        """
        for animal in animal_list:  # Iterate through animals in list
            if isinstance(animal, Herbivore):
                self.herbivores.append(animal)
            elif isinstance(animal, Carnivore):
                self.carnivores.append(animal)
            else:
                raise ValueError("List may only contain Herbivore and Carnivore instances!")

    def remove_animals(self, animal_list):
        """Removes a list of animal objects from the cell class

        :param animal_list: A list containing animal objects
        :type animal_list: list
        """
        for animal in animal_list:  # Iterate through animals in list
            if isinstance(animal, Herbivore):
                self.herbivores.remove(animal)
            elif isinstance(animal, Carnivore):
                self.carnivores.remove(animal)
            else:
                raise AttributeError("List may only contain Herbivore and Carnivore instances!")

    def randomize_herbs(self):
        """Shuffles the self.herbivores list"""
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
            for pair in sorted(fitness_dict.items(), key=operator.itemgetter(1), reverse=True)
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


class Lowland(LandscapeCell):
    """
    Lowland class for cells
    """
    params = {"f_max": 800.0}

    def __init__(self):
        super().__init__()  # Initialise landscape class


class Highland(LandscapeCell):
    """
    Highland class for cells
    """
    params = {"f_max": 300.0}

    def __init__(self, location=None):
        super().__init__()  # Initialise landscape class


class Desert(LandscapeCell):
    """
    Desert class for cells.
    No fodder available for herbivores, but carnivores may kill herbivores
    """
    params = {"f_max": 0.0}

    def __init__(self):
        super().__init__()  # Initialise landscape class


class Water:
    """
    Water class for cells
    """
    is_mainland = False
    type = "Water"

    def __repr__(self):
        return "Water cell"

    def __str__(self):
        return "Water cell"
