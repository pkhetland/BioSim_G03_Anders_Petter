# -*- coding: utf-8 -*-

"""
A basic interface file containing which imports the BioSim class and runs the simulation.
"""

from src.biosim import BioSim

if __name__ == "__main__":
    geogr = "WWWW\nWLHW\nWWWW"
    # geogr = """WWW
    # WLW
    # WWW"""

    ini_pop = [
        {
            "loc": (2, 2),
            "pop": [{"species": "Herbivore", "age": 5, "weight": 30} for _ in range(150)]
        },
        {
            "loc": (2, 2),
            "pop": [{"species": "Carnivore", "age": 5, "weight": 20} for _ in range(40)]
        }
    ]

    ini_carns = []

    # cmax = {'Herbivore': 500, 'Carnivore': 200}

    sim = BioSim(
        seed=123,
        ini_pop=ini_pop,
        island_map=geogr,
        cmax_animals=None,
        ymax_animals=None,
        hist_specs={'weight': {'max': 80, 'delta': 2}, 'fitness': {'max': 1.0, 'delta': 0.05}},
        plot_graph=True,
        img_base='test'
    )  # Create simple simulation instance

    # sim.set_animal_parameters('Carnivore', {'omega': 0})
    # sim.set_animal_parameters('Herbivore', {'omega': 0})

    sim.set_landscape_parameters('L', {'f_max': 800.0})

    sim.simulate(num_years=2, vis_years=1, img_years=1)

    # sim.simulate(num_years=200)
