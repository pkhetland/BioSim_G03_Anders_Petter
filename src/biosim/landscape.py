
# -*- coding: utf-8 -*-

"""
Lowland class for the simulation.
"""

import numpy as np


class Lowland:
    """
    Args...
    """
    def __init__(self, f_max=800.0, location=None):
        self.f_max = f_max  # Set fodder amount for each new year
        self.fodder = f_max  # Set starting fodder amount to f_max
        # if location:
        #     self.location = location


class Highland:
    pass


class Desert:
    pass


class Ocean:
    pass