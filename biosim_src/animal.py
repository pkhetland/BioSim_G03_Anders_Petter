# -*- coding: utf-8 -*-

__author__ = "Anders Mølmen Høst & Petter Kolstad Hetland"
__email__ = "anders.molmen.host@nmbu.no, petter.storesund.hetland@nmbu.no"

import random as random
from math import e


class Animal:
    """Super class for Herbivores and Carnivores.

    **Subclasses**:
        - Herbivore class
        - Carnivore class

    :param weight: Weight of animal
    :type weight: float
    :param age: Age of animal
    :type age: int
    """

    def __init__(self, weight, age):
        if weight is None:
            self._weight = self.birth_weight
        else:
            self._weight = float(weight)
        self._age = age

        self._species = self.__class__.__name__
        self._death_prob = None
        self.has_moved = False

        self._fitness = None
        self._fitness_valid = False

    @classmethod
    def set_params(cls, new_params):
        """Set parameters for animal classes.

        :param new_params: New parameters to be set to the class params
        :type new_params: dict

        .. see also::
            - `biosim.set_animal_parameters`

        """
        for key in new_params:
            if key not in cls.p:
                raise KeyError("Invalid key name: " + key)

        for key in cls.p:
            if key in new_params:
                if new_params[key] < 0:
                    raise ValueError("Parameter must be positive")
                cls.p.update(new_params)

    @classmethod
    def get_params(cls):
        """Getter function for the class parameters.

        :return: Dictionary with current parameters for class
        :rtype: dict
        """
        return cls.p

    def __repr__(self):
        """Format for string representation.
        """
        return "{}({} years, {:.3} kg)".format(self._species, self._age, self._weight)

    def __str__(self):
        """Format for better readability.
        """
        return "{}({} years, {:.3} kg)".format(self._species, self._age, self._weight)

    @classmethod
    def from_dict(cls, animal_dict):
        """Allows the sim to add instances directly from dictionaries when adding populations.

        :param animal_dict: Dictionary that specifies class weight and age
        :type animal_dict: dict

        :Example:
            .. code-block:: python

                example_dict = {'species': 'Herbivore', 'age': 5, 'weight': 20}
                herb = Herbivore.from_dict(example_dict)

        .. seealso::
            - `BioSim.add_population`

        """
        class_weight = animal_dict["weight"]
        class_age = animal_dict["age"]
        return cls(age=class_age, weight=class_weight)

    @property
    def weight(self):
        """Getter method for Animal._weight

        :return: Weight of animal
        :r_type: float
        """
        return self._weight

    @weight.setter
    def weight(self, weight):
        """Setter method for Animal._weight"""
        self._weight = weight

    @property
    def age(self):
        """Getter method for Animal._age.

        :return: Age of animal
        :r_type: int
        """
        return self._age

    @age.setter
    def age(self, age):
        """Setter method for Animal._age."""
        self._age = age

    @property
    def species(self):
        """Getter method for Animal._species

        :return: Species of animal
        :r_type: str
        """
        return self._species

    def aging(self):
        """Increments age by one every season.

        .. seealso::
            - `BioSim.run_year_cycle`
        """
        self.age += 1

    def give_birth(self, n_same):
        """Animals give birth based on fitness and same-type animals in cell.

        :param n_same: number of same-type animals
        :type n_same: int

            ...

        :return: True or False
        :rtype: bool

        .. note::

            - Animals give birth with a probability depending on fitness and n-same species in cell.
            - If the animal is to give birth, it will only happen if birth_weight is less
                than weight of parent.

        .. seealso::

            - `BioSim.procreation`

        """
        birth_prob = self.p["gamma"] * self.fitness * (n_same - 1)
        if self.weight < self.p["zeta"] * (self.p["w_birth"] + self.p["sigma_birth"]):
            return False, None  # Return false if weight of mother is less than birth
        elif birth_prob >= 1:
            give_birth = True
        elif 0 < birth_prob < 1:
            give_birth = True if random.random() < birth_prob else False
        else:
            give_birth = False

        if give_birth:  # If give_birth is true
            birth_weight = self.birth_weight
            if birth_weight < self.weight:
                self.weight -= self.p["xi"] * birth_weight
                self._fitness_valid = False  # Signal that saved fitness is incorrect
                return True, birth_weight
            else:
                return False, None
        else:
            return False, None

    def migrate(self):
        """Method deciding whether animal will migrate or not.

        :return: Boolean value where True is migrate
        :rtype: bool

        .. seealso::
            - BioSim.migrate
            - BioSim.run_year_cycle

        """
        move_prob = self.p["mu"] * self.fitness
        if random.random() < move_prob:
            return True
        else:
            return False

    def lose_weight(self):
        """Animals lose weight each year based on parameter `eta`."""
        self.weight -= self.weight * self.p["eta"]
        self._fitness_valid = False  # Signal that saved fitness is incorrect

    def death(self):
        """Return true when called if the animal is to be removed from the simulation
        and false otherwise.

        :return: Bool indicating death or no death
        :rtype: bool

        .. seealso::
            - `BioSim.run_year_cycle`

        """
        if self.weight <= 0:
            death = True
        else:
            self._death_prob = self.p["omega"] * (1 - self.fitness)
            death = True if random.random() < self._death_prob else False

        return death

    @staticmethod
    def q(sgn, x, x_half, phi):
        """Mathematical function for calculating fitness.

        :param sgn: Sign, positive/negative
        :param x, x_half, phi: Instance variables

        .. math::

            q^{+-}(x, x_{half}, \phi) = \dfrac{1}{1 + e^{+-\phi(x - x_{half})}}

        """
        return 1.0 / (1.0 + e ** (sgn * phi * (x - x_half)))

    @property
    def fitness(self):
        """Function returning the fitness of an animal.

        :return: A value between 0 and 1, where 1 is perfect fitness and 0 is death
        :rtype: float

        .. math::

            \phi_{animal} = q^{+} (a, a_{half}, \phi_{age}) * q^{-} (w, w_{half}, \phi_{weight})

        .. note::
            If animal weight is <= 0, fitness is set to 0 regardless.

        """
        if self._fitness is None or not self._fitness_valid:
            self._fitness = self.q(+1, self.age, self.p["a_half"], self.p["phi_age"]) * self.q(
                -1, self.weight, self.p["w_half"], self.p["phi_weight"]
            )
            self._fitness_valid = True

        return self._fitness

    @property
    def birth_weight(self):
        """Birth weight of a newborn animal is drawn randomly from a gaussian curve.

        :return birth_weight: drawn from gaussian distribution
        :rtype: float

        .. seealso::
            - BioSim.procreation
            - Animal.give_birth

        """
        birth_weight = random.gauss(self.p["w_birth"], self.p["sigma_birth"])
        return birth_weight


class Herbivore(Animal):
    """Herbivore class.

    *Properties*:
        - `p`: Parameters specific to Herbivore instances.

    :param weight: Weight used to initiate Animal super()
    :param age: Age used to initiate Animal super()
    """

    p = {  # Dictionary of parameters belonging to the Herbivore class
        "w_birth": 8.0,
        "sigma_birth": 1.5,
        "beta": 0.9,
        "eta": 0.05,
        "a_half": 40.0,
        "phi_age": 0.6,
        "w_half": 10.0,
        "phi_weight": 0.1,
        "mu": 0.25,
        "gamma": 0.2,
        "zeta": 3.5,
        "xi": 1.2,
        "omega": 0.4,
        "F": 10.0,
    }

    def __init__(self, weight=None, age=0):
        super().__init__(weight, age)

    def eat_fodder(self, cell):
        """When an animal eats, its weight increases.

        .. note::
            - Herbivore will try to eat enough ('F') fodder, and if that is not possible,
                it will eat what is left in the cell.
            - Weight of herbivore will increase by `F` times `beta`.

        .. seealso::
            - `Carnivore.kill_prey`
            - `BioSim.feeding`

        """
        consumption_amount = self.p["F"]  # Calculate amount of fodder consumed
        if consumption_amount <= cell.fodder:
            self.weight += self.p["beta"] * consumption_amount  # Eat fodder
            cell.fodder -= consumption_amount  # Removes consumed fodder from cell object

        elif consumption_amount > cell.fodder > 0:
            self.weight += self.p["beta"] * cell.fodder  # Eat fodder
            cell.fodder = 0  # Sets fodder to zero.

        self._fitness_valid = False  # Signal that saved fitness is incorrect


class Carnivore(Animal):
    """Carnivore class.

    *Properties*:
        - `p`: Parameters specific to Carnivore instances.

    :param weight: Weight used to initiate Animal super()
    :param age: Age used to initiate Animal super()
    """

    p = {  # Dictionary containing default parameter values for Carnivore class
        "w_birth": 6.0,
        "sigma_birth": 1.0,
        "beta": 0.75,
        "eta": 0.125,
        "a_half": 40.0,
        "phi_age": 0.3,
        "w_half": 4.0,
        "phi_weight": 0.4,
        "mu": 0.4,
        "gamma": 0.8,
        "zeta": 3.5,
        "xi": 1.1,
        "omega": 0.8,
        "F": 50.0,
        "DeltaPhiMax": 10.0,
    }

    def __init__(self, weight=None, age=0):
        super().__init__(weight, age)

    def kill_prey(self, sorted_herbivores):
        """Iterates through sorted herbivores and eats until F is met.

        :param sorted_herbivores: Herbivores sorted by fitness levels from low to high
        :type sorted_herbivores: list

        :return: Animals killed by herbivore to be removed from simulation
        :rtype: list

        .. seealso::
            - BioSim.feeding
            - Herbivore.eat_fodder
            - LandscapeCell.sorted_herbivores

        """
        consumption_weight = 0
        herbs_killed = []
        fitness = self.fitness

        for herb in sorted_herbivores:
            if consumption_weight < self.p["F"]:
                fitness_diff = fitness - herb[1]
                if fitness_diff <= 0:
                    kill_prey = False

                elif 0 < fitness_diff < self.p["DeltaPhiMax"]:
                    kill_prob = fitness_diff / self.p["DeltaPhiMax"]
                    kill_prey = True if random.random() <= kill_prob else False

                else:
                    kill_prey = True

                if kill_prey:  # If the herb is killed
                    self._fitness_valid = False  # Signal that saved fitness is incorrect
                    consumption_weight += herb[
                        0
                    ].weight  # Add herb weight to consumption_weight variable
                    herbs_killed.append(herb[0])
            else:
                continue

        if consumption_weight > self.p["F"]:  # Auto-adjust consumption_weight to be <= F-parameter
            consumption_weight = self.p["F"]

        self.weight += consumption_weight * self.p["beta"]  # Add weight to carnivore

        return herbs_killed
