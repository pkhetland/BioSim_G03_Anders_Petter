# -*- coding: utf-8 -*-

"""
Test set for the initial Lowland class.
"""

from biosim_src.landscape import Island, Desert, Highland, Lowland, Water
from biosim_src.animal import Herbivore, Carnivore
from biosim_src.biosim import BioSim
import pytest

"""
Tests of classes in landscape.py. Check if classes behaves as expected
"""


class TestHighlandLandscapeCell:

    @pytest.fixture
    def highland_cell(self):
        """Create basic Highland instance for testing"""
        return Highland()

    def test_highland_fmax(self, highland_cell):
        """
        :property: Highland.params
        Test that highland parameters are correct
        """
        assert highland_cell.params['f_max'] == 300.0

    def test_highland_mainland(self, highland_cell):
        """
        :property: Highland.params
        Test that is_mainland property is True
        """
        assert highland_cell.is_mainland

    def test_highland_fodder(self, highland_cell):
        """
        :cls property: Highland._fodder
        Fodder attribute of instance can be accessed and has the right value
        """
        assert highland_cell._fodder == highland_cell.params['f_max']

    def test_fodder_setter(self, highland_cell):
        """
        :setter: LandscapeCell.fodder
        :property: Highland._fodder
        Fodder attribute of instance can be accessed and has the right value
        """
        highland_cell.fodder = 200.0
        assert highland_cell._fodder == 200.0

    def test_reset_animals(self, highland_cell):
        """
        :method: LandscapeCell.add_animal
        :method: LandscapeCell.reset_animals
        :property: LandscapeCell.carnivores
        :property: LandscapeCell.has_moved
        Test that has_moved property is correctly set and reset
        """
        highland_cell.add_animals([Carnivore(), Herbivore()])
        highland_cell.carnivores[0].has_moved = True
        highland_cell.reset_animals()
        assert highland_cell.carnivores[0].has_moved is False

    def test_shuffle_herbs(self, highland_cell):
        """
        :method: LandscapeCell.add_animals
        :method: LandscapeCell.randomize_herbs
        Test that shuffle method shuffles herbivores list
        """
        highland_cell.add_animals([Herbivore() for _ in range(1000)])
        original_herbs = [animal for animal in highland_cell.herbivores]
        highland_cell.randomize_herbs()
        assert highland_cell.herbivores != original_herbs

    def test_repr_and_str(self, highland_cell):
        """
        Test __repr__ and __str__ dunder methods for Highland cell
        """
        assert repr(highland_cell) == str(highland_cell) == 'Highland(f_max: 300.0)'

    def test_set_params(self, highland_cell):
        """
        :cls method: Highland.set_params
        Test that error is raised when invalid key is passed
        """
        with pytest.raises(AttributeError):
            highland_cell.set_params({'ff_maxx': 200.0})

    def test_add_remove_animals(self, highland_cell):
        """
        :method: LandscapeCell.add_animals
        :method: LandscapeCell.remove_animals
        :property: LandscapeCell.animal_count
        Test that animals can be added and removed correctly
        """
        animals = [Herbivore(), Carnivore(), Herbivore()]
        highland_cell.add_animals(animals)
        highland_cell.remove_animals([animals[0], animals[1]])
        assert highland_cell.herb_count == 1

    @pytest.mark.parametrize('add_remove_func',
                             ['add', 'remove'])
    def test_invalid_add_remove_animals(self, highland_cell, add_remove_func):
        """
        :method: LandscapeCell.add_animals
        :method: LandscapeCell.remove_animals
        Test that error is raised when non-instance objects are passed to methods
        """
        with pytest.raises(ValueError):
            if add_remove_func == 'add':
                highland_cell.add_animals(['Herbivore'])
            else:
                highland_cell.remove_animals(['Carnivore'])

    def test_sorted_herbivores_and_carnivores(self, highland_cell):
        """
        :method: LandscapeCell.add_animals
        :method: LandscapeCell.sorted_herbivores
        :method: LandscapeCell.sorted_carnivores
        Check that sorting algorithms sort the lists by fitness
        """
        highland_cell.add_animals([Herbivore(weight=50), Herbivore(weight=20)])
        highland_cell.add_animals([Carnivore(weight=25), Carnivore(weight=40)])
        assert highland_cell.sorted_herbivores == highland_cell.herbivores[::-1]
        assert highland_cell.sorted_carnivores == highland_cell.carnivores[::-1]

    def test_is_empty(self, highland_cell):
        """
        :setter: LandscapeCell.fodder
        :property: LandscapeCell.is_empty
        """
        highland_cell.fodder = 0
        assert highland_cell.is_empty is True


class TestLowland:
    @pytest.fixture
    def lowland_cell(self):
        """Create basic Lowland instance"""
        return Lowland()

    def test_lowland_fmax(self, lowland_cell):
        """
        :cls property: Lowland.params
        Check that f_max is correct
        """
        assert lowland_cell.params['f_max'] == 800.0

    def test_lowland_mainland(self, lowland_cell):
        """
        :property: LandscapeCell.is_mainland
        Check that is_mainland returns True
        """
        assert lowland_cell.is_mainland

    def test_lowland_fodder(self, lowland_cell):
        """
        :property: LandscapeCell.fodder
        Fodder attribute of instance can be accessed and has the right value
        """
        assert lowland_cell.fodder == lowland_cell.params['f_max']


class TestDesert:
    @pytest.fixture
    def desert_cell(self):
        """Create basic desert instance"""
        return Desert()

    def test_desert_fmax(self, desert_cell):
        """
        :cls property: Desert.params
        Test that class parameters are correct
        """
        assert desert_cell.params['f_max'] == 0.0

    def test_desert_mainland(self, desert_cell):
        """
        :property: LandscapeCell.is_mainland
        Test that is_mainland returns True
        """
        assert desert_cell.is_mainland

    def test_desert_fodder(self, desert_cell):
        """
        :property: LandscapeCell._fodder
        Fodder attribute of instance can be accessed and has the right value
        """
        assert desert_cell._fodder == desert_cell.params['f_max']


class TestWater:

    def test_water_instance(self):
        """
        :cls property: Water.is_mainland
        Test that is_mainland returns False
        """
        water = Water()
        assert not water.is_mainland

    def test_repr_and_str_water(self):
        """
        :method: Water.__repr__
        :method: Water.__str__
        Test that dunder methods return correct value
        """
        water = Water()
        assert repr(water) == str(water) == 'Water cell'


class TestIsland:

    @pytest.mark.parametrize('bad_boundary',
                             ['H', 'D', 'L'])
    def test_border(self, bad_boundary):
        """Test that invalid border raises error
        Modified from author Hans E. Plasser"""
        with pytest.raises(ValueError):
            geogr = f"""{bad_boundary}WW
                        WLW
                        WWW"""
            Island(geogr)

    @pytest.mark.parametrize('bad_map',
                             ['H, D, L'])
    def test_inconsistent_map(self, bad_map):
        """Test that invalid row lengths raise error
        Modified from author Hans E. Plasser"""
        with pytest.raises(ValueError):
            geogr = f"""{bad_map}WWW
                        WLW
                        WWW"""
            Island(geogr)

    def test_invalid_map(self):
        """Test that invalid map symbols raise error"""
        with pytest.raises(ValueError):
            geogr = f"""WWW
                        WSW
                        WWW"""
            Island(geogr)

    @pytest.fixture
    def island(self):
        """Create basic Island instance for testing"""
        geogr = """WWWW
        WLHW
        WDWW
        WWWW"""
        return Island(map_str=geogr)

    def test_count_del_animals(self, island):
        """
        :method: Island.count_animals
        :method: Island.del_animals
        Test counting and removing animals with lists passed and arguments only
        """
        island.count_animals(num_herbs=10, num_carns=10)
        island.del_animals(animal_list=[Herbivore()])
        island.del_animals(num_herbs=5, num_carns=5)
        assert island.num_animals == 9
        assert island.num_herbs == 4
        assert island.num_carns == 5

    def test_island_instance(self, island):
        """Test that island is an instance of Island"""
        assert isinstance(island, Island)

    def test_landscape(self, island):
        """
        :property: Island.landscape
        Test that landscape property is of type `dict`
        """
        assert type(island.landscape) == dict

    def test_map_str(self, island):
        """
        :property: Island.map_str
        Test that map_str property matches initial input
        """
        assert island.map_str == """WWWW
        WLHW
        WDWW
        WWWW"""

    def test_land_cells(self, island):
        """
        :property: Island.land_cells
        Test that land_cells property is of correct type and length
        """
        assert type(island.land_cells) == dict
        assert len(island.land_cells) == 3

    def test_rows_and_cols(self, island):
        """
        :property: Island.unique_rows
        :property: Island.unique_cols
        Test that row and col counters return correct values
        """
        unique_rows = island.unique_rows
        unique_cols = island.unique_cols
        assert unique_cols == unique_rows == [1, 2, 3, 4]

    @pytest.mark.parametrize('params',
                             [('L', {'f_max': 1000.0}),
                              ('H', {'f_max': 200.0})])
    def test_set_landscape_params(self, island, params):
        """
        :method: Island.set_landscape_params
        Test that method alters properties of cells correctly
        """
        island.set_landscape_params(params[0], params[1])
        if params[0] == 'L':
            assert Lowland.f_max() == 1000.0
        elif params[0] == 'H':
            assert Highland.f_max() == 200.0

    def test_set_invalid_landscape_params(self, island):
        """
        :method: Island.set_landscape_params
        Test that invalid key raises error
        """
        with pytest.raises(ValueError):
            island.set_landscape_params('S', {'f_max': 200.0})

    def test_set_neighbors(self, island):
        """
        :property: Island._land_cells
        :property: LandscapeCell.land_cell_neighbors
        Check that neighbors are counted for a sample cell
        """
        assert len(island._land_cells[(2, 2)].land_cell_neighbors) == 2

    @pytest.fixture
    def biosim(self):
        """
        Create a basic Biosim instance for further testing
        """
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

    def test_carn_pop_matrix(self, biosim):
        """
        :method: Island.update_pop_matrix
        Test that carnivore population matrix is of correct shape and value
        """
        biosim._island.update_pop_matrix()
        assert biosim._island.carn_pop_matrix == [[0, 0, 0], [0, 2, 0], [0, 0, 0]]

    def test_herb_pop_matrix(self, biosim):
        """
        :method: Island.update_pop_matrix
        Test that herbivore population matrix is of correct shape and value
        """
        biosim._island.update_pop_matrix()
        assert biosim._island.herb_pop_matrix == [[0, 0, 0], [0, 3, 0], [0, 0, 0]]

    def test_animal_weights(self, biosim):
        """
        :property: Island.animal_weights
        Test that animal weights property is of correct shape and value
        """
        assert biosim._island.animal_weights == [[20.0, 20.0, 20.0], [25.0, 25.0]]

    def test_animal_age(self, biosim):
        """
        :property: Island.animal_ages
        Test that animal ages property is of correct shape and value
        """
        assert biosim._island.animal_ages == [[5.0, 5.0, 5.0], [4.0, 4.0]]


    def test_animal_fitness(self, biosim):
        """
        :property: Island.animal_fitness
        Test that animal fitness property is of correct shape and value
        """
        fixed_herb_fitness = Herbivore(weight=20, age=5).fitness
        fixed_carn_fitness = Carnivore(weight=25, age=4).fitness
        assert biosim._island.animal_fitness == [
            [fixed_herb_fitness, fixed_herb_fitness, fixed_herb_fitness],
            [fixed_carn_fitness, fixed_carn_fitness]
        ]
