# -*- coding: utf-8 -*-

"""
Test set for the initial Lowland class.
"""


import pytest

from src.biosim.Lowland import Lowland


def test_lowland_instance():
    """Basic Lowland instance can be created with or without argument"""
    lowland_default = Lowland()
    lowland_100 = Lowland(f_max=100.0)

