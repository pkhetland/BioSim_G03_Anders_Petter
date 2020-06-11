# -*- coding: utf-8 -*-

"""
A basic interface file containing which imports the BioSim class and runs the simulation.
"""

from src.biosim import BioSim

if __name__ == "__main__":
    geogr = """WWWWWWW
               WDDDDDW
               WDDDDDW
               WDDDDDW
               WDDDDDW
               WDDDDDW
               WWWWWWW"""

    ini_herbs = [{
            "loc": (4, 4),
            "pop": [{"species": "Herbivore", "age": 5, "weight": 20} for _ in range(1000)]
    }]

    ini_carns = [{
        "loc": (3, 3),
        "pop": [{"species": "Carnivore", "age": 5, "weight": 20} for _ in range(40)]
    }]

    sim = BioSim(
        seed=123, ini_pop=ini_herbs, island_map=geogr, plot_graph=True
    )  # Create simple simulation instance

    # sim.add_population(ini_carns)

    sim.set_animal_parameters('Carnivore', {'omega': 0})
    sim.set_animal_parameters('Herbivore', {'omega': 0})

    # sim.set_landscape_parameters('L', {'f_max': 800.0})

    sim.simulate(num_years=1000)

    # sim.simulate(num_years=20)
