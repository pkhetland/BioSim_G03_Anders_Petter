# -*- coding: utf-8 -*-

"""
Test set for the initial Lowland class.
"""

from src.landscape import Island, Desert, Highland, Lowland, Water
from src.animal import Herbivore, Carnivore
from src.biosim import BioSim
import pytest


@pytest.fixture
def lowland_cell():
    return Lowland()


def test_lowland_fmax(lowland_cell):
    """Basic Lowland instance can be created with or without argument"""
    assert lowland_cell.params['f_max'] == 800.0


def test_lowland_mainland(lowland_cell):
    """Basic Lowland instance can be created with or without argument"""
    assert lowland_cell.is_mainland


def test_lowland_fodder(lowland_cell):
    """Fodder attribute of instance can be accessed and has the right value"""
    assert lowland_cell.fodder == lowland_cell.params['f_max']


def test_add_remove_animals(lowland_cell):
    animals = [Herbivore(), Carnivore()]
    lowland_cell.add_animals(animals)
    lowland_cell.remove_animals([animals[0]])
    assert len(lowland_cell.animals) == 1


@pytest.fixture
def highland_cell():
    return Highland()


def test_highland_fmax(highland_cell):
    """Basic Lowland instance can be created with or without argument"""
    assert highland_cell.params['f_max'] == 300.0


def test_highland_mainland(highland_cell):
    """Basic Lowland instance can be created with or without argument"""
    assert highland_cell.is_mainland


def test_highland_fodder(highland_cell):
    """Fodder attribute of instance can be accessed and has the right value"""
    assert highland_cell._fodder == highland_cell.params['f_max']


@pytest.fixture
def desert_cell():
    return Desert()


def test_desert_fmax(desert_cell):
    """Basic Lowland instance can be created with or without argument"""
    assert desert_cell.params['f_max'] == 0.0


def test_desert_mainland(desert_cell):
    """Basic Lowland instance can be created with or without argument"""
    assert desert_cell.is_mainland


def test_desert_fodder(desert_cell):
    """Fodder attribute of instance can be accessed and has the right value"""
    assert desert_cell._fodder == desert_cell.params['f_max']


def test_ocean_instance():
    ocean = Water()
    assert not ocean.is_mainland


@pytest.fixture
def island():
    geogr = """WWW
    WLW
    WWW"""
    return Island(map_str=geogr)


def test_landscape(island):
    assert type(island.landscape) == dict


def test_map_str(island):
    assert island.map_str == """WWW
    WLW
    WWW"""


def test_land_cells(island):
    assert type(island.land_cells) == dict
    assert len(island.land_cells) == 1


def test_rows_and_cols(island):
    unique_rows = island.unique_rows
    unique_cols = island.unique_cols
    assert unique_cols == unique_rows == [1, 2, 3]


@pytest.mark.parametrize('bad_boundary',
                         ['H, D, L'])
def test_border(bad_boundary):
    with pytest.raises(ValueError):
        geogr = f"""{bad_boundary}WW
                    WLW
                    WWW"""
        Island(geogr)


@pytest.mark.parametrize('bad_map',
                         ['H, D, L'])
def test_inconcistent_map(bad_map):
    with pytest.raises(ValueError):
        geogr = f"""{bad_map}WWW
                    WLW
                    WWW"""
        Island(geogr)


@pytest.fixture
def biosim():
    ini_pop = [
        {
            "loc": (2, 2),
            "pop": [{"species": "Herbivore", "age": 5, "weight": 20} for _ in range(3)]
        },
        {
            "loc": (2, 2),
            "pop": [{"species": "Carnivore", "age": 4, "weight": 25} for _ in range(2)]
        }
    ]
    geogr = """WWW
    WLW
    WWW"""
    return BioSim(geogr, ini_pop, seed=123)


def test_carn_pop_matrix(biosim):
    biosim._island.update_pop_matrix()
    assert biosim._island.carn_pop_matrix == [[0, 0, 0], [0, 2, 0], [0, 0, 0]]


def test_herb_pop_matrix(biosim):
    biosim._island.update_pop_matrix()
    assert biosim._island.herb_pop_matrix == [[0, 0, 0], [0, 3, 0], [0, 0, 0]]


def test_animal_weights(biosim):
    assert biosim._island.animal_weights == [[20.0, 20.0, 20.0], [25.0, 25.0]]


def test_animal_age(biosim):
    assert biosim._island.animal_ages == [[5.0, 5.0, 5.0], [4.0, 4.0]]


def test_animal_fitness(biosim):
    fixed_herb_fitness = Herbivore(weight=20, age=5).fitness
    fixed_carn_fitness = Carnivore(weight=25, age=4).fitness
    assert biosim._island.animal_fitness == [
        [fixed_herb_fitness, fixed_herb_fitness, fixed_herb_fitness],
        [fixed_carn_fitness, fixed_carn_fitness]
    ]
