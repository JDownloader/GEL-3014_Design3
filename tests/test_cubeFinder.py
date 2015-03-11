from unittest import TestCase
from baseStation.cubeFinder import CubeFinder
from vision.cube import Cube
from mock import Mock

class TestCubeFinder(TestCase):
    empty_cubefinder = CubeFinder()
    single_cube_cubefinder = CubeFinder()
    def setUp(self):
        cube = Cube('red')
        cube.find_position = Mock(return_value=(30,30))
        self.single_cube_cubefinder.add_cube(cube)

    def test_get_all_cubes_is_empty_at_first(self):
        cubes = self.empty_cubefinder.get_all_cubes()
        self.assertEqual(len(cubes), 0)

    def test_get_all_cubes_return_one_for_single_cube(self):
        cubes = self.single_cube_cubefinder.get_all_cubes()
        self.assertEqual(len(cubes), 1)