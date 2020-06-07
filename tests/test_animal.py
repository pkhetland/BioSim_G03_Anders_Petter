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
        # Decreasing parameters
        herb.p['eta'] = 0.1
        carn.p['eta'] = 0.2
        herb_initial_weight, carn_initial_weight = herb.weight, carn.weight
        herb.lose_weight(), carn.lose_weight()
        # New weight of animal must be less than before
        assert herb.weight < herb_initial_weight
        assert carn.weight < carn_initial_weight

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


