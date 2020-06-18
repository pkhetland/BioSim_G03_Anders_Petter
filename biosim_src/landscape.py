# -*- coding: utf-8 -*-

"""
Lowland class for the simulation.
"""

import random
from biosim_src.animal import Herbivore, Carnivore


class Island:
    """The Island object collects all landscape cells in the map and keeps track of animals.

    :param map_str: The representation of cell types in the simulation
    :type map_str: str

    :Example:
        .. code-block:: python

            example_map = '''WWWW
                             WLDW
                             WHDW
                             WWWW'''

    .. note::

        - Only H, L, D and W cell representation are accepted.
        - All map rows need to be the same length.
    """

    def __init__(self, map_str):
        self.landscape = self.map_from_str(map_str)  # Create landscape from map_str
        self.map_str = map_str  # Save map_str as property
        self._land_cells = None  # Create placeholder for mainland cells
        self.check_border_cells()  # Initiate test of map borders e.g. that all are Water cells
        self.set_neighbors()  # Define neighbor cells for each cell and save for later

        self._num_herbs = 0  # Herbivore counter
        self._num_carns = 0  # Carnivore counter

        self.herb_pop_matrix = [[0 for _ in self.unique_cols] for _ in self.unique_rows]
        # Herbivore population matrix
        self.carn_pop_matrix = [[0 for _ in self.unique_cols] for _ in self.unique_rows]
        # Carnivore population matrix

    def count_animals(self, num_herbs=0, num_carns=0, animal_list=None):
        """Count animals for fast retrieval when needed.

        :param num_herbs: Number of herbs to be counted
        :type num_herbs: int
        :param num_carns: Number of carns to be counted
        :type num_carns: int
        :param animal_list: List of animal instances with automatic counting
        :type animal_list: list

        .. note::

            The user may count animals using integer directly, or pass a list of Animal objects
            for automatic counting.

        .. seealso::

            Island.del_animals
        """

        if num_herbs >= 0 and num_carns >= 0:
            self._num_herbs += num_herbs  # Count herbs
            self._num_carns += num_carns  # Count carns
        else:
            raise ValueError("num_herbs and num_carns need to be 0 or a positive integer.")

        if animal_list is not None:
            self._num_herbs += len(
                [animal for animal in animal_list if animal.species == "Herbivore"]
            )  # Count herbivores
            self._num_carns += len(
                [animal for animal in animal_list if animal.species == "Carnivore"]
            )  # Count carnivores

    def del_animals(self, num_herbs=0, num_carns=0, animal_list=None):
        """Remove animals from counters.

        :param num_herbs: Number of herbs to be removed
        :type num_herbs: int
        :param num_carns: Number of carns to be removed
        :type num_carns: int
        :param animal_list: List of animal instances with automatic removal
        :type animal_list: list

        .. note::
            Like count_animals, integer can be passed or a list of Animal objects.

        .. seealso::

            Island.count_animals
        """
        if num_herbs >= 0 and num_carns >= 0:
            self._num_herbs -= num_herbs  # Remove herbs
            self._num_carns -= num_carns  # Remove carns
        else:
            raise ValueError("num_herbs and num_carns need to be 0 or a positive integer.")

        if animal_list is not None:
            self._num_herbs -= len(
                [animal for animal in animal_list if animal.species == "Herbivore"]
            )
            self._num_carns -= len(
                [animal for animal in animal_list if animal.species == "Carnivore"]
            )

    def set_neighbors(self):
        """Find and save mainland neighbor cells for all mainland cells in Island instance.

        .. note::

            - This function only runs once when instantiating the Island object.
            - Only mainland neighbors will be saved to the list.
        """
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
        """Total animal count of Island instance.

        :return: Total animal count
        :rtype: int

        .. seealso::
            - Island.num_herbs
            - Island.num_carns
        """
        return self._num_herbs + self._num_carns

    @property
    def num_herbs(self):
        """Herb count of Island instance

        :return: Herb count
        :rtype: int

        .. seealso::
            - Island.num_animals
            - Island.num_carns

        """
        return self._num_herbs

    @property
    def num_carns(self):
        """Carn count of Island instance

        :return: Carn count
        :rtype: int

        .. seealso::
            - Island.num_herbs
            - Island.num_animals

        """
        return self._num_carns

    @staticmethod
    def set_landscape_params(landscape, params):
        """Update class parameters of Lowland or Highland class.

        :param landscape: Indicator of either Lowland og Highland
        :type landscape: str
        :param params: New keys and values for class variables
        :type params: dict

        :Example:
            .. code-block:: python

                set_landscape_params('L', {'f_max': 500.0}}

        .. note::
            - Only 'L' and 'H' contain changeable parameters
            - Only 'f_max' is changeable in the current version.

        """
        if landscape == "L":
            Lowland.set_params(params)
        elif landscape == "H":
            Highland.set_params(params)
        else:
            raise ValueError("Only params in Lowland and Highland can be changed! No params set.")

    @property
    def land_cells(self):
        """Getter function for _land_cells property.

        :return: Coord and instance of mainland cells
        :rtype: dict

        .. note::
            This method runs the get_land_cells method the first time it is called,
            and then functions as a getter for `Island._land_cells`

        .. seealso::
            - Island.get_land_cells

        """
        if self._land_cells is None:
            self._land_cells = self.get_land_cells
        return self._land_cells

    @property
    def get_land_cells(self):
        """Check is_mainland property and discard Water cells.

        :return: Coord and instance of mainland cells
        :rtype: dict

        .. seealso::
            - Island.land_cells

        """
        return {loc: cell for loc, cell in self.landscape.items() if cell.is_mainland}

    @property
    def unique_rows(self):
        """Return unique row values.

        :return: Row coordinate values
        :rtype: list

        .. seealso::
            - Island.unique_cols

        """
        return list(set([coord[0] for coord in self.landscape]))

    @property
    def unique_cols(self):
        """Return unique col values.

        :return: Col coordinate values
        :rtype: list

        .. seealso::
            - Island.unique_rows

        """
        return list(set([coord[1] for coord in self.landscape]))

    @staticmethod
    def map_from_str(map_str):
        """The Island instance takes in a map str and converts it into a dictionary of
        coord keys and class values.

        :param map_str: A multi-line string representing cell classes and coordinates
        :type map_str: str
            ...
        :return: The landscape for the simulation with initiated landscape classes
        :rtype: dict

        :Example:
            .. code-block:: python

                example_input = '''WWW
                                   WLW
                                   WWW'''

                example_return = [
                    (1, 1): Water(), (1, 2): Water(), (1, 3): Water()
                    (2, 1): Water(), (2, 2): Lowland(), (2, 3): Water()
                    (3, 1): Water(), (3, 2): Water(), (3, 3): Water()
                ]

        .. seealso::
            - Island.__init__

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
        """Iterate through land_cells and check that none have border coordinates.

        .. note::
            The borders are checked when the Island instance is initiated.

        """
        for row, col in self.land_cells:
            if row == 1 or row == self.unique_rows[-1] or col == 1 or col == self.unique_cols[-1]:
                raise ValueError("Only water cells may be border cells!")

    def update_pop_matrix(self):
        """Update the population matrices for heatmap.

        :Example:

            .. code-block:: python

                example_matrix = [
                    [0, 0, 0],
                    [0, 221, 0],
                    [0, 0, 0],
                ]

        .. seealso::
            - `visualization` module

        """
        for row in self.unique_rows[1:-1]:  # First and last cell is water
            for col in self.unique_cols[1:-1]:  # First and last cell is water
                cell = self.landscape[(row, col)]
                if cell.is_mainland:
                    # print(cell)
                    self.herb_pop_matrix[row - 1][col - 1] = cell.herb_count
                    self.carn_pop_matrix[row - 1][col - 1] = cell.carn_count

    @property
    def animal_weights(self):
        """Find weights of current animals in Island instance for histograms.

        :return: Herbivore weights and carnivore weights
        :rtype: List of lists

        .. seealso::
            - Island.animal_ages
            - Island.animal_fitness

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
        """Find ages of current animals in Island instance for histograms.

        :return: Herbivore ages and carnivore ages
        :rtype: List of lists

        .. seealso::
            - Island.animal_weights
            - Island.animal_fitness

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
        """Find fitness of current animals in Island instance for histograms.

        :return: Herbivore fitness and carnivore fitness
        :rtype: List of lists

        .. seealso::
            - Island.animal_ages
            - Island.animal_weights

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
    """Parent class for landscape cells.

    :Subclasses:
        - Lowland
        - Highland
        - Desert

    :Properties:
        - herbivores: A list containing herbivores in the cell
        - carnivores: A list containing carnivores in the cell

    .. note::
        LandscapeCell objects will be instantiated through subclasses and be contained in an
        Island object.

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
        """Set new values of class parameters for Herbivore or Carnivore.

        :param param_dict: Keys and values for new param values
        :type param_dict: dict

        .. seealso::
            - `BioSim.set_animal_parameters`

        """
        for param in param_dict:
            if param in cls.params:
                cls.params[param] = param_dict[param]
            else:
                raise AttributeError("Invalid parameter dictionary! Format: {'<param>': <value>}")

    @classmethod
    def f_max(cls):
        """Getter method for LandscapeCell._f_max property of Island instance."""
        return cls.params["f_max"]

    @property
    def fodder(self):
        """Getter method for LandscapeCell._fodder property."""
        return self._fodder

    @fodder.setter
    def fodder(self, new_fodder):
        """Setter method for LandscapeCell._fodder property."""
        self._fodder = new_fodder

    @property
    def is_mainland(self):
        """Getter method for LandscapeCell._is_mainland property."""
        return self._is_mainland

    def reset_animals(self):
        """Reset Animal.has_moved property of animals after all animals in a cell has
        had the chance to migrate.

        .. note::
            The Animal.has_moved property ensures no animal moves twice in the same yearly cycle.

        .. seealso::
            - Animal.migrate
            - BioSim.migrate

        """
        for animal in self.animals:
            animal.has_moved = False

    def add_animals(self, animal_list):
        """Adds a list of animals to the cell class.

        :param animal_list: A list containing animal objects
        :type animal_list: list

        .. seealso::
            - LandscapeCell.remove_animals
            - LandscapeCell.herbivores
            - LandscapeCell.carnivores

        """
        for animal in animal_list:  # Iterate through animals in list
            if isinstance(animal, Herbivore):
                self.herbivores.append(animal)
            elif isinstance(animal, Carnivore):
                self.carnivores.append(animal)
            else:
                raise ValueError("List may only contain Herbivore and Carnivore instances!")

    def remove_animals(self, animal_list):
        """Removes a list of animal objects from the cell class.

        :param animal_list: A list containing animal objects
        :type animal_list: list

        .. seealso::
            - LandscapeCell.add_animals
            - LandscapeCell.herbivores
            - LandscapeCell.carnivores

        """
        for animal in animal_list:  # Iterate through animals in list
            if isinstance(animal, Herbivore):
                self.herbivores.remove(animal)
            elif isinstance(animal, Carnivore):
                self.carnivores.remove(animal)
            else:
                raise ValueError("List may only contain Herbivore and Carnivore instances!")

    def randomize_herbs(self):
        """Shuffles the self.herbivores list."""
        random.shuffle(self.herbivores)

    @property
    def animals(self):
        """Combines herbivores list and carnivores list.

        :return: All animal instances in the LandscapeCell instance
        :rtype: list
        """
        return self.herbivores + self.carnivores

    @property
    def herb_count(self):
        """Counts the number of herbivores in the LandscapeCell instance.

        :return: Herbivore count
        :rtype: int
        """
        return len(self.herbivores)

    @property
    def carn_count(self):
        """Counts the number of carnivores in the LandscapeCell instance.

        :return: Carnivore count
        :rtype: int
        """
        return len(self.carnivores)

    @property
    def sorted_carnivores(self):
        """Sorts all `carnivores` by `fitness` from higher to lower.

        :return: Sorted carnivores and corresponding fitness
        :rtype: list
        """
        fitness_dict = {carn: carn.fitness for carn in self.carnivores}
        sorted_tuples = dict(sorted(fitness_dict.items(), key=lambda x: x[1], reverse=True))

        return list(sorted_tuples.keys())

    @property
    def sorted_herbivores(self):
        """Sorts all `herbivores` by `fitness` from lower to higher.

        :return: Sorted herbivores and corresponding fitness values
        :rtype: List of tuples
        """
        fitness_dict = {herb: herb.fitness for herb in self.herbivores}
        sorted_tuples = sorted(fitness_dict.items(), key=lambda x: x[1], reverse=False)

        return sorted_tuples

    @property
    def is_empty(self):
        """Checks if the cell is out of fodder.

        :return: True if LandscapeCell._fodder is zero
        :rtype: bool
        """
        return self.fodder == 0


class Lowland(LandscapeCell):
    """Lowland class for cells.

    :class property:
        - `f_max`: Fodder max to be reset each year. Default value: 800.0

    .. seealso::
        - LandscapeCell.set_params

    """

    params = {"f_max": 800.0}

    def __init__(self):
        super().__init__()  # Initialise landscape class


class Highland(LandscapeCell):
    """Highland class for cells.

    :class property:
        - `f_max`: Fodder max to be reset each year. Default value: 300.0

    .. seealso::
        - LandscapeCell.set_params

    """

    params = {"f_max": 300.0}

    def __init__(self, location=None):
        super().__init__()  # Initialise landscape class


class Desert(LandscapeCell):
    """Desert class for cells.

    :class property:
        - `f_max`: Fodder max to be reset each year. Default value: 0.0

    .. note::
        - Desert cells have a fixed f_max value of 0.0, and LandscapeCell.set_params is invalid for
            instances of this subclass.

    """

    params = {"f_max": 0.0}

    def __init__(self):
        super().__init__()  # Initialise landscape class


class Water:
    """Water class for cells.

    :class property:
        - `is_mainland`: Set to false for Water instances.

    """

    is_mainland = False
    type = "Water"

    def __repr__(self):
        return "Water cell"

    def __str__(self):
        return "Water cell"
