# -*- coding: utf-8 -*-

"""
Tests for animal class.
"""


class TestAnimal:

    """
    Tests for animal class
    """

    def test_eat_fodder(self):
        """
        Weight of animal shall increase after eating fodder

        """
        herb = Herbivore()
        herb_after = herb.eat_fodder()
        F = 10
        if F > 0:
            assert herb.weight() < herb_after.weight()

class TestHerbivore:

    """
    Tests for herbivore class
    """

    def test_constructor(self):
        """Herbivore can be created"""
        herb = Herbivore()
        assert isinstance(herb, Herbivore)
