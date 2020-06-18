# -*- coding: utf-8 -*-

"""
Tests for animal class.
"""
from biosim_src.animal import Herbivore, Carnivore
from biosim_src.landscape import Lowland
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


def phi_z_test(N, p, n):
    """
    Formula for the z-test used in statistical tests
    Based on H.E. Plesser: biolab/test_bacteria.py
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
        the death probability. Testing with different values of omega
        We compute the number of dead animals returned by our death function from class Animal.
        Then we compare this value to the mean of dead animals derived from a fixed probability.


        Null hypothesis: The number of dead animals returned by the death function is
        statistically significant with a p-value greater than the alpha parameter.
        Alternative hypothesis: The number of dead animals returned is not statistically
        significant and we reject the null hypothesis.
        """
        random.seed(123)
        # High age ensures low fitness
        herb = Herbivore(age=100, weight=10)
        # with low fitness we assume that the death probability is the same as omega
        herb.set_params(omega_dict)
        # death probability set equal to omega
        p = Herbivore.p["omega"]
        # Number of animals
        N = 1000
        # Number of dead animals
        n = sum(herb.death() for _ in range(N))
        # Performing the z-test
        assert phi_z_test(N, p, n) > TestAnimal.alpha

    @pytest.mark.parametrize("birth_dict", [{"w_birth": 8.0, "sigma_birth": 1.5},
                                            {"w_birth": 6.0, "sigma_birth": 1.0},
                                            {"w_birth": 7.0, "sigma_birth": 1.5}])
    def test_mean_birth_weight(self, birth_dict, reset_herbivore_params):
        """ Test that the birth weight of animals are normal distributed using the normaltest
        from scipy.
        https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.normaltest.html

        Null hypothesis: The birth weight of the animal is normally distributed
        Alternative hypothesis: The birth weight are not normally distributed.

        We keep the null hypothesis if the p-value is larger than the significance level alpha
        """
        random.seed(123)
        N = 1000
        Herbivore.set_params(birth_dict)
        herb_birth_weights = [Herbivore(age=5, weight=20).birth_weight for _ in range(N)]
        k2, phi = stats.normaltest(herb_birth_weights)
        assert phi > TestAnimal.alpha

    def test_certain_birth(self, mocker, reset_herbivore_params):
        """
        test give birth function
        Mock the random number generator to always return one.
        Then as long as weight is not zero. give_birth function shall return True.

        """
        herb = Herbivore(weight=800, age=5)
        num_herbs = 10
        mocker.patch("random.random", return_value=0)
        give_birth, _ = herb.give_birth(num_herbs)
        assert give_birth is True

    @pytest.mark.parametrize("gamma_dict", [{"gamma": 0.2},
                                            {"gamma": 0.4},
                                            {"gamma": 0.6},
                                            {"gamma": 0.8}])
    def test_give_birth(self, gamma_dict, reset_herbivore_params):
        """Test that for animals with fitness close to one, and two animals of same type one specie
        in a cell. The give_birth function should be well approximated by the parameter gamma.
        An we test this against our function under the significance level alpha.

        Null hypothesis: The give_birth function returns correct with fixed gamma
        Alternative hypothesis: The give_birth function does not return correct. We reject our
        null hypothesis.
        """

        random.seed(123)
        N = 1000
        Herbivore.set_params(gamma_dict)
        num_herbs = 2
        p = gamma_dict["gamma"]
        list_birth = [Herbivore(weight=200, age=5).give_birth(num_herbs) for _ in range(N)]
        # number when births return True
        n = sum([item[0] for item in list_birth])
        mean = N * p
        assert phi_z_test(N, p, n) > TestAnimal.alpha

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
    Tests for carnivore class
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
        mock_sorted_list = [(herb, herb.fitness) for herb in herb_list]
        kill_count = 0
        for _ in mock_sorted_list:
            if carn.kill_prey(mock_sorted_list):
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
        mock_sorted_list = [(herb, herb.fitness) for herb in herb_list]
        initial_weight = carn.weight
        _ = carn.kill_prey(mock_sorted_list)
        new_weight = carn.weight
        assert new_weight == initial_weight + carn.p["beta"] * carn.p["F"]

