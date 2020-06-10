# -*- coding: utf-8 -*-

"""
Test set for the initial Lowland class.
"""


import pytest

from src.biosim.animal import Herbivore, Carnivore
from src.biosim.landscape import Lowland, Highland, Water, Desert
from src.biosim.interface import Simulation


def test_map_from_str():
    sim = Simulation(
        ini_geogr = """WWW
        WLW
        WWW""")
    assert sim.landscape is not None