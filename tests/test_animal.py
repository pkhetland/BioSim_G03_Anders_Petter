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
    def create_animals(self):
        # Comment AH. Need a function to create
        self.n_herbivores = 50
        self.n_carnivores = 50
        self.animals = Animal(self.n_herbivores, self.n_carnivores)

    def test_death(self):
        """
        Test that the probability of death is greater than zero
        """
        pass

    def test_constructor(self):
        """Herbivore can be created"""
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
