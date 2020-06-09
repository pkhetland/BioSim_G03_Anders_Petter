# -*- coding: utf-8 -*-

"""
A basic interface file containing the minimum requirements for running a simulation
with one animal in one cell.
"""

from src.biosim.animal import Herbivore, Carnivore, Animal
from src.biosim.landscape import Lowland, Highland, Water, Desert

import textwrap

import numpy as np
import random as random
import operator
import matplotlib.pyplot as plt


class Simulation:
    """
    Main interface class for BioSim
    """

    def __init__(self, seed=123, randomize_animals=True, ini_geogr=None):

        if ini_geogr is None:
            self.landscape = {  # Hard-coded map
                (1, 1): Water(),
                (1, 2): Water(),
                (1, 3): Water(),
                (1, 4): Water(),
                (2, 1): Water(),
                (2, 2): Lowland(),  # Mid cell
                (2, 3): Water(),  # Mid cell
                (2, 4): Water(),
                (3, 1): Water(),
                (3, 2): Water(),
                (3, 3): Water(),
                (3, 4): Water()}
        elif type(ini_geogr) == str:
            self.landscape = self.map_from_str(ini_geogr)

        self.year = 0

        random.seed(seed)
        self._randomize_animals = randomize_animals

        # Arguments for plotting
        self._y_herb = None
        self._y_carn = None
        self._herb_line = None
        self._carn_line = None

    @property
    def all_animals(self):
        """

        """
        total_animals = []
        for cell in self.landscape.values():
            if cell.is_mainland:
                total_animals.extend(cell.animals)
        return total_animals

    @property
    def total_animal_count(self):
        return sum([cell.animal_count for cell in self.landscape.values() if cell.is_mainland])

    @property
    def total_herb_count(self):
        return sum([cell.herb_count for cell in self.landscape.values() if cell.is_mainland])

    @property
    def total_carn_count(self):
        return sum([cell.carn_count for cell in self.landscape.values() if cell.is_mainland])

    def run_year_cycle(self):
        """
        Runs through each of the 6 yearly seasons for all cells
        """
        for loc, cell in self.landscape.items():
            if cell.is_mainland:
                #  1. Feeding
                cell.fodder = cell.f_max
                # Randomize animals before feeding
                if self._randomize_animals:
                    cell.randomize_herbs()

                for herb in cell.herbivores:  # Herbivores eat first
                    # if not cell.is_empty:
                    if cell.fodder != 0:
                        herb.eat_fodder(cell)

                for carn in cell.carnivores:  # Carnivores eat last
                    herbs_killed = carn.kill_prey(
                        cell.sorted_herbivores
                    )  # Carnivore hunts for herbivores
                    cell.remove_animals(herbs_killed)  # Remove killed animals from cell

                #  2. Procreation
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

                # 3. Migration
                # Define neighbor cells once:
                neighbor_cells = [
                    self.landscape[(loc[0] - 1, loc[1])],
                    self.landscape[(loc[0], loc[1] + 1)],
                    self.landscape[(loc[0] + 1, loc[1])],
                    self.landscape[(loc[0], loc[1] - 1)]
                ]

                removed_animals = []
                for animal in cell.animals:
                    if animal.migrate():
                        available_neighbors = [neighbor for neighbor in neighbor_cells
                                               if neighbor.is_mainland
                                               ]

                        if len(available_neighbors) > 0:
                            chosen_cell = np.random.choice(available_neighbors)
                            chosen_cell.add_animals([animal])
                            removed_animals.append(animal)

                cell.remove_animals(removed_animals)

                #  4. Aging
                for animal in cell.animals:
                    animal.aging()

                #  5. Loss of weight
                for animal in cell.animals:
                    animal.lose_weight()

                #  6. Death
                dead_animals = []

                for herb in cell.herbivores:
                    if herb.death():
                        Herbivore.subtract_herbivore()
                        dead_animals.append(herb)

                for carn in cell.carnivores:
                    if carn.death():
                        Carnivore.subtract_carnivore()
                        dead_animals.append(carn)

                cell.remove_animals(dead_animals)

                self.year += 1  # Add year to simulation

    def run_simulation(self, num_years):
        """
        :param num_years: number of years to simulate
        """
        self._y_herb = [np.nan for _ in range(num_years)]
        self._y_carn = [np.nan for _ in range(num_years)]

        ax = self.init_plot(num_years)

        for year in range(num_years):
            self.run_year_cycle()

            self._y_herb[year] = self.total_herb_count
            self._y_carn[year] = self.total_carn_count

            self.update_plot(ax)

        print("Simulation complete.")

    def init_plot(self, num_years):
        """
        :param num_years: Number of years to run sim for x-axis
        :type num_years: int
        """
        fig = plt.figure()  # Initiate pyplot
        ax = fig.add_subplot(111)  # Add a single subplot
        (self._herb_line,) = ax.plot(self._y_herb)  # Initiate the herbivore line
        (self._carn_line,) = ax.plot(self._y_carn)  # Initiate the carnivore line
        ax.legend(["Herbivore count", "Carnivore count"])  # Insert legend into plot
        ax.set_xlabel("Simulation year")  # Define x-label
        ax.set_ylabel("Animal count")  # Define y-label
        ax.set_xlim([0, num_years])  # x-limit is set permanently to amount of years to simulate

        plt.ion()  # Activate interactive mode

        return ax

    def update_plot(self, ax):
        """Redraw plot with updated values

        :param ax: pyplot axis
        :type ax: object
        """
        if max(self._y_herb) >= max(self._y_carn):  # Find the biggest count value in either y_herb or y_carn
            ax.set_ylim([0, max(self._y_herb) + 20])  # Set the y-lim to this max
        else:
            ax.set_ylim([0, max(self._y_carn) + 20])  #

        self._herb_line.set_ydata(self._y_herb)
        self._herb_line.set_xdata(range(len(self._y_herb)))
        self._carn_line.set_ydata(self._y_carn)
        self._carn_line.set_xdata(range(len(self._y_carn)))

        plt.pause(1e-6)

    @staticmethod
    def map_from_str(map_str):
        map_dict = {}
        map_str = map_str.splitlines()

        for row_coord, cell_row in enumerate(map_str):
            for col_coord, cell in enumerate(cell_row):
                coord = (row_coord+1, col_coord+1)
                if cell == 'W':
                    map_dict[coord] = Water()
                elif cell == 'L':
                    map_dict[coord] = Lowland()
                elif cell == 'H':
                    map_dict[coord] = Highland()
                elif cell == 'D':
                    map_dict[coord] = Desert()
                else:
                    raise ValueError('Map strings need to be W, L, H og D!')
        return map_dict


if __name__ == "__main__":
    geogr = """WWWW
WLHW
WWWW"""
    sim = Simulation(ini_geogr=geogr)  # Create simple simulation instance

    sim.landscape[(2, 2)].add_animals([Herbivore(age=5, weight=20) for _ in range(200)])
    sim.landscape[(2, 2)].add_animals([Carnivore(age=5, weight=20) for _ in range(40)])

    # Test multi-cell sim
    # sim.landscape[(2, 3)].add_animals([Herbivore(age=5, weight=20) for _ in range(500)])

    sim.run_simulation(num_years=200)

    input("Press enter...")
    # print([herb.fitness for herb in cell.sorted_herbivores])
    # print([carn.fitness for carn in cell.sorted_carnivores])
