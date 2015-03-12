from unittest import TestCase
from baseStation.cubeFinder import CubeFinder
from vision.cube import Cube
from mock import Mock


class TestCubeFinder(TestCase):
    CUBE_COLOR = 'red'
    CUBE_X = 30
    CUBE_Y = 31
    
    def setUp(self):
        fake_kinect = None
        self.empty_cubefinder = CubeFinder(fake_kinect)
        self.single_cube_cubefinder = CubeFinder(fake_kinect)
        cube = Cube(self.CUBE_COLOR)
        cube.find_position = Mock(return_value=(self.CUBE_X, self.CUBE_Y))
        cube.position = (self.CUBE_X, self.CUBE_Y)
        self.single_cube_cubefinder.add_cube(cube)

    def test_get_all_cubes_is_empty_at_first(self):
        cubes = self.empty_cubefinder.get_all_cubes()
        self.assertEqual(len(cubes), 0)

    def test_get_all_cubes_contains_one_for_single_cube(self):
        cubes = self.single_cube_cubefinder.get_all_cubes()
        self.assertEqual(len(cubes), 1)

    def test_get_all_cubes_return_return_new_added_cube(self):
        is_inside_cubes = False
        cube = Cube('blue')
        self.empty_cubefinder.add_cube(cube)
        cubes = self.empty_cubefinder.get_all_cubes()
        if cube in cubes:
            is_inside_cubes = True
        assert is_inside_cubes

    def test_cant_add_same_instance_two_time(self):
        cube = Cube('blue')
        self.empty_cubefinder.add_cube(cube)
        self.empty_cubefinder.add_cube(cube)
        cubes = self.empty_cubefinder.get_all_cubes()
        self.assertEqual(len(cubes), 1)

    def test_get_position_list(self):
        array = [[self.CUBE_X, self.CUBE_Y, self.CUBE_COLOR,]]
        self.assertEqual(self.single_cube_cubefinder.get_cubes_positions(), array)