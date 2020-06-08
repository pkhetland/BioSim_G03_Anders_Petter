# -*- coding: utf-8 -*-

"""
A basic interface file containing the minimum requirements for running a simulation
with one animal in one cell.
"""

from src.biosim.animal import Herbivore, Carnivore
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

    def __init__(self, seed=123, randomize_animals=True):

        self.landscape = {  # Hard-coded map
            (1, 1): Water(),
            (1, 2): Water(),
            (1, 3): Water(),
            (1, 4): Water(),
            (2, 1): Water(),
            (2, 2): Water(),
            (2, 3): Lowland(),  # Mid cell
            (2, 4): Water(),
            (3, 1): Water(),
            (3, 2): Water(),
            (3, 3): Water(),
            (3, 4): Water()
        }

        self.year = 0

        random.seed(seed)
        self._randomize_animals = randomize_animals

        # Arguments for plotting
        self._y_herb = None
        self._y_carn = None
        self._herb_line = None
        self._carn_line = None

    @ property  # Should be replaced with classmethod in animal class
    def total_animals(self):
        total_animals = []
        for cell in self.landscape.values():
            if cell.is_mainland:
                total_animals.extend(cell.animals)
        return total_animals

    @ property  # Should be replaced with classmethod in animal class
    def total_animal_count(self):
        return len(self.total_animals)

    @property  # Should be replaced with classmethod in animal class
    def total_herb_count(self):
        return len([animal for animal in self.total_animals if animal.__class__.__name__ == 'Herbivore'])

    @property  # Should be replaced with classmethod in animal class
    def total_carn_count(self):
        return len([animal for animal in self.total_animals if animal.__class__.__name__ == 'Carnivore'])

    def run_year_cycle(self):
        """
        Runs through each of the 6 yearly seasons for all cells
        """
        for loc, cell in self.landscape.items():
            if cell.__class__.__name__ != "Water":
                #  1. Feeding
                cell.fodder = cell.f_max
                # Randomize animals before feeding
                if self._randomize_animals:
                    cell.randomize()

                for herb in cell.herbivore_list:  # Herbivores eat first
                    if cell.fodder != 0:
                        herb.eat_fodder(cell)

                for carn in cell.carnivore_list:  # Carnivores eat last
                    herbs_killed = carn.kill_prey(
                        cell.sorted_herbivores
                    )  # Carnivore hunts for herbivores
                    for herb in herbs_killed:
                        cell.animals.remove(herb)

                #  2. Procreation
                for herb in cell.herbivore_list:  # Herbivores give birth
                    give_birth, birth_weight = herb.give_birth(cell.herb_count)

                    if give_birth:
                        cell.animals.append(Herbivore(weight=birth_weight, age=0))

                for carn in cell.carnivore_list:  # Carnivores give birth
                    give_birth, birth_weight = carn.give_birth(cell.carn_count)

                    if give_birth:
                        cell.animals.append(Carnivore(weight=birth_weight, age=0))

                #  3. Migration
                removed_animals = []
                for animal in cell.animals:
                    will_migrate = animal.migrate()

                    if will_migrate:
                        top_neighbor = self.landscape[(loc[0]-1, loc[1])]
                        right_neighbor = self.landscape[(loc[0], loc[1]+1)]
                        bot_neighbor = self.landscape[(loc[0]+1, loc[1])]
                        left_neighbor = self.landscape[(loc[0], loc[1]-1)]

                        available_neighbors = [neighbor for neighbor in [top_neighbor,
                                                                         right_neighbor,
                                                                         bot_neighbor,
                                                                         left_neighbor]
                                               if neighbor.__class__.__name__ != 'Water'
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

                for animal in dead_animals:
                    cell.animals.remove(animal)

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
        """
        fig = plt.figure()  # Initiate pyplot
        ax = fig.add_subplot(111)  # Add a single subplot
        (self._herb_line,) = ax.plot(self._y_herb)  # Initiate the herbivore line
        (self._carn_line,) = ax.plot(self._y_carn)  # Initiate the carnivore line
        ax.legend(["Herbivore count", "Carnivore count"])  # Insert legend into plot
        ax.set_xlabel("Simulation year")  # Define x-label
        ax.set_ylabel("Animal count")  # Define y-label
        ax.set_ylim([0, self.total_animal_count])  # Initial y-limit is equal to animal total
        ax.set_xlim([0, num_years])  # x-limit is set permanently to amount of years to simulate

        plt.ion()  # Activate interactive mode

        return ax

    def update_plot(self, ax):
        """
        Redraw plot with updated values
        :param ax: Pyplot axis
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

    # @property
    # def mean_herb_fitness(self):
    #     return np.mean([herb.fitness for herb in self.herbivore_list])
    #
    # @property
    # def mean_carn_fitness(self):
    #     return np.mean([carn.fitness for carn in self.carnivore_list])


if __name__ == "__main__":

    sim = Simulation()  # Create simple simulation instance

    sim.landscape[(2, 3)].add_animals([Herbivore(age=5, weight=20) for _ in range(150)])
    # sim.landscape[(2, 3)].add_animals([Carnivore(age=5, weight=20) for _ in range(40)])

    # Test multi-cell sim
    # sim.landscape[(2, 3)].add_animals([Herbivore(age=5, weight=20) for _ in range(50)])

    sim.run_simulation(num_years=1000)

    input("Press enter...")
    print([herb.fitness for herb in sim.sorted_herbivores])
    print([carn.fitness for carn in sim.sorted_carnivores])

    #herb_carn_single_cell
    # for animal in sim.animals:
    #     print(animal.birth_weight())
