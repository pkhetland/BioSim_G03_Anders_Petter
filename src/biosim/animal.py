# -*- coding: utf-8 -*-

__author__ = "Anders Mølmen Høst & Petter Kolstad Hetland"
__email__ = "anders.molmen.host@nmbu.no, petter.storesund.hetland@nmbu.no"

import numpy as np


class Animal:

    """
    Super class for Herbivores and Carnivores
    """

    # p = {}    # Empty dictionary to fill in parameters Herbivore or Carnivore

    def __init__(self, weight, age, p):
        if weight is None:
            self.weight = self.birth_weight()
        else:
            self.weight = weight
        self.age = age
        self.p = p

    def birth_weight(self):
        """
        birth weight of animal is drawn randomly
        Param: w_birth: birth weight of animal
        Param: sigma_birth: standard deviation
        Param: N: Population size
        return: array: weight_dist, Standard normal distribution of birth weights
        Seed: default_rng(int)

        """
        self.weight = np.random.normal(self.p["w_birth"], self.p["sigma_birth"])
        return self.weight

    def aging(self):
        """
        Increment age by one every season
        """
        self.age += 1

    def give_birth(self, cell, n_same):
        """
        Animals give birth based on fitness and same-type animals in cell
        """
        birth_prob = self.p["gamma"] * self.fitness * n_same - 1
        if self.weight < self.p["zeta"] * (self.p["w_birth"] + self.p["sigma_birth"]):
            return False, None  # Return false if weight of mother is less than birth
        elif birth_prob > 1:
            give_birth = True
        elif 0 < birth_prob < 1:
            give_birth = np.random.choice([False, True], p=[1 - birth_prob, birth_prob])
        else:
            give_birth = False

        if give_birth:  # If give_birth is true
            birth_weight = 2  # 2 is to be replace with the birth_weight function
            if birth_weight < self.weight:
                self.weight -= self.p["xi"] * birth_weight
                return True, birth_weight
            else:
                return False, None
        else:
            return False, None

    def death(self):
        """
        Return true when called if the animal is to be removed from the simulation
        and false otherwise.
        """
        if self.weight <= 0:
            return True
        else:
            death_prob = self.p["omega"] * (1 - self.fitness)
            return np.random.choice([False, True], p=[1 - death_prob, death_prob])

    @staticmethod
    def q(sgn, x, xhalf, phi):
        return 1.0 / (1.0 + np.exp(sgn * phi * (x - xhalf)))

    @property
    def fitness(self):
        """
        Function returning the fitness of an animal.
        Return: int: 0 < 1
        """
        return self.q(+1, self.age, self.p["a_half"], self.p["phi_age"]) * self.q(
            -1, self.weight, self.p["w_half"], self.p["phi_weight"]
        )


class Herbivore(Animal):
    def __init__(self, weight, age, p=None):
        if p is None:  # If no parameters are specified
            self.p = {  # Insert default values for species
                "w_birth": 8.0,
                "sigma_birth": 1.5,
                "beta": 0.9,
                "eta": 0.05,
                "a_half": 40,
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
        else:
            self.p = p

        super().__init__(weight, age, self.p)

    def eat_fodder(self, cell):
        """
        When an animal eats, its weight increases
        """
        consumption_amount = self.p["beta"] * self.p["F"]  # Calculate amount of fodder consumed
        if consumption_amount < cell.fodder:
            self.weight += consumption_amount  # Eat fodder
            cell.fodder -= consumption_amount  # Removes consumed fodder from cell object

        elif consumption_amount > cell.fodder > 0:
            self.weight += cell.fodder  # Eat fodder
            cell.fodder -= cell.fodder  # Sets fodder to zero.

        else:
            pass


if __name__ == "__main__":
    herb1 = Herbivore(10, 0)
    herb2 = Herbivore(weight=None, age=0)
    print(herb1.weight)
    print(herb1.birth_weight())
    # Output: Herb1 has both weight and birth_weight. BUG
