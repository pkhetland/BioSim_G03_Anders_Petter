# -*- coding: utf-8 -*-

from biosim_src.animal import Herbivore, Carnivore
from biosim_src.landscape import Island
from biosim_src.visualization import Plotting

import random as random
import numpy as np
import time
import os
import subprocess
from os import path

# Update these variables to point to your ffmpeg and convert binaries
# If you installed ffmpeg using conda or installed both softwares in
# standard ways on your computer, no changes should be required.
_FFMPEG_BINARY = "ffmpeg"

# update this to the directory and file-name beginning
# for the graphics files
_DEFAULT_GRAPHICS_DIR = os.path.join("..", "data")
_DEFAULT_GRAPHICS_NAME = "biosim"
_DEFAULT_MOVIE_FORMAT = "mp4"  # alternatives: mp4, gif


class BioSim:
    """Main interface class for completing simulations and setting parameters.

            :param island_map: Multi-line string specifying island geography
            :param ini_pop: List of dictionaries specifying initial population
            :param seed: Integer used as random number seed
            :param ymax_animals: Number specifying y-axis limit for graph showing animal numbers
            :param cmax_animals: Dict specifying color-code limits for animal densities
            :param hist_specs: Specifications for histograms, see below
            :param img_base: String with beginning of file name for figures, including path
            :param img_fmt: String with file type for figures, e.g. 'png'

            If ymax_animals is None, the y-axis limit should be adjusted automatically.
            If cmax_animals is None, sensible, fixed default values should be used.
            cmax_animals is a dict mapping species names to numbers, e.g.,
            {'Herbivore': 50, 'Carnivore': 20}.

            hist_specs is a dictionary with one entry per property for which a histogram shall be
            shown.
            For each property, a dictionary providing the maximum value and the bin width must be
            given, e.g.,
            {'weight': {'max': 80, 'delta': 2}, 'fitness': {'max': 1.0, 'delta': 0.05}}
            Permitted properties are 'weight', 'age', 'fitness'.

            If img_base is None, no figures are written to file.
            Filenames are formed as
            '{}_{:05d}.{}'.format(img_base, img_no, img_fmt)
            where img_no are consecutive image numbers starting from 0.
            img_base should contain a path and beginning of a file name.
            """

    def __init__(
        self,
        island_map=None,
        ini_pop=[],    # should have been None
        seed=123,
        ymax_animals=None,
        cmax_animals=None,
        hist_specs=None,
        img_base=None,
        img_fmt="png",
        plot_graph=True,
    ):

        if island_map is None:  # Set default map if none is provided
            map_str = """WWW\nWLW\nWWW"""  # Set default map str
            self._island = Island(map_str)  # Initiate Island
        elif type(island_map) == str:  # Check map str type
            self._island = Island(island_map)  # Initiate Island
        else:
            raise ValueError("Map string needs to be of type str!")

        self._ymax = ymax_animals
        self._cmax = cmax_animals

        self._hist_specs = hist_specs

        self.add_population(ini_pop)  # Add initial population to Island instance

        self._year = 0  # Year counter
        self._year_target = 0  # Number of simulated years total
        self._plot_bool = plot_graph  # Visualization on/off
        self._plot = None  # Plot figure for simulation initialized
        self._img_base = img_base  # Str for naming saved figures
        self._img_fmt = img_fmt  # Format saved figures

        # Set seeds
        random.seed(seed)  # Seed python random seed

    @staticmethod
    def set_animal_parameters(species, params):
        """Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """
        if species == "Herbivore":
            Herbivore.set_params(params)
        elif species == "Carnivore":
            Carnivore.set_params(params)
        else:
            raise ValueError("species needs to be either Herbivore or Carnivore!")

    def set_landscape_parameters(self, landscape, params):
        """Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """
        self._island.set_landscape_params(landscape, params)

    def add_population(self, population):
        """Add a population to specific `island` cells by providing a list of dictionaries.

        :param population: List of dictionaries specifying population

        :Example:
            .. code-block:: python

                 example_pop = {
                    'loc': (4,4),
                    'pop': [
                        {'species': 'Herbivore', 'age': 2, 'weight': 60},
                        {'species': 'Herbivore', 'age': 9, 'weight': 30},
                        {'species': 'Herbivore', 'age': 16, 'weight': 14}
                    ]
                 }
        """
        if type(population) == list:
            for loc_dict in population:  # This loop will be replaced with a more elegant iteration
                new_animals = [
                    Herbivore.from_dict(animal_dict)
                    if animal_dict["species"] == "Herbivore"
                    else Carnivore.from_dict(animal_dict)
                    for animal_dict in loc_dict["pop"]
                ]
                self._island.landscape[loc_dict["loc"]].add_animals(new_animals)
                self._island.count_animals(animal_list=new_animals)
        else:
            raise ValueError(
                f"Pop list needs to be a list of dicts! Was of type " f"{type(population)}."
            )

    def feeding(self, cell):
        """Iterates through each animal in the cell and feeds it according to species.

        :param cell: Current cell object where animals should be fed
        :type cell: object

        .. note::
            `Herbivore` instances will call `eat_fodder` method, while `Carnivore` instances will
            call
            `eat_prey` method.
        """
        cell.fodder = cell.f_max()
        # Randomize animals before feeding
        cell.randomize_herbs()

        for herb in cell.herbivores:  # Herbivores eat first in random order
            if cell.fodder > 0:
                herb.eat_fodder(cell)

        for carn in cell.sorted_carnivores:  # Carnivores eat last, stronger animals first
            herbs_killed = carn.kill_prey(cell.sorted_herbivores)  # Carnivore hunts for herbivores
            cell.remove_animals(herbs_killed)  # Remove killed animals from cell
            self._island.del_animals(num_herbs=len(herbs_killed))

    def procreation(self, cell):
        """Iterates through each animal in the cell and procreates.

        :param cell: Current cell object
        :type cell: object
        """
        new_herbs = []
        new_carns = []
        n_herbs, n_carns = cell.herb_count, cell.carn_count

        for herb in cell.herbivores:  # Herbivores give birth)
            give_birth, birth_weight = herb.give_birth(n_herbs)

            if give_birth:
                new_herbs.append(Herbivore(weight=birth_weight, age=0))

        for carn in cell.carnivores:  # Carnivores give birth
            give_birth, birth_weight = carn.give_birth(n_carns)

            if give_birth:
                new_carns.append(Carnivore(weight=birth_weight, age=0))

        cell.add_animals(new_herbs + new_carns)  # Add new animals to cell

        self._island.count_animals(num_herbs=len(new_herbs), num_carns=len(new_carns))

    @staticmethod
    def migrate(cell):
        """Iterates through each animal in the cell and runs migrate process.
        Animals will only migrate once due to the `has_moved` property.

        :param cell: Current cell object
        :type cell: object
        """
        migrated_animals = []
        for animal in cell.animals:
            if not animal.has_moved and animal.migrate():
                if len(cell.land_cell_neighbors) > 0:
                    chosen_cell = random.choice(cell.land_cell_neighbors)
                    chosen_cell.add_animals([animal])
                    migrated_animals.append(animal)

                animal.has_moved = True

        cell.remove_animals(migrated_animals)
        cell.reset_animals()

    def run_year_cycle(self):
        """Runs through each of the 6 yearly seasons for all cells.

        - Step 1: Animals feed
        - Step 2: Animals procreate
        - Step 3: Animals migrate
        - Step 4: Animals age
        - Step 5: Animals lose weight
        - Step 6: Animals die

        .. seealso::
            - `biosim_src.feeding`
            - `biosim_src.procreation`
            - `biosim_src.migrate`
        """
        for loc, cell in self._island.land_cells.items():
            #  1. Feeding
            self.feeding(cell)

            #  2. Procreation
            self.procreation(cell)

            # 3. Migration
            self.migrate(cell)

            #  4. Aging
            for animal in cell.animals:
                animal.aging()

            #  5. Loss of weight
            for animal in cell.animals:
                animal.lose_weight()

            #  6. Death
            dead_animals = []

            for animal in cell.animals:
                if animal.death():
                    dead_animals.append(animal)

            cell.remove_animals(dead_animals)
            self._island.del_animals(animal_list=dead_animals)

        self._year += 1  # Add year to simulation

    def simulate(self, num_years, vis_years=1, img_years=None):
        """Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files (default: vis_years)

        .. note::

            - When `plot_graph` is set to `True`, plots are initiated and updated.
                Setting`plot_graph` to `False` allows the user to run simulations faster.
            - Image files will be numbered consecutively and used for creating mp4-files.

        .. seealso::

            - `biosim_src.run_year_cycle`
            - `visualization` module

        """
        start_time = time.time()
        self._year_target += num_years

        if self._plot_bool and self._plot is None:
            self._plot = Plotting(
                self._island, cmax=self._cmax, ymax=self._ymax, hist_specs=self._hist_specs
            )
            self._island.update_pop_matrix()
            self._plot.init_plot(num_years)
            self._plot.y_herb[self._year] = self._island.num_herbs
            self._plot.y_carn[self._year] = self._island.num_carns

        elif self._plot_bool:
            self._plot.set_x_axis(self._year_target)
            self._plot.y_herb += [np.nan for _ in range(num_years)]
            self._plot.y_carn += [np.nan for _ in range(num_years)]

        for _ in range(num_years):
            self.run_year_cycle()

            if not self._plot_bool:  # Results are printed if visualization is disabled r
                print(f"Year: {self._year}")
                print(f"Total animal count: {self.num_animals}")
                print(f"Species count: {self.num_animals_per_species}")

            if self._plot_bool:
                self._plot.y_herb[self._year] = self._island.num_herbs
                self._plot.y_carn[self._year] = self._island.num_carns
                if self._year % vis_years == 0:
                    self._island.update_pop_matrix()
                    self._plot.update_plot()

            if self._img_base is not None:
                if img_years is None:
                    if self._year % vis_years == 0:
                        self._plot.save_graphics(self._img_base, self._img_fmt)

                else:
                    if self._year % img_years == 0:
                        self._plot.save_graphics(self._img_base, self._img_fmt)

        finish_time = time.time()

        print("Simulation complete.")
        print("Elapsed time: {:.6} seconds".format(finish_time - start_time))

    @property
    def year(self):
        """ Last year simulated to be used in s and counting.

        :return: Last year simulated
        :rtype: int
        """
        return self._year

    @property
    def num_animals(self):
        """Total number of animals on island.

        :return: Total number of animals in `Island` instance
        :rtype: int
        """
        return self._island.num_animals

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island.

        :return: Number of `herbivores` and `carnivores` on island
        :rtype: dict

        :Example:
            Returned dict example:

            .. code-block:: python

                {'Herbivore': 255, 'Carnivore': 105}
        """
        return {"Herbivore": self._island.num_herbs, "Carnivore": self._island.num_carns}

    def make_movie(self, movie_fmt=_DEFAULT_MOVIE_FORMAT):
        """Creates MPEG4 movie from visualization images saved.

        .. note:
            - Requires ffmpeg

        The movie is stored as img_base + movie_fmt.
        Author: Hans E. Plasser
        """

        if self._img_base is None:
            raise RuntimeError("No filename defined.")

        if movie_fmt == "mp4":
            try:
                # Parameters chosen according to http://trac.ffmpeg.org/wiki/Encode/H.264,
                # section "Compatibility"
                subprocess.check_call(
                    [
                        _FFMPEG_BINARY,
                        "-i",
                        "{}_%05d.png".format(self._img_base),
                        "-y",
                        "-profile:v",
                        "baseline",
                        "-level",
                        "3.0",
                        "-pix_fmt",
                        "yuv420p",
                        "{}.{}".format(self._img_base, movie_fmt),
                    ]
                )
            except subprocess.CalledProcessError as err:
                raise RuntimeError("ERROR: ffmpeg failed with: {}".format(err))
        else:
            raise ValueError("Unknown movie format: " + movie_fmt)

    def image_cleanup(self):
        """Removes created image files after movie is rendered."""
        pass
