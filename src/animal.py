# -*- coding: utf-8 -*-

__author__ = "Anders Mølmen Høst & Petter Kolstad Hetland"
__email__ = "anders.molmen.host@nmbu.no, petter.storesund.hetland@nmbu.no"

import numpy as np
import random as random
from math import e


class Animal:
    # Empty dictionaries to set parameters
    p = {}

    """
    Super class for Herbivores and Carnivores. TEST
    """
    instance_count = 0

    def __init__(self, weight, age):
        """
        :param weight: Weight of animal
        :type weight: float
        :param age: Age of animal
        :type age: int
        """
        if weight is None:
            self._weight = self.birth_weight
        else:
            self._weight = float(weight)
        self._age = age

        self._species = self.__class__.__name__
        self._death_prob = None

        random.seed(123)  # Set seed - Will be moved to interface

        Animal.instance_count += 1

    @classmethod
    def set_params(cls, new_params):
        """
        Set parameter for animal classes
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
        """
        Return dictionary with parameters
        """
        return cls.p

    def __repr__(self):
        return '{}({} years, {:.3} kg)'.format(self._species, self._age, self._weight)

    def __str__(self):
        return '{}({} years, {:.3} kg)'.format(self._species, self._age, self._weight)

    @classmethod
    def from_dict(cls, animal_dict):
        """Allows the sim to add instances directly from dictionaries when adding pop

        :param animal_dict: Dict with format {'species': 'Herbivore', 'age': 5, 'weight': 20}
        :type animal_dict: dict
        """
        class_weight = animal_dict['weight']
        class_age = animal_dict['age']
        return cls(age=class_age, weight=class_weight)

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, weight):
        self._weight = weight

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, age):
        self._age = age

    @property
    def species(self):
        return self._species

    def aging(self):
        """
        Increment age by one every season
        """
        self.age += 1

    def give_birth(self, n_same):
        """
        Animals give birth based on fitness and same-type animals in cell
        """
        birth_prob = self.p["gamma"] * self.fitness * n_same - 1
        if self.weight < self.p["zeta"] * (self.p["w_birth"] + self.p["sigma_birth"]):
            return False, None  # Return false if weight of mother is less than birth
        elif birth_prob >= 1:
            give_birth = True
        elif 0 < birth_prob < 1:
            give_birth = True if random.random() < birth_prob else False
            # give_birth = random.choice([True, False], weights=[birth_prob, 1 - birth_prob])
        else:
            give_birth = False

        if give_birth:  # If give_birth is true
            birth_weight = self.birth_weight
            if birth_weight < self.weight:
                self.weight -= self.p["xi"] * birth_weight
                return True, birth_weight
            else:
                return False, None
        else:
            return False, None

    def migrate(self):
        """
        Returns bool indicating whether animal will migrate
        """
        move_prob = self.p["mu"] * self.fitness
        return True if random.random() < move_prob else False
        # return np.random.choice([True, False], p=[move_prob, 1 - move_prob])

    def lose_weight(self):
        """
        Animals lose weight based on eta parameter
        """
        self.weight -= self.weight * self.p["eta"]

    def death(self):
        """
        Return true when called if the animal is to be removed from the simulation
        and false otherwise.
        """
        if self.weight <= 0:
            death = True
        else:
            if self._death_prob is None:
                self._death_prob = self.p["omega"] * (1 - self.fitness)

            death = True if random.random() < self._death_prob else False
            # death = np.random.choice(
            #     [True, False], weights=[self._death_prob, 1 - self._death_prob]
            # )
            self._death_prob = None

        if death:
            Animal.instance_count -= 1
            if self.species == 'Herbivore':
                Herbivore.instance_count -= 1
            elif self.species == 'Carnivore':
                Carnivore.instance_count -= 1

        return death

    @staticmethod
    def q(sgn, x, x_half, phi):
        return 1.0 / (1.0 + e**(sgn * phi * (x - x_half)))

    @property
    def fitness(self):
        """
        Function returning the fitness of an animal.
        Return: int: 0 < 1
        """
        return self.q(+1, self.age, self.p["a_half"], self.p["phi_age"]) * self.q(
            -1, self.weight, self.p["w_half"], self.p["phi_weight"]
        )

    @property
    def birth_weight(self):
        """
        birth weight of newborn animal is drawn randomly
        param: w_birth: birth weight of animal
        param: sigma_birth: standard deviation
        param: N: Population size
        return: array: weight_dist, Standard normal distribution of birth weights

        """
        birth_weight = np.random.normal(self.p["w_birth"], self.p["sigma_birth"])
        return birth_weight


class Herbivore(Animal):

    instance_count = 0
    p = {
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
                "F": 10.0}

    def __init__(self, weight=10, age=0):
        if self.p is None:  # If no parameters are specified
            super().p.update({  # Insert default values for species
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
            })
        else:
            super().get_params()

        super().__init__(weight, age)

        Herbivore.instance_count += 1

    def eat_fodder(self, cell):
        """
        When an animal eats, its weight increases
        """
        consumption_amount = (
            self.p["beta"] * self.p["F"]
        )  # Calculate amount of fodder consumed
        if consumption_amount <= cell.fodder:
            self.weight += consumption_amount  # Eat fodder
            cell.fodder -= (
                consumption_amount  # Removes consumed fodder from cell object
            )

        elif consumption_amount > cell.fodder > 0:
            self.weight += cell.fodder  # Eat fodder
            cell.fodder = 0  # Sets fodder to zero.


class Carnivore(Animal):
    """
    Carnivore class
    """

    instance_count = 0
    p = {"w_birth": 6.0,
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
         "DeltaPhiMax": 10.0}

    def __init__(self, weight=None, age=0):
        if self.p is None:  # If no parameters are specified
            super().p.update({  # Insert default values for species
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
            })
        else:
            self.p = super().get_params()

        super().__init__(weight, age)

        Carnivore.instance_count += 1

    def kill_prey(self, sorted_herbivores):
        """Iterates through sorted herbivores and eats until F is met

        :param sorted_herbivores: Herbivores sorted by fitness levels from low to high
        :type sorted_herbivores: list
        ...
        :return: Animals killed by herbivore to be removed from simulation
        :rtype: list
        """
        consumption_weight = 0
        herbs_killed = []
        fitness = self.fitness

        for herb in sorted_herbivores:
            if consumption_weight < self.p["F"]:
                fitness_diff = fitness - herb.fitness
                if fitness_diff <= 0:
                    kill_prey = False

                elif 0 < fitness_diff < self.p["DeltaPhiMax"]:
                    kill_prob = fitness_diff / self.p["DeltaPhiMax"]
                    kill_prey = True if random.random() <= kill_prob else False
                    # kill_prey = random.choice(
                    #     [True, False], weights=[kill_prob, 1 - kill_prob]
                    # )

                else:
                    kill_prey = True

                if kill_prey:  # If the herb is killed
                    consumption_weight += (
                        herb.weight
                    )  # Add herb weight to consumption_weight variable
                    herbs_killed.append(herb)

                    Animal.instance_count -= 1
                    Herbivore.instance_count -= 1

        if (
            consumption_weight > self.p["F"]
        ):  # Auto-adjust consumption_weight to be <= F-parameter
            consumption_weight = self.p["F"]

        self.weight += consumption_weight * self.p["beta"]  # Add weight to carnivore

        return herbs_killed


if __name__ == "__main__":
    Herbivore.set_params({"w_birth": 9.0})
    print(Herbivore.get_params())
    print(Herbivore.p)
    print(Carnivore.get_params())
    Carnivore.set_params({"w_birth": -5.0, "beta": 0.95})
    print(Carnivore.get_params())
    # new instance with default parameters

    # Output 10. OK
    # KeyError. Expected 8. Comments?

