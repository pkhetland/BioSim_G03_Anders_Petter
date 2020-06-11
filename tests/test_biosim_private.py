# -*- coding: utf-8 -*-

"""
Test set for the initial Lowland class.
"""


import pytest

from src.biosim.animal import Herbivore, Carnivore
from src.biosim.landscape import Lowland, Highland, Water, Desert
from src.biosim.biosim import BioSim


def test_map_from_str():
    sim = BioSim(
        island_map = """WWW
        WLW
        WWW""")
    assert sim.landscape is not None