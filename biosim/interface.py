# -*- coding: utf-8 -*-

"""
A basic interface file containing which imports the BioSim class and runs the simulation.
"""

from src.biosim import BioSim

if __name__ == "__main__":
    geogr = """WWW
    WLW
    WWW"""

    ini_pop = [
        {
            "loc": (2, 2),
            "pop": [{"species": "Herbivore", "age": 5, "weight": 20} for _ in range(50)]
        }
    ]

    sim = BioSim(
        seed=12345,
        ini_pop=ini_pop,
        island_map=geogr,
        cmax_animals=None,
        ymax_animals=None,
        hist_specs=None,
        plot_graph=True,
        img_base='Test'
    )  # Create simple simulation instance

    sim.simulate(num_years=3, img_years=1)

    input('Press enter')

    sim.make_movie()

    # sim.add_population([{
    #         "loc": (2, 2),
    #         "pop": [{"species": "Carnivore", "age": 5, "weight": 20} for _ in range(20)]
    #     }])

    # sim.simulate(num_years=200)
