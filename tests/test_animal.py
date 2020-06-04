# -*- coding: utf-8 -*-

"""
Tests for animal class.
"""
from src.biosim.animal import Herbivore

class TestAnimal:

    """
    Tests for animal class
    """


class TestHerbivore:

    """
    Tests for herbivore class
    """

    def test_constructor(self):
        """Herbivore can be created"""
        herb = Herbivore()
        assert isinstance(herb, Herbivore)

    def test_eat_fodder(self):
        """
        Weight of animal shall increase after eating fodder

        """
        herb = Herbivore(landscape=None, weight=10, age=0)
        herb_weight = herb.weight
        herb.eat_fodder
        # new weight
        herb_weight_after = herb.weight
        assert herb_weight < herb_weight_after
