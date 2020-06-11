# -*- coding: utf-8 -*-

"""
A collection of plotting functions for biosim.py
"""

import matplotlib.pyplot as plt
import numpy as np


class Plotting:
    def __init__(self, island, img_base=None):
        # Arguments for plotting
        self._island = island
        self._img_base = None
        self._img_counter = None

        self.y_herb = None
        self.y_carn = None
        self._herb_line = None
        self._carn_line = None
        self._herb_fitness_list = None
        self._carn_fitness_list = None
        self._herb_fitness_line = None
        self._carn_fitness_line = None

        self._ax_main = None
        self._ax_weight = None
        self._ax_fitness = None
        self._ax_age = None
        self._axhm_herb = None
        self._imax_herb = None
        self._axhm_carn = None
        self._imax_carn = None
        self._axim = None
        self._axlg = None

    def init_plot(self, num_years):
        """ Initialize the plot at the beginning of the simulation

        :param num_years: Number of years to run sim for x-axis
        :type num_years: int
        """

        self.y_herb = [np.nan for _ in range(num_years)]
        self.y_carn = [np.nan for _ in range(num_years)]

        fig = plt.figure(figsize=(10, 7), constrained_layout=True)  # Initiate pyplot
        gs = fig.add_gridspec(4, 6)

        self._ax_main = fig.add_subplot(gs[:2, :])  # Add the main subplot
        self._ax_weight = fig.add_subplot(gs[2, :2])
        self._ax_fitness = fig.add_subplot(gs[2, 2:4])
        self._ax_age = fig.add_subplot(gs[2, 4:])
        self._axhm_herb = fig.add_subplot(gs[3, :2])
        self._axhm_carn = fig.add_subplot(gs[3, 2:4])
        self._axim = fig.add_subplot(gs[3, -2:-1])  # Add support subplot
        self._axlg = fig.add_subplot(gs[3, -1])

        self._plot_map(self._island.map_str)
        self._plot_heatmap()

        (self._herb_line,) = self._ax_main.plot(self.y_herb)  # Initiate the herbivore line
        (self._carn_line,) = self._ax_main.plot(self.y_carn)  # Initiate the carnivore line

        self._ax_main.legend(["Herbivore count", "Carnivore count"])  # Insert legend into plot
        self._ax_main.set_xlabel("Simulation year")  # Define x-label
        self._ax_main.set_ylabel("Animal count")  # Define y-label
        self._ax_main.set_xlim(
            [0, num_years]
        )  # x-limit is set permanently to amount of years to simulate

        plt.ion()  # Activate interactive mode

    def update_plot(self,
                    year):
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
        if max(self.y_herb) >= max(
                self.y_carn
        ):  # Find the biggest count value in either y_herb or y_carn
            self._ax_main.set_ylim([0, max(self.y_herb) + 20])  # Set the y-lim to this max
        else:
            self._ax_main.set_ylim([0, max(self.y_carn) + 20])  #

        self._herb_line.set_ydata(self.y_herb)
        self._herb_line.set_xdata(range(len(self.y_herb)))
        self._carn_line.set_ydata(self.y_carn)
        self._carn_line.set_xdata(range(len(self.y_carn)))

        self._ax_weight.clear()
        self._ax_weight.hist(self._island.animal_weights, bins=10)
        self._ax_weight.set_xlim([0, 100])

        self._ax_fitness.clear()
        self._ax_fitness.hist(self._island.animal_fitness, bins=10)
        self._ax_fitness.set_xlim([0, 1])

        self._ax_age.clear()
        self._ax_age.hist(self._island.animal_ages, bins=10)
        self._ax_age.set_xlim([0, 30])

        self._ax_weight.set_title('Weight distribution')
        self._ax_fitness.set_title('Fitness distribution')
        self._ax_age.set_title('Age distribution')

        self._imax_herb.set_data(self._island.herb_pop_matrix)
        self._imax_carn.set_data(self._island.carn_pop_matrix)


        plt.pause(1e-6)

    def _plot_map(self, map_str):
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

        self._axim.imshow(kart_rgb)
        self._axim.set_xticks(range(len(kart_rgb[0])))
        self._axim.set_xticklabels(range(1, 1 + len(kart_rgb[0])))
        self._axim.set_yticks(range(len(kart_rgb)))
        self._axim.set_yticklabels(range(1, 1 + len(kart_rgb)))

        self._axlg.axis('off')
        for ix, name in enumerate(('Water', 'Lowland',
                                   'Highland', 'Desert')):
            self._axlg.add_patch(plt.Rectangle((0., ix * 0.2), 0.3, 0.1,
                                         edgecolor='none',
                                         facecolor=rgb_value[name[0]]))
            self._axlg.text(0.35, ix * 0.2, name, transform=self._axlg.transAxes)

    def _plot_heatmap(self):
        """Create matrix for population and create heatmap

        Create self._axhm_herb and self._axhm_carn?
        """
        self.herb_pop_matrix = [[0 for _ in self._island.unique_cols] for _ in self._island.unique_rows]
        self.carn_pop_matrix = [[0 for _ in self._island.unique_cols] for _ in self._island.unique_rows]

        self._imax_herb = self._axhm_herb.imshow(self._island.herb_pop_matrix,
                               cmap='viridis', interpolation='nearest', vmax=200)
        self._imax_carn = self._axhm_carn.imshow(self._island.carn_pop_matrix,
                               cmap='cividis', interpolation='nearest', vmax=50)
        self._axhm_herb.set_title('Herbivore density')
        self._axhm_carn.set_title('Carnivore density')

        plt.colorbar(self._imax_herb,
                     ax=self._axhm_herb,
                     orientation='vertical')

        plt.colorbar(self._imax_carn,
                     ax=self._axhm_carn,
                     orientation='vertical')

    def _save_graphics(self):
        """Saves graphics to file if file name given. From randviz sim."""

        if self._img_base is None:
            return

        plt.savefig('{base}_{num:05d}.{type}'.format(base=self._img_base,
                                                     num=self._img_ctr,
                                                     type=self._img_fmt))
        self._img_ctr += 1