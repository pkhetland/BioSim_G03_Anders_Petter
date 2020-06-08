# -*- coding: utf-8 -*-

"""
Tests for animal class.
"""
from src.biosim.animal import Herbivore, Carnivore, Animal
from src.biosim.interface import Simulation
from src.biosim.landscape import Lowland

import pytest


class TestAnimal:

    """
    Tests for animal class
    """
    @pytest.fixture
    def set_parameters(self, death_prob=1):
        # Comment AH. Need a function to create animals

        # Probability of dying 1

        self.death_prob = death_prob



    def test_certain_death(self):
        """
        Test that the animal always must die given death_prob = 1
        100 Herbivore instances all must die
        See examples/biolab/test_bacteria.py
        NOT WORKING, test fails

        """
        h = Herbivore()
        for _ in range(100):
            assert h.death()



    def test_constructor(self):
        """
        Herbivore can be created
        """
        herb = Herbivore(weight=10, age=0)
        carn = Carnivore()
        assert isinstance(herb, Herbivore), isinstance(carn, Carnivore)

    def test_aging(self):
        """
        Test that the animal age increases
        """
        herb = Herbivore(weight=10, age=0)
        carn = Carnivore(weight=10)
        herb.aging()
        carn.aging()
        assert herb.age > 0, carn.age > 0

    def test_lose_weight(self):
        """
        Test that animals lose weight
        """
        herb, carn = Herbivore(weight=20), Carnivore(weight=20)
        herb.lose_weight(), carn.lose_weight()

        assert herb.weight == (20 - (20 * herb.p['eta']))
        assert carn.weight == (20 - (20 * carn.p['eta']))

    def test_parameters(self):
        """
        Test parameters of herbs and carns
        """
        herb, carn = Herbivore(), Carnivore()
        assert herb.p != carn.p


class TestHerbivore:
    """
    Tests for herbivore class
    """
    def test_eat_fodder(self):
        """
        Weight of animal shall increase after eating fodder

        """
        herb = Herbivore(weight=10, age=0)
        herb_weight = herb.weight
        herb.eat_fodder(cell=Lowland())
        # new weight
        herb_weight_after = herb.weight
        assert herb_weight < herb_weight_after

    def test_give_birth(self):
        """
        Test that the give birth function works
        """
        pass


class TestCarnivore:
    """
    Test for carnivore class
    """
    def test_kill_prey(self):
        carn = Carnivore(age=5, weight=90)
        killed_herbivores = carn.kill_prey([Herbivore(age=10, weight=10), Herbivore(age=5, weight=80)])
        assert carn.weight > 40


