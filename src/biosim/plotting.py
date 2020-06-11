# -*- coding: utf-8 -*-

"""
A collection of plotting functions for biosim.py
"""

import matplotlib.pyplot as plt
import numpy as np


class Plotting:
    def __init__(self, island):
        # Arguments for plotting
        self._island = island

        self._y_herb = None
        self._y_carn = None
        self._herb_line = None
        self._carn_line = None
        self._herb_fitness_list = None
        self._carn_fitness_list = None
        self._herb_fitness_line = None
        self._carn_fitness_line = None

    def init_plot(self, num_years):
        """ Initialize the plot at the beginning of the simulation

        :param num_years: Number of years to run sim for x-axis
        :type num_years: int
        """

        self._y_herb = [np.nan for _ in range(num_years)]
        self._y_carn = [np.nan for _ in range(num_years)]

        fig = plt.figure(figsize=(10, 7), constrained_layout=True)  # Initiate pyplot
        gs = fig.add_gridspec(4, 6)

        ax_main = fig.add_subplot(gs[:2, :])  # Add the main subplot
        ax_weight = fig.add_subplot(gs[2, :2])
        ax_fitness = fig.add_subplot(gs[2, 2:4])
        ax_age = fig.add_subplot(gs[2, 4:])
        axhm_herb = fig.add_subplot(gs[3, :2])
        axhm_carn = fig.add_subplot(gs[3, 2:4])
        axim = fig.add_subplot(gs[3, -2:-1])  # Add support subplot
        axlg = fig.add_subplot(gs[3, -1])

        self.plot_map(self._island.map_str, axim, axlg)
        self.plot_heatmap(axhm_herb, axhm_carn)

        (self._herb_line,) = ax_main.plot(self._y_herb)  # Initiate the herbivore line
        (self._carn_line,) = ax_main.plot(self._y_carn)  # Initiate the carnivore line

        ax_main.legend(["Herbivore count", "Carnivore count"])  # Insert legend into plot
        ax_main.set_xlabel("Simulation year")  # Define x-label
        ax_main.set_ylabel("Animal count")  # Define y-label
        ax_main.set_xlim(
            [0, num_years]
        )  # x-limit is set permanently to amount of years to simulate

        plt.ion()  # Activate interactive mode

        return ax_main, ax_weight, ax_fitness, ax_age, axhm_herb, axhm_carn

    def update_plot(self,
                    year,
                    ax_main,
                    ax_weight,
                    ax_fitness,
                    ax_age,
                    axhm_herb,
                    axhm_carn):
        """Redraw plot with updated values

        :param ax_main: pyplot axis for line plots
        :type ax_main: object
        :param ax_weight: pyplot axis weight histogram
        :type ax_weight: object
        :param ax_fitness: pyplot axis for fitness histogram
        :type ax_fitness: object
        :param ax_age: pyplot axis for age histogram
        :type ax_age: object
        :param axhm_herb: pyplot axis for herbivore density heatmap
        :type axhm_herb: object
        :param axhm_carn: pyplot axis for carnivore density heatmap
        :type axhm_carn: object
        """
        if max(self._y_herb) >= max(
                self._y_carn
        ):  # Find the biggest count value in either y_herb or y_carn
            ax_main.set_ylim([0, max(self._y_herb) + 20])  # Set the y-lim to this max
        else:
            ax_main.set_ylim([0, max(self._y_carn) + 20])  #

        self._herb_line.set_ydata(self._y_herb)
        self._herb_line.set_xdata(range(len(self._y_herb)))
        self._carn_line.set_ydata(self._y_carn)
        self._carn_line.set_xdata(range(len(self._y_carn)))

        ax_weight.clear()
        ax_weight.hist(self._island.animal_weights, bins=10)
        ax_weight.set_xlim([0, 100])

        ax_fitness.clear()
        ax_fitness.hist(self._island.animal_fitness, bins=10)
        ax_fitness.set_xlim([0, 1])

        ax_age.clear()
        ax_age.hist(self._island.animal_ages, bins=10)
        ax_age.set_xlim([0, 30])

        ax_weight.set_title('Weight distribution')
        ax_fitness.set_title('Fitness distribution')
        ax_age.set_title('Age distribution')

        if year % 5 == 0:

            axhm_herb.clear(), axhm_carn.clear()
            axhm_herb.imshow(self._island.herb_pop_matrix, cmap='hot')
            axhm_carn.imshow(self._island.carn_pop_matrix, cmap='hot')
            axhm_herb.set_title('Herbivore density')
            axhm_carn.set_title('Carnivore density')

        plt.pause(1e-6)


    @staticmethod
    def plot_map(map_str, axim, axlg):
        """Author: Hans

        :param map_str: Multi-line string containing letters symbolizing the landscape
        :type map_str: str
        :param axim: Image axis for plotting map
        :type axim: object
        :param axlg: Legend axis for plotting legend blocks
        :type axlg: object
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

        Create self.axhm_herb and self.axhm_carn?
        """
        self.herb_pop_matrix = [[0 for _ in self._island.unique_cols] for _ in self._island.unique_rows]
        self.carn_pop_matrix = [[0 for _ in self._island.unique_cols] for _ in self._island.unique_rows]

        axhm_herb.imshow(self.herb_pop_matrix)
        axhm_carn.imshow(self.carn_pop_matrix)
        axhm_herb.set_title('Herbivore density')

        axhm_carn.set_title('Carnivore density')
        axhm_carn.set_xticks(range(len(self._island.unique_cols)))
        axhm_carn.set_xticklabels(range(1, len(self._island.unique_cols) +1))
        axhm_carn.set_yticks(range(len(self._island.unique_rows)))
        axhm_carn.set_yticklabels(range(1, len(self._island.unique_rows) +1))

        axhm_herb.set_xticks(range(len(self._island.unique_cols)))
        axhm_herb.set_xticklabels(range(1, len(self._island.unique_cols ) +1))
        axhm_herb.set_yticks(range(len(self._island.unique_rows)))
        axhm_herb.set_yticklabels(range(1, len(self._island.unique_rows ) +1))
