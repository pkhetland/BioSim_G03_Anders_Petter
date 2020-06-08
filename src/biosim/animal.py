# -*- coding: utf-8 -*-

__author__ = "Anders Mølmen Høst & Petter Kolstad Hetland"
__email__ = "anders.molmen.host@nmbu.no, petter.storesund.hetland@nmbu.no"

import numpy as np
import random as random


class Animal:
    """
    Super class for Herbivores and Carnivores
    """

    # instance_count = 0

    def __init__(self, weight, age):
        if weight is None:
            self.weight = self.birth_weight
        else:
            self.weight = weight
        self.age = age
        self.death_prob = None

        np.random.seed(123)

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
            give_birth = np.random.choice([True, False], p=[birth_prob, 1 - birth_prob])
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
        move_prob = self.p['mu'] * self.fitness
        return np.random.choice([True, False], p=[move_prob, 1-move_prob])

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
            return True
        else:
            if self.death_prob is None:
                self.death_prob = self.p["omega"] * (1 - self.fitness)
                death = np.random.choice([True, False], p=[self.death_prob, 1-self.death_prob])
                self.death_prob = None
                return death

    # @classmethod
    # def add_animal(cls):
    #     cls.instance_count += 1
    #
    # @classmethod
    # def remove_animal(cls):
    #     cls.instance_count -= 1

    @staticmethod
    def q(sgn, x, x_half, phi):
        return 1.0 / (1.0 + np.exp(sgn * phi * (x - x_half)))

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
    def __init__(self, weight=None, age=0, p=None):

        if p is None:  # If no parameters are specified
            self.p = {  # Insert default values for species
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
        else:
            self.p = p

        super().__init__(weight, age)
        # super().add_animal()

    def eat_fodder(self, cell):
        """
        When an animal eats, its weight increases
        """
        consumption_amount = self.p["beta"] * self.p["F"]  # Calculate amount of fodder consumed
        if consumption_amount <= cell.fodder:
            self.weight += consumption_amount  # Eat fodder
            cell.fodder -= consumption_amount  # Removes consumed fodder from cell object

        elif consumption_amount > cell.fodder > 0:
            self.weight += cell.fodder  # Eat fodder
            cell.fodder = 0  # Sets fodder to zero.

        else:
            print("Out of food")
            return


class Carnivore(Animal):
    """
    Carnivore class
    """

    def __init__(self, weight=None, age=0, p=None):
        if p is None:  # If no parameters are specified
            self.p = {  # Insert default values for species
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
        else:
            self.p = p

        super().__init__(weight, age)
        # super().add_animal()

    def kill_prey(self, sorted_herbivores):
        consumption_weight = 0
        herbs_killed = []

        for herb in sorted_herbivores:
            if consumption_weight < self.p["F"]:
                fitness_diff = self.fitness - herb.fitness
                if fitness_diff <= 0:
                    kill_prey = False

                elif 0 < fitness_diff < self.p["DeltaPhiMax"]:
                    kill_prob = fitness_diff / self.p["DeltaPhiMax"]
                    kill_prey = np.random.choice([True, False], p=[kill_prob, 1 - kill_prob])

                else:
                    kill_prey = True

                if kill_prey:  # If the herb is killed
                    consumption_weight += (
                        herb.weight
                    )  # Add herb weight to consumption_weight variable
                    herbs_killed.append(herb)

        if consumption_weight > self.p["F"]:  # Auto-adjust consumption_weight to be <= F-parameter
            consumption_weight = self.p["F"]

        self.weight += consumption_weight * self.p["beta"]  # Add weight to carnivore

        return herbs_killed


#
if __name__ == "__main__":
     herb1 = Herbivore()
     carn1 = Carnivore()
     print(herb1.death())
     print(herb1.fitness)
     print(herb1.birth_weight)
     print(carn1.birth_weight)
