# -*- coding: utf-8 -*-

"""
Tests for animal class.
"""
from biosim.animal import Herbivore, Carnivore
from biosim.landscape import Lowland
import math
import scipy.stats as stats
import pytest
import random


@pytest.fixture()
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


def formula_z_test(N, p, n):
    """
    Formula for the z-test used in tests
    """
    mean = N * p
    var = N * p * (1 - p)
    Z = (n - mean) / math.sqrt(var)
    phi = 2 * stats.norm.cdf(-abs(Z))
    return phi


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

    def test_set_invalid_params(self, reset_herbivore_params):
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
        Replace random number by a fixed value 0.
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
        Test that the animal always must die given a weight of 0.
        See examples/biolab/test_bacteria.py

        """
        herbivore.weight = 0
        assert herbivore.death()

    @pytest.mark.parametrize("omega_dict", [{"omega": 0.6}, {"omega": 0.4}])
    def test_death_z_test(self, reset_herbivore_params, omega_dict):

        """
        Based on H.E. Plesser: biolab/test_bacteria.py

        Probabilistic test of death function. Testing on herbivores.

        Given that the sample size is large. Under the Z-test the distribution under the null
        hypothesis can be estimated approximately by the normal distribution.
        See https://en.wikipedia.org/wiki/Z-test.

        Assuming low fitness of animals such that omega can be interpreted as an approximation of
        the death probability.
        We compute the number of dead animals returned by our death function from class Animal.
        Then we compare this value to the mean of dead animals derived from a fixed probability.


        Null hypothesis: The number of dead animals returned by the death function is
        statistically significant with a p-value greater than the alpha parameter.
        Alternative hypothesis: The number of dead animals returned is not statistically
        significant and we reject the null hypothesis.
        """
        random.seed(123)
        # High age gives low fitness
        herb = Herbivore(age=100, weight=10)
        # with low fitness we assume that the death probability is the same as omega
        # set parameters
        print(omega_dict)
        herb.set_params(omega_dict)
        fitness_herbs = [herb.fitness for _ in range(100)]
        print("fitness of herbs", fitness_herbs)
        # death probability set equal to omega
        p = Herbivore.p["omega"]
        # Number of animals
        N = 1000
        # Number of dead animals
        n = sum(herb.death() for _ in range(N))
        print("n is", n)
        # print([b.death() for _ in range(10)])
        print("formula phi is", formula_z_test(N, p, n))
        mean = N * p
        print("mean is", mean)
        var = N * p * (1-p)
        print("var is", var)
        Z = (n-mean) / math.sqrt(var)
        phi = 2 * stats.norm.cdf(-abs(Z))
        assert phi > TestAnimal.alpha
        print("phi", phi)

    @pytest.mark.parametrize("birth_dict", [{"w_birth": 8.0, "sigma_birth": 1.5},
                                            {"w_birth": 5.0, "sigma_birth": 7.5}])
    def test_mean_birth_weight(self, birth_dict, reset_herbivore_params):
        """
        Same type as above. But with exact value of variance

        Test that the birth weight of animals have a mean
        as specified in the animals parameter dictionary.

        Null hypothesis: The birth weight of the animal is returned correctly.
        Alternative hypothesis: The mean of the birth weight is not significant. The birth weight
        of the animal is not returned correctly. The observed mean birth weight has a p-value
        less than the significance level. We reject are null hypothesis if the difference between
        our computed mean and the sample mean is large.
        """
        random.seed(123)
        N = 1000
        Herbivore.set_params(birth_dict)
        n = sum(Herbivore(age=5, weight=50).birth_weight for _ in range(N))
        print("n is", n)
        # Theoretical mean
        p = Herbivore.p["w_birth"]
        mean = N * p
        print("mean is", mean)
        # Since the standard deviation is known, we can write the variance as
        var = (Herbivore.p["sigma_birth"]**2) * N
        print(var)
        Z = (n - mean) / math.sqrt(var)
        phi = 2 * stats.norm.cdf(-abs(Z))
        assert phi > TestAnimal.alpha
        print("phi", phi)

    def test_certain_birth(self, mocker, reset_herbivore_params):
        """
        test give birth function
        Mock the random number generator to always return one.
        Then as long as weight is not zero. give_birth function shall return True.

        """
        herb = Herbivore(weight=80, age=5)
        num_herbs = 10
        mocker.patch("random.random", return_value=0)
        give_birth, _ = herb.give_birth(num_herbs)
        assert give_birth is True

    @pytest.mark.parametrize("gamma_dict", [{"gamma": 0.2},
                                            {"gamma": 0.4},
                                            {"gamma": 0.6},
                                            {"gamma": 0.8}])
    def test_give_birth(self, gamma_dict, reset_herbivore_params):
        """Test that for animals with fitness close to one, and two same animals of one specie in
          a cell. The birth function should be well approximated by the parameter gamma."""

        random.seed(123)
        N = 1000
        Herbivore.set_params(gamma_dict)
        num_herbs = 2
        p = gamma_dict["gamma"]
        list_birth = [Herbivore(weight=200, age=5).give_birth(num_herbs) for _ in range(N)]
        # number when births return True
        n = sum([item[0] for item in list_birth])
        print("n is", n)
        mean = N * p
        print(mean)
        var = N * p * (1 - p)
        Z = (n - mean) / math.sqrt(var)
        phi = 2 * stats.norm.cdf(-abs(Z))
        print(phi)
        assert phi > TestAnimal.alpha



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
        greater numbers during a year cycle. Each mother can at most give birth to one animal.
        A high fitness and gamma parameter ensures highly fertile animals.
        """
        num_newborns = 0
        adult_herbs = [Herbivore(age=5, weight=40) for _ in range(100)]
        num_adults = len(adult_herbs)
        for herb in adult_herbs:
            herb.set_params(({"gamma": 0.99}))
            if herb.give_birth(num_adults):
                num_newborns += 1
        assert num_newborns <= num_adults


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
        """
        Test kill prey. With a high fitness diff the carnivore will always kill the herbivore.
        """
        carn = Carnivore(age=5, weight=30)
        herb_list = [Herbivore(age=100, weight=50) for _ in range(100)]
        kill_count = 0
        for _ in herb_list:
            if carn.kill_prey(herb_list):
                kill_count += 1
        assert kill_count == 100

    @pytest.mark.parametrize("params", [{"beta": 0.75, "DeltaPhiMax": 0.1}])
    def test_weight_gain(self, reset_carnivore_params, reset_herbivore_params, params):
        """
        Testing weight gain of carnivores. Assuming they have access to more fodder than they
        will eat. Making old heavy herbivores with low fitness. Carnivores should add beta * F
        weight
        Assuming fitness diff is larger than DeltaPhiMax such that the carnivore always kills
        the herbivore.
        """
        carn = Carnivore(age=5, weight=40)
        # number of herbivores
        N = 1000
        herb_list = [Herbivore(age=100, weight=200) for _ in range(N)]
        initial_weight = carn.weight
        # print(initial_weight)
        _ = carn.kill_prey(herb_list)
        # kill_count = len(herbs_killed)

        new_weight = carn.weight
        # n = kill_count
        print(new_weight)
        print(carn.p["beta"]*carn.p["F"])
        assert new_weight == initial_weight + carn.p["beta"] * carn.p["F"]
        # Assertion fails, weight is aded for all herbivores.

