# -*- coding: utf-8 -*-

"""
Tests for animal class.
"""
from src.animal import Herbivore, Carnivore
from src.landscape import Lowland
import math
import scipy.stats as stats
import pytest
import random


@pytest.fixture
def reset_herbivore_params():
    """
    Based on test_dish.py
    set parameters of herbivores back to defaults
    """
    yield Herbivore.set_params(Herbivore.p)


@pytest.fixture
def reset_carnivore_params():
    """
    Set parameters of carnivores back to defaults
    """
    yield Carnivore.set_params(Carnivore.p)

def test_give_birth():
    """
    Mock the birth function to see it returns correct.
    Replace random number by fixed value.

    Making sure the weight is greater than the newborn weight

    """
    pass


class TestAnimal:
    alpha = 0.01    # Significance level

    """
    Tests for animal class
    
    """
    def test_set_params(self):
        """
        Test that parameters can be set
        """
        my_params = {"w_birth": 10,
                     "sigma_birth": 2.5}
        Herbivore.set_params(my_params)
        assert Herbivore.p["w_birth"] == 10
        assert Herbivore.p["sigma_birth"] == 2.5

    def test_set_invalid_params(self):
        """
        Test errors with illegal keys and values
        """
        with pytest.raises(KeyError):
            assert Herbivore.p["w_death"]
        with pytest.raises(ValueError):
            assert Herbivore.set_params({"sigma_birth": -5})

    @pytest.fixture    # carnivore instance
    def carnivore(self):
        return Carnivore()

    @pytest.fixture    # herbivore instance
    def herbivore(self):
        return Herbivore()

    @pytest.fixture
    def animals(self):
        """
        create animals of different type, age and weight to use in test of fitness
        """

        animals = [Herbivore(age=0, weight=5),
                   Herbivore(age=0, weight=1000),
                   Herbivore(age=100, weight=5),
                   Herbivore(age=100, weight=1000),
                   Herbivore(age=0, weight=5),
                   Carnivore(age=0, weight=5),
                   Carnivore(age=0, weight=1000),
                   Carnivore(age=100, weight=5),
                   Carnivore(age=100, weight=1000)]
        return animals

    def test_fitness(self, animals):
        """
        Fitness function shall return a value between 0 and 1
        for all animals


        """
        for animal in animals:
            assert 0 <= animal.fitness <= 1

    def test_death_mocker(self, herbivore, mocker):
        """
        Replace random number by a function returning a fixed value.
        Animal will then always die.
        """
        mocker.patch("random.random", return_value=0)
        assert herbivore.death() is True

    def test_migrate(self, herbivore, mocker):
        """
        Mock migrate function to see if it returns correct
        Test passes if animal migrates

        """
        mocker.patch("random.random", return_value=0)
        assert herbivore.migrate() is True

    def test_certain_death_weight(self, herbivore):
        """
        Test that the animal always must die given death_prob = 1
        100 Herbivore instances all must die
        See examples/biolab/test_bacteria.py

        """
        herbivore.weight = 0
        assert herbivore.death()

    def test_death_z_test(self, reset_herbivore_params):

        """
        Souce: biolab/test_bacteria.py

        Probabilistic test of death function. Testing on herbivores.
        Assuming low fitness of animal so that omega decides the magnitude of the death probability.
        We compute the number of dead animals returned by our death function from class Animal.
        Then we compare this value to the mean of dead animals derived from a fixed probability.
        This probability is obtained by setting the omega parameter.


        Null hypothesis: The number of dead animals returned by the death function has a
        statistically significant p-value.
        Alternative hypothesis: The number of dead animals returned is not statistically
        significant and we reject the null hypothesis.
        """
        # Task: Import seed from BioSim
        random.seed(123)
        # High age gives low fitness
        herb = Herbivore(age=100, weight=10)
        # with low fitness we assume that the death probability is the same as omega
        # set parameters
        my_parameters = {"phi_age": 0.6, "phi_weight": 0.1, "omega": 0.4}
        herb.set_params(my_parameters)
        fitness_herbs = [herb.fitness for _ in range(100)]
        print("fitness of herbs", fitness_herbs)
        # death probability set equal to omega
        p = my_parameters["omega"]
        # Number of animals
        N = 1000
        # Number of dead animals
        n = sum(herb.death() for _ in range(N))
        print("n is", n)
        # print([b.death() for _ in range(10)])

        mean = N * p
        print("mean is", mean)
        var = N * p * (1-p)
        Z = (n-mean) / math.sqrt(var)
        phi = 2 * stats.norm.cdf(-abs(Z))
        assert phi > TestAnimal.alpha
        print("phi", phi)

    def test_constructor(self):
        """
        Animals can be created
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

    def test_lose_weight(self, reset_herbivore_params, reset_carnivore_params):
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

    def test_parameters(self, reset_herbivore_params, reset_carnivore_params):
        """
        Test parameters of herbs and carns
        """
        herb, carn = Herbivore(), Carnivore()
        assert herb.p != carn.p

    def test_single_procreation(self):
        """
        test that the initial herbivore population will not reproduce a newborn population of
        greater numbers. Each mother can at most give birth to one animal. A high fitness
        and gamma parameter ensures highly fertile animals.
        """
        newborn_herbs = 0
        adult_herbs = [Herbivore(age=5, weight=40) for _ in range(100)]
        num_adult_herbs = len(adult_herbs)
        for herb in adult_herbs:
            herb.set_params(({"gamma": 0.99}))
            if herb.give_birth(num_adult_herbs):
                newborn_herbs += 1
        assert newborn_herbs <= num_adult_herbs


class TestHerbivore:
    """
    Tests for herbivore class
    """

    def test_constructor(self):
        """
        Test herbivores can be constructed
        """
        herb = Herbivore()
        assert isinstance(herb, Herbivore)

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


class TestCarnivore:
    """
    Test for carnivore class
    """

    def test_constructor(self):

        """
        Test carnivores can be constructed
        """
        carn = Carnivore()
        assert isinstance(carn, Carnivore)

    def test_kill_prey(self):
        carn = Carnivore(age=5, weight=900)
        killed_herbivores = carn.kill_prey([Herbivore(age=10, weight=1),
                                            Herbivore(age=5, weight=80)])
        assert len(killed_herbivores) > 0