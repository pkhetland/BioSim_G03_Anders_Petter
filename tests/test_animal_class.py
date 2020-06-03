# -*- coding: utf-8 -*-

"""
Tests for animal class.
"""

def test_eat_fodder():
    """
    Weight of animal shall increase after eating fodder
    Fixed values for food and initial weight
    eat_fodder is an attribute for herbivore class
    """
    herb_before = Herbivore()
    herb_before.eat_fodder = herb_after
    F = 10
    if F > 0:
        assert herb_before.weight < herb_after.weight

