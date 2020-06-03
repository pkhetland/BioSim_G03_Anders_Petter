# -*- coding: utf-8 -*-

"""
Test set for the initial Lowland class.
"""


import pytest

from src.biosim.Lowland import Lowland


def test_lowland_instance(self):
    """Basic Lowland instance can be created with or without argument"""
    lowland_default = Lowland()
    lowland_100 = Lowland(f_max=100.0)


def test_fodder(self):
    """Fodder attribute of instance can be accessed and has the right value"""
    lowland = Lowland(f_max=200)
    f_max = lowland.f_max  # Get f_max attribute value
    lowland_fodder = lowland.fodder  # Get fodder attribute value
    lowland_fodder = f_max  # Check that initial fodder amount is same a f_max attribute


def test_population(self):
    """Default values for population counts in cell are correct"""
    lowland = Lowland()
    assert lowland.population == 0
    assert lowland.carn_count == 0
    assert lowland.herb_count == 0


def test_add_animal(self):
    """Add a mockup animal to the cell"""
    lowland = Lowland()
    lowland.add_animal('herbivore', {'attr_1': 50.0, 'attr_2': 100.0})
