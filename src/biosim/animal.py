# -*- coding: utf-8 -*-

__author__ = 'Anders Mølmen Høst & Petter Kolstad Hetland'
__email__ = 'anders.molmen.host@nmbu.no, petter.storesund.hetland@nmbu.no'

import numpy as np


class Animal:

    """
    Super class for Herbivores and Carnivores
    """
    p = {}    # Empty dictionary to fill in parameters Herbivore or Carnivore

    def __init__(self, weight, age):
        if weight is None:
            self.weight = self.birth_weight()
        else:
            self.weight = weight
        self.age = age

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

    def eat_fodder(self, beta=0.9, F=10):
        """
        When an animal eats, its weight increases

        """
        self.weight += beta * F

    def aging(self):
        """
        Increment age by one every season
        """
        self.age += 1

    @staticmethod
    def q(sgn, x, xhalf, phi):
        return 1. / (1. + np.exp(sgn * phi * (x - xhalf)))

    def fitness(self):
        """
        Function returning the fitness of an animal.
        Return: int: 0 < 1
        """
        return (self.q(+1, self.age, self.p['a_half'], self.p['phi_age'])
                * self.q(-1, self.weight, self.p['w_half'], self.p['phi_weight']))


class Herbivore(Animal):
    p = {'w_birth': 8.0,
         'sigma_birth': 1.5,
         'beta': 0.9,
         'eta': 0.05,
         'a_half': 40,
         'phi_age': 0.6,
         'w_half': 10.0,
         'phi_weight': 0.1,
         'mu': 0.25,
         'gamma': 0.2,
         'zeta': 3.5,
         'xi': 1.2,
         'omega': 0.4,
         'F': 10.0}

    def __init__(self, weight, age):
        super().__init__(weight, age)


if __name__ == "__main__":
    herb1 = Herbivore(10, 0)
    herb2 = Herbivore(weight=None, age=0)
    print(herb1.weight)
    print(herb1.birth_weight())
    # Output: Herb1 has both weight and birth_weight. BUG