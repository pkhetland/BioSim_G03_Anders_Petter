# -*- coding: utf-8 -*-

"""
Test set for the initial Lowland class.
"""


import pytest
import glob
import os
import os.path

from src.animal import Herbivore, Carnivore
from src.biosim import BioSim
from src.landscape import Lowland, Highland

"""
====================== TEST BIOSIM CLASS ======================
"""


def test_map_from_str():
    """
    Test that the map string is properly saved
    """
    island_map = """WWW
            WDW
            WWW"""
    sim = BioSim(island_map=island_map)
    assert sim._island.map_str == island_map


def test_default_map():
    """
    Test that a default map is created if no map is given
    """
    sim = BioSim(island_map=None)
    assert sim._island.map_str == """WWW\nWLW\nWWW"""


def test_invalid_map():
    """
    That ValueError from invalid map
    """
    with pytest.raises(ValueError):
        BioSim(island_map=['WWW\nWLW\nWWW'])


@pytest.fixture
def biosim():
    """
    Create basic map instance for testing
    """
    return BioSim(island_map='WWW\nWLW\nWWW')


def test_repr_and_str(biosim):
    """
    Test the __repr__ and __str__ functions
    """
    biosim.add_population([{'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 20}]}])
    animal = biosim._island.landscape[(2, 2)].herbivores[0]
    assert repr(animal) == str(animal) == 'Herbivore(5 years, 20.0 kg)'


def test_set_animal_parameters(biosim):
    """
    :method: Biosim.set_animal_parameters I
    Test the 'set_animal_parameters' function
    """
    assert Herbivore.p['F'] == 10
    assert Carnivore.p['w_half'] == 4
    biosim.set_animal_parameters('Herbivore', {'F': 20})
    biosim.set_animal_parameters('Carnivore', {'w_half': 6})
    assert Herbivore.p['F'] == 20
    assert Carnivore.p['w_half'] == 6


def test_invalid_animal_param_key(biosim):
    """
    :method: Biosim.set_animal_parameters II
    Test invalid key passed to the function
    """
    with pytest.raises(KeyError):
        biosim.set_animal_parameters(species='Herbivore', params={'FF': 20})


def test_invalid_animal_param_value(biosim):
    """
    :method: Biosim.set_animal_parameters III
    Test invalid value passed to the function
    """
    with pytest.raises(ValueError):
        biosim.set_animal_parameters(species='Herbivore', params={'F': -20})


def test_invalid_animal_parameters(biosim):
    """
    :method: Biosim.set_animal_parameters IV
    Test invalid 'species' parameter
    """
    with pytest.raises(ValueError):
        biosim.set_animal_parameters(species='Derpivore', params={'F': 20})


def test_set_landscape_parameters(biosim):
    """
    :method: Biosim.set_landscape_parameters I
    Test that landscape params can be set correctly
    """
    assert Lowland.f_max() == 800.0
    assert Highland.f_max() == 300.0
    biosim.set_landscape_parameters('L', {'f_max': 700.0})
    biosim.set_landscape_parameters('H', {'f_max': 250.0})
    assert Lowland.f_max() == 700.0
    assert Highland.f_max() == 250.0


def test_invalid_landscape_parameters(biosim):
    """
    :method: Biosim.set_landscape_parameters II
    Test invalid key sent to function
    """
    with pytest.raises(ValueError):
        biosim.set_landscape_parameters('S', {'f_max': 20.0})


def test_add_invalid_pop(biosim):
    """
    :method: Biosim.add_population I
    Test if animals can be added through dictionary
    """
    with pytest.raises(ValueError):
        biosim.add_population({
            "loc": (2, 2),
            "pop": [{"species": "Carnivore", "age": 5, "weight": 20} for _ in range(20)]
        })


@pytest.fixture
def biosim_with_animals():
    """
    Create Biosim instance with population for further testing
    """
    biosim = BioSim(island_map='WWWWW\nWLDHW\nWWWWW')
    biosim.add_population([
        {
            "loc": (2, 2),
            "pop": [{"species": "Carnivore", "age": 5, "weight": 20} for _ in range(20)]
        },
        {
            "loc": (2, 2),
            "pop": [{"species": "Herbivore", "age": 5, "weight": None} for _ in range(50)]
        },
        {
            "loc": (2, 3),
            "pop": [{"species": "Herbivore", "age": 5, "weight": 0} for _ in range(20)]
        }
    ])
    return biosim


def test_add_population(biosim_with_animals):
    """
    :method: Biosim.add_population II
    :property: Biosim.num_animals I
    :property: Biosim.num_animals_per_species I
    Test that animals are added and counted correctly
    """
    assert biosim_with_animals.num_animals == 90
    assert biosim_with_animals.num_animals_per_species == {'Herbivore': 70, 'Carnivore': 20}


def test_year_cycle(biosim_with_animals):
    """
    :method: Biosim.run_year_cycle I
    Test that function can be run with population
    """
    biosim_with_animals.run_year_cycle()


def test_simulate(biosim_with_animals):
    """
    :method: Biosim.simulate I
    :property: Biosim.year I
    Test that simulation can be run without visuals and years are counted
    """
    biosim_with_animals.simulate(num_years=500, vis_years=1, img_years=None)
    assert biosim_with_animals.year == 500


def test_simulate_extreme(biosim_with_animals):
    """
    :method: Biosim.simulate II
    :method: Biosim.set_animal_parameters II
    Test that certain chance of killing prey is 1 if DeltaPhiMax is triggered in kill_preys
    """
    biosim_with_animals.set_animal_parameters('Carnivore', {'DeltaPhiMax': 0.7})
    biosim_with_animals.simulate(num_years=100, vis_years=1, img_years=None)


@pytest.fixture
def figfile_root():
    """
    Provide name for figfile root and delete figfiles after test completes.
    Author: Hans Ekkehard Plesser
    """
    ffroot = os.path.join('.', 'testfigroot')
    yield ffroot
    for f in glob.glob(ffroot + '_0*.png'):
        os.remove(f)


def test_figure_saved(figfile_root):
    """
    :method: Biosim.simulate II
    Test that figures are saved during simulation.
    Author: Hans Ekkehard Plesser
    """

    sim = BioSim(island_map="WWWW\nWLHW\nWWWW",
                 ini_pop=[],
                 seed=1,
                 img_base=figfile_root,
                 img_fmt='png',
                 plot_graph=True)
    sim.simulate(2, vis_years=1, img_years=None)
    sim.simulate(2, vis_years=1, img_years=1)

    assert os.path.isfile(figfile_root + '_00000.png')
    assert os.path.isfile(figfile_root + '_00001.png')
    assert os.path.isfile(figfile_root + '_00002.png')
    assert os.path.isfile(figfile_root + '_00003.png')
