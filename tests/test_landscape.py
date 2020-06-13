# -*- coding: utf-8 -*-

"""
Test set for the initial Lowland class.
"""

from src.landscape import Island, Desert, Highland, Lowland, Water
from src.animal import Herbivore, Carnivore
from src.biosim import BioSim
import pytest


"""
================== TEST HIGHLAND AND LANDSCAPECELL ==================
"""


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


def test_fodder_setter(highland_cell):
    """Fodder attribute of instance can be accessed and has the right value"""
    highland_cell.fodder = 200.0
    assert highland_cell._fodder == 200.0


def test_reset_animals(highland_cell):
    highland_cell.add_animals([Carnivore(), Herbivore()])
    highland_cell.carnivores[0].has_moved = True
    highland_cell.reset_animals()
    assert highland_cell.carnivores[0].has_moved is False


def test_shuffle_herbs(highland_cell):
    highland_cell.add_animals([Herbivore() for _ in range(1000)])
    original_herbs = [animal for animal in highland_cell.herbivores]
    highland_cell.randomize_herbs()
    assert highland_cell.herbivores != original_herbs


def test_repr_and_str(highland_cell):
    assert repr(highland_cell) == str(highland_cell) == 'Highland(f_max: 300.0)'


def test_set_params(highland_cell):
    with pytest.raises(AttributeError):
        highland_cell.set_params({'ff_maxx': 200.0})


def test_add_remove_animals(highland_cell):
    animals = [Herbivore(), Carnivore(), Herbivore()]
    highland_cell.add_animals(animals)
    highland_cell.remove_animals([animals[0], animals[1]])
    assert highland_cell.animal_count == 1


@pytest.mark.parametrize('add_remove_func',
                         ['add', 'remove'])
def test_invalid_add_remove_animals(highland_cell, add_remove_func):
    with pytest.raises(AttributeError):
        if add_remove_func == 'add':
            highland_cell.add_animals(['Herbivore'])
        else:
            highland_cell.remove_animals((['Carnivore']))


def test_sorted_herbivores_and_carnivores(highland_cell):
    highland_cell.add_animals([Herbivore(weight=50), Herbivore(weight=20)])
    highland_cell.add_animals([Carnivore(weight=25), Carnivore(weight=40)])
    assert highland_cell.sorted_herbivores == highland_cell.herbivores[::-1]
    assert highland_cell.sorted_carnivores == highland_cell.carnivores[::-1]


def test_is_empty(highland_cell):
    highland_cell.fodder = 0
    assert highland_cell.is_empty is True


"""
================== TEST LOWLAND ==================
"""


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


"""
================== TEST DESERT ==================
"""

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


"""
================== TEST OCEAN ==================
"""

def test_ocean_instance():
    water = Water()
    assert not water.is_mainland

def test_repr_and_str_water():
    water = Water()
    assert repr(water) == str(water) == 'Water cell'


"""
================== TEST ISLAND ==================
"""


@pytest.mark.parametrize('bad_boundary',
                         ['H', 'D', 'L'])
def test_border(bad_boundary):
    with pytest.raises(ValueError):
        geogr = f"""{bad_boundary}WW
                    WLW
                    WWW"""
        Island(geogr)


@pytest.mark.parametrize('bad_map',
                         ['H, D, L'])
def test_inconsistent_map(bad_map):
    with pytest.raises(ValueError):
        geogr = f"""{bad_map}WWW
                    WLW
                    WWW"""
        Island(geogr)


def test_invalid_map():
    with pytest.raises(ValueError):
        geogr = f"""WWW
                    WSW
                    WWW"""
        Island(geogr)


@pytest.fixture
def island():
    geogr = """WWWW
    WLHW
    WDWW
    WWWW"""
    return Island(map_str=geogr)


def test_count_del_animals(island):
    island.count_animals(num_herbs=10, num_carns=10)
    island.del_animals(animal_list=[Herbivore()])
    island.del_animals(num_herbs=5, num_carns=5)
    assert island.num_animals == 9
    assert island.num_herbs == 4
    assert island.num_carns == 5


def test_island_instance(island):
    assert isinstance(island, Island)


def test_landscape(island):
    assert type(island.landscape) == dict


def test_map_str(island):
    assert island.map_str == """WWWW
    WLHW
    WDWW
    WWWW"""


def test_land_cells(island):
    assert type(island.land_cells) == dict
    assert len(island.land_cells) == 3


def test_rows_and_cols(island):
    unique_rows = island.unique_rows
    unique_cols = island.unique_cols
    assert unique_cols == unique_rows == [1, 2, 3, 4]


@pytest.mark.parametrize('params',
                         [('L', {'f_max': 1000.0}),
                          ('H', {'f_max': 200.0})])
def test_set_landscape_params(island, params):
    island.set_landscape_params(params[0], params[1])
    if params[0] == 'L':
        assert Lowland.f_max() == 1000.0
    elif params[0] == 'H':
        assert Highland.f_max() == 200.0


def test_set_invalid_landscape_params(island):
    with pytest.raises(AttributeError):
        island.set_landscape_params('S', {'f_max': 200.0})


def test_set_neighbors(island):
    assert len(island._land_cells[(2, 2)].land_cell_neighbors) == 2


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
