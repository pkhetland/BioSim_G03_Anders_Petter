# -*- coding: utf-8 -*-

"""
Test set for the initial Lowland class.
"""


import pytest

from src.biosim.Lowland import Lowland


def test_lowland_instance():
    """Basic Lowland instance can be created with or without argument"""
    lowland_default = Lowland()
    lowland_100 = Lowland(f_max=100.0)


def test_fodder():
    """Fodder attribute of instance can be accessed and has the right value"""
    lowland = Lowland(f_max=200)
    f_max = lowland.f_max  # Get f_max attribute value
    lowland_fodder = lowland.fodder  # Get fodder attribute value
    lowland_fodder = f_max  # Check that initial fodder amount is same a f_max attribute


def test_population():
    """Default values for population counts in cell are correct"""
    lowland = Lowland()
    assert len(lowland.population) == 0
    assert lowland.carn_count == 0
    assert lowland.herb_count == 0


def test_add_animal():
    """Add a mock up animal to the cell"""
    lowland = Lowland()
    lowland.add_animal('Herbivore', 2, 20)


def test_animal_count():
    """Add animals and test count"""
    lowland = Lowland()
    lowland.add_animal('Herbivore', 2, 20)
    lowland.add_animal('Carnivore', 10, 100)
    lowland.add_animal('Carnivore', 5, 50)

    assert lowland.population_count == 3
    assert lowland.carn_count == 2
    assert lowland.herb_count == 1


def test_lowland_location():
    lowland = Lowland(location=(1, 2))
    assert lowland.location == (1, 2)
