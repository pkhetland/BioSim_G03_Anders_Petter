# -*- coding: utf-8 -*-

"""
Test set for the initial Lowland class.
"""


import pytest

from src import BioSim


def test_map_from_str():
    sim = BioSim(
        island_map = """WWW
        WLW
        WWW""")
    assert sim.landscape is not None