# -*- coding: utf-8 -*-

__author__ = 'Anders Mølmen Høst & Petter Kolstad Hetland'
__email__ = 'anders.molmen.host@nmbu.no, petter.storesund.hetland@nmbu.no'

"""
Super class for Herbivores and Carnivores
"""


class Animal:

    def __init__(self, landscape, weight=None):
        self._landscape = landscape
        self.weight = weight
        self.age = 0

    @property
    def eat_fodder(self, beta=0.9, F=10):
        """
        When an animal eats, its weight increases

        """
        self.weight += beta * F
        return self.weight
