# -*- coding: utf-8 -*-

"""
A basic interface file containing which imports the BioSim class and runs the simulation.
"""

from src.biosim import BioSim

if __name__ == "__main__":
    geogr = """WWWWWWW
               WDLDLDW
               WLHHLHW
               WWWWWWW"""

    ini_herbs = [{
            "loc": (2, 2),
            "pop": [{"species": "Herbivore", "age": 5, "weight": 20} for _ in range(150)]
    }]

    ini_carns = [{
        "loc": (2, 2),
        "pop": [{"species": "Carnivore", "age": 5, "weight": 20} for _ in range(40)]
    }]

    sim = BioSim(
        seed=123, ini_pop=ini_herbs, island_map=geogr, plot_graph=False
    )  # Create simple simulation instance

    sim.add_population(ini_carns)

    # sim.set_animal_parameters('Carnivore', {'omega': 0, 'xi': 1.8})
    # sim.set_animal_parameters('Herbivore', {'omega': 0, 'xi': 1.8})

    # sim.set_landscape_parameters('L', {'f_max': 800.0})

    sim.simulate(num_years=20)

    sim.simulate(num_years=20)
