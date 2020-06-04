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
    Comment: Consider merging the two function in one
    """

    def q(self, sgn, x, xhalf, phi):
        return 1. / (1. + np.exp(sgn * phi * (x - xhalf)))

    """
    Source: Afternoon lecture INF200. 2. June 2020
    """

    def fitness(self, age, weight, p):
        return (q(+1, age, p['a_half'], p['phi_age'])
                * q(-1, weight, p['w_half'], p['phi_weight']))


class Herbivore(Animal):
    def __init__(self, weight, age):
        super().__init__(weight, age)