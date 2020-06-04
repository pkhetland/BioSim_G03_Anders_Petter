# -*- coding: utf-8 -*-

__author__ = 'Anders Mølmen Høst & Petter Kolstad Hetland'
__email__ = 'anders.molmen.host@nmbu.no, petter.storesund.hetland@nmbu.no'


class Animal:

    """
    Super class for Herbivores and Carnivores
    """

    def __init__(self, weight, age=0):
        self.weight = weight
        self.age = age

    def eat_fodder(self, beta=0.9, F=10):
        """
        When an animal eats, its weight increases

        """
        self.weight += beta * F
        return self.weight

    def aging(self):
        """
        Increment age by one every season
        """
        self.age += 1
        return self.age

    """
    Source: Afternoon lecture INF200. 2. June 2020
    Comment: Consider merging the two function in one, not working as it should
    Suggestions?
    """
    @classmethod
    def q(cls, sgn, x, xhalf, phi):
        return 1. / (1. + np.exp(sgn * phi * (x - xhalf)))

    """
    Source: Afternoon lecture INF200. 2. June 2020
    """
    @classmethod
    def fitness(cls, q, age, weight):
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
        return (q(+1, age, p['a_half'], p['phi_age'])
                * q(-1, weight, p['w_half'], p['phi_weight']))


class Herbivore(Animal):
    def __init__(self, weight, age):
        super().__init__(weight, age)