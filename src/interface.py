# -*- coding: utf-8 -*-

"""
A basic interface file containing which imports the BioSim class and runs the simulation.
"""

from src.biosim import BioSim

if __name__ == "__main__":
    geogr = """WWWWWW
    WDDDDW
    WDDDDW
    WDDDDW
    WWWWWW"""

    ini_pop = [
        {
            "loc": (3, 3),
            "pop": [{"species": "Herbivore", "age": 5, "weight": 20} for _ in range(1000)]
        },
        # {
        #     "loc": (3, 3),
        #     "pop": [{"species": "Carnivore", "age": 5, "weight": 20} for _ in range(20)]
        # }
    ]

    sim = BioSim(
        seed=123,
        ini_pop=ini_pop,
        island_map=geogr,
        cmax_animals=None,
        ymax_animals=None,
        hist_specs=None,
        plot_graph=True,
        img_base=None
    )  # Create simple simulation instance

    sim.set_animal_parameters('Carnivore', {'omega': 0})
    sim.set_animal_parameters('Herbivore', {'omega': 0})

    sim.set_landscape_parameters('L', {'f_max': 800.0})

    sim.simulate(num_years=400)

    # sim.simulate(num_years=200)
