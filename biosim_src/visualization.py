# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt
import numpy as np


class Plotting:
    """Plotting class to be used in biosim.py.
    """
    def __init__(self, island, cmax=None, ymax=None, hist_specs=None):
        self._island = island
        self._img_base = None
        self._img_ctr = 0

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
        self._weight_hist = None
        self._fitness_hist = None
        self._age_hist = None
        self._axhm_herb = None
        self._imax_herb = None
        self._axhm_carn = None
        self._imax_carn = None
        self._axim = None
        self._axlg = None

        self._ymax = ymax

        self._cmax = cmax
        if self._cmax is None:
            self._cmax = {"Herbivore": 200, "Carnivore": 50}

        self._cmax_herb = self._cmax["Herbivore"]
        self._cmax_carn = self._cmax["Carnivore"]

        if hist_specs is None:
            self._hist_specs = {
                "weight": {"max": 80, "delta": 2},
                "fitness": {"max": 1.0, "delta": 0.05},
                "age": {"max": 80, "delta": 2},
            }
        else:
            self._hist_specs = hist_specs

    def init_plot(self, num_years):
        """Initialize the plot at the beginning of the simulation.

        :param num_years: Number of years to run sim for x-axis
        :type num_years: int
        """
        self.y_herb = [np.nan for _ in range(num_years + 1)]
        self.y_carn = [np.nan for _ in range(num_years + 1)]

        fig = plt.figure(figsize=(10, 7), constrained_layout=True)  # Initiate pyplot
        gs = fig.add_gridspec(4, 6)

        self._ax_main = fig.add_subplot(gs[:2, :])  # Add the main subplot
        self._ax_weight = fig.add_subplot(gs[2, :2])  # Add weight subplot
        self._ax_fitness = fig.add_subplot(gs[2, 2:4])  # Add fitness subplot
        self._ax_age = fig.add_subplot(gs[2, 4:])  # Add age subplot
        self._axhm_herb = fig.add_subplot(gs[3, :2])  # Add herb heatmap subplot
        self._axhm_carn = fig.add_subplot(gs[3, 2:4])  # Add carn heatmap subplot
        self._axim = fig.add_subplot(gs[3, -2:-1])  # Add map subplot
        self._axlg = fig.add_subplot(gs[3, -1])  # Add map legend subplot

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

        if self._ymax is not None:
            self._ax_main.set_ylim([0, self._ymax])

        plt.ion()  # Activate interactive mode

    def set_x_axis(self, years_target):
        self._ax_main.set_xlim([0, years_target])  # Update x_limit when several simulations are run

    def update_plot(self):
        """Redraw plot with updated values.
        """
        if self._ymax is None:
            if max(self.y_herb) >= max(
                self.y_carn
            ):  # Find the biggest count value in either y_herb or y_carn
                self._ax_main.set_ylim([0, max(self.y_herb) + 20])  # Set y-lim
            else:
                self._ax_main.set_ylim([0, max(self.y_carn) + 20])  # Set y-lim

        if self._island.num_carns > 0 or self._island.num_herbs > 0:
            weight_data = self._island.animal_weights
            weight_max = int(max(max(weight_data)))
            weight_min = int(min(min(weight_data)))
            weight_delta = self._hist_specs["weight"]["delta"]
            self._ax_weight.clear()
            self._weight_hist = self._ax_weight.hist(
                weight_data, range(weight_min, weight_max + int(weight_delta), weight_delta),
            )
            self._ax_weight.set_xlim([0, self._hist_specs["weight"]["max"]])

            fitness_data = self._island.animal_fitness
            fitness_delta = self._hist_specs["fitness"]["delta"]

            self._ax_fitness.clear()
            self._ax_fitness.hist(fitness_data, bins=np.arange(0, 1 + fitness_delta, fitness_delta))

            self._ax_fitness.set_xlim([0, self._hist_specs["fitness"]["max"]])

            age_data = self._island.animal_ages
            age_max = int(max(max(age_data)))
            age_min = int(min(min(age_data)))
            age_delta = self._hist_specs["age"]["delta"]
            self._ax_age.clear()
            self._ax_age.hist(age_data, bins=range(age_min, age_max + int(age_delta), age_delta))
            self._ax_age.set_xlim([0, self._hist_specs["age"]["max"]])

            self._herb_line.set_ydata(self.y_herb)
            self._herb_line.set_xdata(range(len(self.y_herb)))
            self._carn_line.set_ydata(self.y_carn)
            self._carn_line.set_xdata(range(len(self.y_carn)))

            self._ax_weight.set_title("Weight distribution")
            self._ax_fitness.set_title("Fitness distribution")
            self._ax_age.set_title("Age distribution")

        self._imax_herb.set_data(self._island.herb_pop_matrix)
        self._imax_carn.set_data(self._island.carn_pop_matrix)

        plt.pause(1e-6)

    def _plot_map(self, map_str):
        """Author: Hans E. Plasser

        :param map_str: Multi-line string containing letters symbolizing the landscape
        :type map_str: str
        """

        rgb_value = {
            #      R    G    B
            "W": (0.0, 0.0, 1.0),  # blue
            "L": (0.0, 0.6, 0.0),  # dark green
            "H": (0.5, 1.0, 0.5),  # light green
            "D": (1.0, 1.0, 0.5),
        }  # light yellow

        kart_rgb = [[rgb_value[column] for column in row.strip()] for row in map_str.splitlines()]

        self._axim.imshow(kart_rgb)
        self._axim.set_xticks(range(len(kart_rgb[0])))
        self._axim.set_xticklabels(range(1, 1 + len(kart_rgb[0])))
        self._axim.set_yticks(range(len(kart_rgb)))
        self._axim.set_yticklabels(range(1, 1 + len(kart_rgb)))

        for label in self._axim.xaxis.get_ticklabels()[1::2]:
            label.set_visible(False)

        self._axlg.axis("off")
        for ix, name in enumerate(("Water", "Lowland", "Highland", "Desert")):
            self._axlg.add_patch(
                plt.Rectangle(
                    (0.0, ix * 0.2), 0.3, 0.1, edgecolor="none", facecolor=rgb_value[name[0]]
                )
            )
            self._axlg.text(0.35, ix * 0.2, name, transform=self._axlg.transAxes)

    def _plot_heatmap(self):
        """Create matrix for population and initiate heatmap.
        """
        self.herb_pop_matrix = [
            [0 for _ in self._island.unique_cols] for _ in self._island.unique_rows
        ]
        self.carn_pop_matrix = [
            [0 for _ in self._island.unique_cols] for _ in self._island.unique_rows
        ]

        self._imax_herb = self._axhm_herb.imshow(
            self._island.herb_pop_matrix,
            cmap="viridis",
            interpolation="nearest",
            vmax=self._cmax_herb,
        )
        self._imax_carn = self._axhm_carn.imshow(
            self._island.carn_pop_matrix,
            cmap="cividis",
            interpolation="nearest",
            vmax=self._cmax_carn,
        )
        self._axhm_herb.set_title("Herbivore density")
        self._axhm_carn.set_title("Carnivore density")

        plt.colorbar(self._imax_herb, ax=self._axhm_herb, orientation="vertical")

        plt.colorbar(self._imax_carn, ax=self._axhm_carn, orientation="vertical")

    def save_graphics(self, img_base, img_fmt):
        """Saves graphics to file if file name given. Modified from Hans E. Plasser."""

        if img_base is None:
            return

        plt.savefig(
            "{base}_{num:05d}.{type}".format(base=img_base, num=self._img_ctr, type=img_fmt)
        )
        self._img_ctr += 1
