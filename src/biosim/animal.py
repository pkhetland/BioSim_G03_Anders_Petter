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




class Herbivore(Animal):
    def __init__(self, weight, age):
        super().__init__(weight, age)