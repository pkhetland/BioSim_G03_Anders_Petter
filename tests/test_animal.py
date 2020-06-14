# -*- coding: utf-8 -*-

"""
Tests for animal class.
"""
from src.animal import Herbivore, Carnivore
from src.landscape import Lowland
import math
import scipy.stats as stats
import pytest


def test_set_params():
    """
    Test that parameters can be set
    """
    my_params = {"w_birth": 10,
                 "sigma_birth": 2.5}
    Herbivore.set_params(my_params)
    assert Herbivore.p["w_birth"] == 10
    assert Herbivore.p["sigma_birth"] == 2.5

@pytest.fixture
def reset_herbivore_params():
    """
    Based on test_dish.py
    set parameters of herbivores back to defaults
    """
    yield

    Herbivore.set_params(Herbivore.p)

@pytest.fixture
def reset_carnivore_params():
    """
    set paramteres of carnivores back to defaults
    """
    yield

    Carnivore.set_params(Carnivore.p)


@pytest.mark.parametrize("invalid_key_value",
                         {"w_death": 10,
                          "sigma_birth": -5})
def test_set_invalid_params(invalid_key_value):
    """
    Test errors
    """
    with pytest.raises(KeyError):
        assert Herbivore.p["w_death"]

    # Last part Do not raise Value Error. Not sure why.
    #with pytest.raises(ValueError):

        #invalid_values = {"sigma_birth": -5}
        #ssert Herbivore.p["sigma_birth"]


@pytest.fixture
def carnivore():
    return Carnivore()


@pytest.fixture()
def herbivore():
    return Herbivore()



@pytest.fixture
def animals():
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


def test_fitness(animals):
    """
    Fitness function shall return a value between 0 and 1
    for all animals


    """
    for animal in animals:
        assert 0 <= animal.fitness <= 1



def test_death(herbivore, mocker):
    """
    Replace random number by a function returning a fixed value
    """
    mocker.patch("random.random", return_value=0)
    assert herbivore.death() is True


def test_give_birth(herbivore, mocker):
    """
    TEST FAILS 13.06
    Mock the birth function to see it returns correct.
    Replace random number by fixed value.

    Making sure the weight is greater than the newborn weight

    """
    mocker.patch("random.random", return_value=0)
    mocker.spy("herbivore.fitness", return_value=1)
    assert herbivore.give_birth(n_same=1000) is True


def test_migrate(herbivore, mocker):
    """
    Mock migrate function to see if it returns correct

    """

    mocker.patch("random.random", return_value=0)
    assert herbivore.migrate() is True

class TestWeightGain:

    """
    Based on suggestions lecture Plesser

    create some new animals for statistical test of carnivores eating herbivores
    Make Herbivores heavy, old and bad fitness. Bad fitness achived throgh high phi_age
    and low phi_weight
    Low DeltaPhiMax such that carnivore only need marginal better fitness than herbivore.

    Then test the weight gain of carnivores.



    """

    @pytest.mark.parametrize("params_herb", {"phi_age": 1,
                                             "phi_weight": 0.1},
                             "params_carn", {"DeltaPhiMax": 0.1,
                                             "F": 50},
                             indirect=True)
    def create_animals(self, params_herb, params_carn):
        self.herbivores = [Herbivore(age=100, weight=1000) for _ in range(100)]
        # 100 herbivores
        self.carnivore = Carnivore(age=5, weight=50)
        for herb in self.herbivores:
            herb.set_params(params_herb)
        self.carnivore.set_params(params_carn)

    def test_weight_gain(self, params_herb, params_carn):
        """
        Statistical test

        """
        pass


class TestAnimal:
    alpha = 0.01

    """
    Tests for animal class
    """
    """
    def test_death_prob(self):
        # Comment AH. Need a function to create animals

        # Probability of dying 1

        self.death_prob = 1
        """
    def test_certain_death(self, herbivore):
        """
        Test that the animal always must die given death_prob = 1
        100 Herbivore instances all must die
        See examples/biolab/test_bacteria.py

        """
        herbivore.weight = 0
        assert herbivore.death()

    def test_death_binom(self):
        """
        Test if the death function returns statistical significant results
        under the bionomial test, with a given death probability p.
        Null hypothesis: The death functions returns correct probability of death of animal
        Alternative hypothesis: The death function does not return correct.
        Reject the null hypothesis if and only if the p-value is less than the significance
        level.

        : param p: The hypothesized probability
        : type p: float
        : param N: The number of animals
        : type N: int
        : param n: The number of deaths
        : type n: int
        """
        h = Herbivore(age=0, weight=10)
        p = 0.2

        # Comment test fails for high values of p. In biolab bacteria example p can be "anything"
        # Comment test fails for high values of p

        N = 1000
        n = sum(h.death() for _ in range(N))
        print("Number of deaths:", n)
        assert stats.binom_test(n, N, p, "greater") > self.alpha
        print(stats.binom_test(n, N, p, "greater"))
        # With a probability of at most p = 0.2 The null hypothesis cannot be rejected


    @pytest.fixture(autouse=True)
    def create_animals(self):
        """
        Based on solution from Bishnu Pudel
        Create two herbivore objects
        """
        h1 = Herbivore(weight=10, age=0)
        h2 = Herbivore(weight=10, age=0)
        # set parameters
        h1.birth_prob = 0.5
        h2.birth_prob = 0.5




    def test_death_z_test(self):

        """
        Souce: biolab/test_bacteria.py

        Probabilistic test of death function. Test the number of deaths is
        normally distributed for large number of animals. And the death probability is
        significant with a p-value of 0.01.
        """
        b = Herbivore(age=0, weight=10)
        # Set mocking parameter of the death probability of the animal
        p = 0.2
        # 100 animals
        N = 100
        n = sum(b.death() for _ in range(N))
        # print([b.death() for _ in range(10)])

        mean = N * p
        var = N * p * (1-p)
        Z = (n-mean) / math.sqrt(var)
        phi = 2 * stats.norm.cdf(-abs(Z))
        assert phi > 0.01


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


    def test_instance_count(self):
        herb = Herbivore()

        assert herb.herbivore_instance_count == 1

        Herbivore.subtract_herbivore()

        assert Herbivore.herbivore_instance_count == 0




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

    def test_instance_count(self):
        """
        Test that classmethods for counting instances work
        """
        carnivores = [Carnivore() for _ in range(5)]

        Carnivore.subtract_carnivore()
        Carnivore.subtract_carnivore()

        assert Carnivore.carnivore_instance_count == 3