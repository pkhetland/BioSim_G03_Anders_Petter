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
import matplotlib.gridspec as gridspec
import seaborn as sns


class Simulation:
    """
    Main interface class for BioSim
    """

    def __init__(self, seed=1, randomize_animals=True, ini_geogr=None):

        self.map_str = ini_geogr
        if self.map_str is None:
            self.landscape = self.map_from_str(
                """WWW
                WLW
                WWW"""
            )
        elif type(self.map_str) == str:
            self.landscape = self.map_from_str(self.map_str)
        else:
            print("Map string needs to be of type str!")

        self.year = 0

        random.seed(seed)
        self._randomize_animals = randomize_animals

        # Arguments for plotting
        self.herb_pop_matrix = None
        self.carn_pop_matrix = None

        self._y_herb = None
        self._y_carn = None
        self._herb_line = None
        self._carn_line = None
        self._herb_fitness_list = None
        self._carn_fitness_list = None
        self._herb_fitness_line = None
        self._carn_fitness_line = None

    @property
    def unique_rows(self):
        return list(set([coord[0] for coord in self.landscape.keys()]))

    @property
    def unique_cols(self):
        return list(set([coord[1] for coord in self.landscape.keys()]))

    @property
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
        for cell in self.landscape.values():
            if cell.is_mainland:
                for herb in cell.herbivores:
                    herb_weights.append(herb.weight)
                for carn in cell.carnivores:
                    carn_weights.append(carn.weight)

        return [herb_weights, carn_weights]

    @property
    def animal_ages(self):
        herb_ages = []
        carn_ages = []
        for cell in self.landscape.values():
            if cell.is_mainland:
                for herb in cell.herbivores:
                    herb_ages.append(herb.age)
                for carn in cell.carnivores:
                    carn_ages.append(carn.age)

        return [herb_ages, carn_ages]

    @property
    def animal_fitness(self):
        herb_fits = []
        carn_fits = []
        for cell in self.landscape.values():
            if cell.is_mainland:
                for herb in cell.herbivores:
                    herb_fits.append(herb.fitness)
                for carn in cell.carnivores:
                    carn_fits.append(carn.fitness)

        return [herb_fits, carn_fits]

    @property
    def carn_weights(self):
        return np.array([
            [carn.weight for carn in cell.herbivores]
            for cell in self.landscape.values() if cell.is_mainland
        ]).flatten()

    @property
    def all_animals(self):
        """
        :return: A list containing all animals in the mainland cells
        :rtype: list
        """
        total_animals = []
        for cell in self.landscape.values():
            if cell.is_mainland:
                total_animals.extend(cell.animals)
        return total_animals

    @property
    def all_herbivores(self):
        """
        :return: A list containing all animals in the mainland cells
        :rtype: list
        """
        all_herbivores = []
        for cell in self.landscape.values():
            if cell.is_mainland:
                all_herbivores.extend(cell.herbivores)
        return all_herbivores

    @property
    def all_carnivores(self):
        """
        :return: A list containing all animals in the mainland cells
        :rtype: list
        """
        all_carnivores = []
        for cell in self.landscape.values():
            if cell.is_mainland:
                all_carnivores.extend(cell.carnivores)
        return all_carnivores

    @property
    def total_animal_count(self):
        """
         :return: Sum of all animal instances in mainland cells
         :rtype: int
        """
        return sum(
            [cell.animal_count for cell in self.landscape.values() if cell.is_mainland]
        )

    @property
    def total_herb_count(self):
        """
         :return: Sum of all herbivore instances in mainland cells
         :rtype: int
        """
        return sum(
            [cell.herb_count for cell in self.landscape.values() if cell.is_mainland]
        )

    @property
    def total_carn_count(self):
        """
         :return: Sum of all carnivore instances in mainland cells
         :rtype: int
        """
        return sum(
            [cell.carn_count for cell in self.landscape.values() if cell.is_mainland]
        )

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
                    self.landscape[(loc[0], loc[1] - 1)],
                ]

                removed_animals = []
                for animal in cell.animals:
                    if animal.migrate():
                        available_neighbors = [
                            neighbor
                            for neighbor in neighbor_cells
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

                for animal in cell.animals:
                    if animal.death():
                        dead_animals.append(animal)

                cell.remove_animals(dead_animals)

                self.year += 1  # Add year to simulation

    def run_simulation(self, num_years):
        """ Runs yearly cycle function for the given number of years
        :param num_years: number of years to simulate
        """
        self._y_herb = [np.nan for _ in range(num_years)]
        self._y_carn = [np.nan for _ in range(num_years)]
        self._herb_fitness_list = []
        self._carn_fitness_list = []

        ax_main, ax_weight, ax_fitness, ax_age, axhm_herb, axhm_carn = self.init_plot(num_years)

        for year in range(num_years):
            print(Carnivore.animal_count)
            print(Herbivore.animal_count)
            self.run_year_cycle()

            self._y_herb[year] = self.total_herb_count
            self._y_carn[year] = self.total_carn_count

            self.update_plot(ax_main, ax_weight, ax_fitness, ax_age, axhm_herb, axhm_carn)

        print("Simulation complete.")

    def init_plot(self, num_years):
        """
        :param num_years: Number of years to run sim for x-axis
        :type num_years: int
        """

        fig = plt.figure(figsize=(12, 7), constrained_layout=True)  # Initiate pyplot
        gs = fig.add_gridspec(4, 6)
        ax_main = fig.add_subplot(gs[:2, :])  # Add the main subplot
        ax_weight = fig.add_subplot(gs[2, :2])

        ax_fitness = fig.add_subplot(gs[2, 2:4])

        ax_age = fig.add_subplot(gs[2, 4:])

        axhm_herb = fig.add_subplot(gs[3, :2])
        axhm_carn = fig.add_subplot(gs[3, 2:4])
        axim = fig.add_subplot(gs[3, -2:-1])  # Add support subplot
        axlg = fig.add_subplot(gs[3, -1])

        self.plot_map(self.map_str, axim, axlg)
        self.plot_heatmap(axhm_herb, axhm_carn)

        (self._herb_line,) = ax_main.plot(self._y_herb)  # Initiate the herbivore line
        (self._carn_line,) = ax_main.plot(self._y_carn)  # Initiate the carnivore line
        # self._herb_fitness_line = ax_2.hist(self._herb_fitness_list)
        # self._carn_fitness_line = ax_2.hist(self._carn_fitness_list)
        ax_main.legend(["Herbivore count", "Carnivore count"])  # Insert legend into plot
        ax_main.set_xlabel("Simulation year")  # Define x-label
        ax_main.set_ylabel("Animal count")  # Define y-label
        ax_main.set_xlim(
            [0, num_years]
        )  # x-limit is set permanently to amount of years to simulate

        plt.ion()  # Activate interactive mode

        return ax_main, ax_weight, ax_fitness, ax_age, axhm_herb, axhm_carn

    def update_plot(self, ax_1, ax_weight, ax_fitness, ax_age, axhm_herb, axhm_carn):
        """Redraw plot with updated values

        :param ax_1: pyplot axis
        :type ax_1: object
        """
        if max(self._y_herb) >= max(
            self._y_carn
        ):  # Find the biggest count value in either y_herb or y_carn
            ax_1.set_ylim([0, max(self._y_herb) + 20])  # Set the y-lim to this max
        else:
            ax_1.set_ylim([0, max(self._y_carn) + 20])  #

        self._herb_line.set_ydata(self._y_herb)
        self._herb_line.set_xdata(range(len(self._y_herb)))
        self._carn_line.set_ydata(self._y_carn)
        self._carn_line.set_xdata(range(len(self._y_carn)))

        # ax_weight.clear()
        # ax_weight.hist(self.animal_weights, bins=10)
        #
        # ax_fitness.clear()
        # ax_fitness.hist(self.animal_fitness, bins=10)
        #
        # ax_age.clear()
        # ax_age.hist(self.animal_ages, bins=10)
        #
        # ax_weight.set_title('Weight distribution')
        # ax_fitness.set_title('Fitness distribution')
        # ax_age.set_title('Age distribution')
        #
        # if self.year % 5 == 1:
        #     self.update_pop_matrix
        #     axhm_herb.clear(), axhm_carn.clear()
        #     axhm_herb.imshow(self.herb_pop_matrix, cmap='hot')
        #     axhm_carn.imshow(self.carn_pop_matrix, cmap='hot')
        #     axhm_herb.set_title('Herbivore density')
        #     axhm_carn.set_title('Carnivore density')

        plt.pause(1e-6)

    @staticmethod
    def plot_map(map_str, axim, axlg):
        """Author: Hans

        """

        #                   R    G    B
        rgb_value = {'W': (0.0, 0.0, 1.0),  # blue
                     'L': (0.0, 0.6, 0.0),  # dark green
                     'H': (0.5, 1.0, 0.5),  # light green
                     'D': (1.0, 1.0, 0.5)}  # light yellow

        kart_rgb = [[rgb_value[column] for column in row.strip()]
                    for row in map_str.splitlines()]

        axim.imshow(kart_rgb)
        axim.set_xticks(range(len(kart_rgb[0])))
        axim.set_xticklabels(range(1, 1 + len(kart_rgb[0])))
        axim.set_yticks(range(len(kart_rgb)))
        axim.set_yticklabels(range(1, 1 + len(kart_rgb)))

        axlg.axis('off')
        for ix, name in enumerate(('Water', 'Lowland',
                                   'Highland', 'Desert')):
            axlg.add_patch(plt.Rectangle((0., ix * 0.2), 0.3, 0.1,
                                         edgecolor='none',
                                         facecolor=rgb_value[name[0]]))
            axlg.text(0.35, ix * 0.2, name, transform=axlg.transAxes)

    def plot_heatmap(self, axhm_herb, axhm_carn):
        """Create matrix for population and create heatmap
        """
        self.herb_pop_matrix = [[0 for _ in self.unique_cols] for _ in self.unique_rows]
        self.carn_pop_matrix = [[0 for _ in self.unique_cols] for _ in self.unique_rows]

        axhm_herb.imshow(self.herb_pop_matrix)
        axhm_carn.imshow(self.carn_pop_matrix)
        axhm_herb.set_title('Herbivore density')
        axhm_carn.set_title('Carnivore density')
        axhm_carn.set_xticks(range(len(self.unique_cols)))
        axhm_carn.set_xticklabels(range(1, len(self.unique_cols)+1))
        axhm_carn.set_yticks(range(len(self.unique_rows)))
        axhm_carn.set_yticklabels(range(1, len(self.unique_rows)+1))
        axhm_herb.set_xticks(range(len(self.unique_cols)))
        axhm_herb.set_xticklabels(range(1, len(self.unique_cols)+1))
        axhm_herb.set_yticks(range(len(self.unique_rows)))
        axhm_herb.set_yticklabels(range(1, len(self.unique_rows)+1))

    @staticmethod
    def map_from_str(map_str):
        """The sim takes in a map str and converts it into a dictionary of
        coord keys and class values

        :param map_str: A multi-line string representing cell classes and coordinates
        :type map_str: str

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


if __name__ == "__main__":
    geogr = """WWWWWW
    WLWDLW
    WHDWDW
    WWWWWW"""
    sim = Simulation(ini_geogr=geogr)  # Create simple simulation instance

    sim.landscape[(2, 2)].add_animals([Herbivore(age=5, weight=20) for _ in range(150)])
    sim.landscape[(2, 2)].add_animals([Carnivore(age=5, weight=20) for _ in range(40)])

    # Test multi-cell sim
    sim.landscape[(2, 5)].add_animals([Herbivore(age=5, weight=20) for _ in range(20)])

    sim.run_simulation(num_years=50)

    input("Press enter...")
    # print([herb.fitness for herb in cell.sorted_herbivores])
    # print([carn.fitness for carn in cell.sorted_carnivores])
