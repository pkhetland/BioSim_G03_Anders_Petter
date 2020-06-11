# -*- coding: utf-8 -*-

"""
A basic interface file containing the minimum requirements for running a simulation
with one animal in one cell.
"""

from src.biosim.animal import Herbivore, Carnivore, Animal
from src.biosim.landscape import Island, Lowland, Highland, Water, Desert
from src.biosim.plotting import Plotting

import numpy as np
import random as random


class Simulation:
    """
    Main interface class for BioSim
    """

    def __init__(self, seed=123, randomize_animals=True, ini_geogr=None, plot_graph=False):

        if ini_geogr is None:
            map_str = """WWW
                         WLW
                         WWW"""
            self._island = Island(map_str)
        elif type(ini_geogr) == str:
            self._island = Island(ini_geogr)
        else:
            print("Map string needs to be of type str!")

        self._year = 0

        random.seed(seed)
        self._randomize_animals = randomize_animals
        self._plot = plot_graph

    @property
    def year(self):
        return self._year

    @property
    def island(self):
        return self._island

    def feeding(self, cell):
        """Iterates through each animal in the cell and feeds it according to species

        :param cell: Current cell object
        :type cell: object
        """
        cell.fodder = cell.f_max
        # Randomize animals before feeding
        if self._randomize_animals:
            cell.randomize_herbs()

        for herb in cell.herbivores:  # Herbivores eat first
            if cell.fodder != 0:
                herb.eat_fodder(cell)

        for carn in cell.carnivores:  # Carnivores eat last
            herbs_killed = carn.kill_prey(
                cell.sorted_herbivores
            )  # Carnivore hunts for herbivores
            cell.remove_animals(herbs_killed)  # Remove killed animals from cell

    @staticmethod
    def procreation(cell):
        """Iterates through each animal in the cell and procreates

        :param cell: Current cell object
        :type cell: object
        """
        new_animals = []
        n_herbs, n_carns = cell.herb_count, cell.carn_count

        for herb in cell.herbivores:  # Herbivores give birth)
            give_birth, birth_weight = herb.give_birth(n_herbs)

            if give_birth:
                new_animals.append(Herbivore(weight=birth_weight, age=0))

        for carn in cell.carnivores:  # Carnivores give birth
            give_birth, birth_weight = carn.give_birth(n_carns)

            if give_birth:
                new_animals.append(Carnivore(weight=birth_weight, age=0))

        cell.add_animals(new_animals)  # Add new animals to cell

    def migrate(self, loc, cell, all_migrated_animals):
        """Iterates through each animal in the cell and migrates

        :param loc: Coordinate of current cell
        :type loc: tuple
        :param cell: Current cell object
        :type cell: object
        """
        # Define neighbor cells once:
        neighbor_cells = [
            self.island.landscape[(loc[0] - 1, loc[1])],
            self.island.landscape[(loc[0], loc[1] + 1)],
            self.island.landscape[(loc[0] + 1, loc[1])],
            self.island.landscape[(loc[0], loc[1] - 1)],
        ]

        migrated_animals = []
        for animal in cell.animals:
            if animal not in all_migrated_animals:
                if animal.migrate():
                    available_neighbors = [
                        neighbor
                        for neighbor in neighbor_cells
                        if neighbor.is_mainland
                    ]

                    if len(available_neighbors) > 0:
                        chosen_cell = random.choice(available_neighbors)
                        chosen_cell.add_animals([animal])
                        migrated_animals.append(animal)

        cell.remove_animals(migrated_animals)
        return migrated_animals

    def run_year_cycle(self):
        """
        Runs through each of the 6 yearly seasons for all cells
        """
        all_migrated_animals = []
        for loc, cell in self.island.land_cells.items():
            #  1. Feeding
            self.feeding(cell)

            #  2. Procreation
            self.procreation(cell)

            # 3. Migration
            migrated_animals = self.migrate(loc, cell, all_migrated_animals)

            all_migrated_animals.extend(migrated_animals)

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

        self._year += 1  # Add year to simulation

    def run_simulation(self, num_years):
        """ Runs yearly cycle function for the given number of years

        :param num_years: number of years to simulate
        :type num_years: int
        """

        if self._plot:
            plot = Plotting(self.island)
            self.island.update_pop_matrix(Herbivore.instance_count, Carnivore.instance_count)
            ax_main, ax_weight, ax_fitness, ax_age, axhm_herb, axhm_carn = plot.init_plot(num_years)

        for year in range(num_years):
            self.run_year_cycle()
            print(f'Year: {self.year}')
            print(f'Animals: {Animal.instance_count}')
            print(f'Herbivores: {Herbivore.instance_count}')
            print(f'Carnivore: {Carnivore.instance_count}')

            if self._plot:
                plot._y_herb[year] = Herbivore.instance_count
                plot._y_carn[year] = Carnivore.instance_count
                plot.update_plot(self._year,
                                 ax_main,
                                 ax_weight,
                                 ax_fitness,
                                 ax_age,
                                 axhm_herb,
                                 axhm_carn)

        print("Simulation complete.")


if __name__ == "__main__":
    geogr = """WWW
    WLW
    WWW"""

    sim = Simulation(ini_geogr=geogr, plot_graph=False)  # Create simple simulation instance
    #
    sim.island.landscape[(2, 2)].add_animals([Herbivore(age=5, weight=20) for _ in range(50)])
    sim.island.landscape[(2, 2)].add_animals([Carnivore(age=5, weight=20) for _ in range(20)])

    # Test multi-cell sim
    # sim.landscape[(2, 3)].add_animals([Herbivore(age=5, weight=20) for _ in range(20)])

    sim.run_simulation(num_years=200)
    # input("Press enter...")