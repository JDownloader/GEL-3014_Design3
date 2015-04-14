from vision.cube import Cube, WhiteCube, BlackCube, FormStencil
from vision.visiontools import VisionTools
from vision.robotLocator import Position
import time
import numpy as np

class CubeFinder():
    def __init__(self, kinect):
        self.kinect = kinect
        self.cubes = []

    def get_all_cubes(self):
        return self.cubes

    def add_cube(self, cube):
        if cube not in self.cubes:
            self.cubes.append(cube)

    def get_cube_position_with_color(self, color):
        if color == 'black':
            cube = BlackCube()
        elif color == 'white':
            cube = WhiteCube()
        else:
            cube=Cube(color)
        for x in range(0, 20):
            image_hsv = self.get_hsv_with_stencil(color)
            cube.find_position(image_hsv, self.kinect)
            if cube.position is not None:
                if Position(cube.position[0], cube.position[1]).is_valid():
                    break
            time.sleep(0.2)
        self.cubes.append(cube)
        return cube.position

    def get_hsv_with_stencil(self, color):
        image_rgb = self.kinect.grab_new_image(bilateral_filter_activated=True)
        image_hsv = VisionTools().get_hsv_image(image_rgb)
        if self.color_already_there(color):
            stencil = [np.array([[0, 258], [366, 258], [366, 480], [0, 480]], np.int32)]
            image_hsv = FormStencil(stencil).apply(image_hsv)
        return image_hsv

    def color_already_there(self, color):
        for cube in self.cubes:
            if cube.color == color:
                return True
        return False

    def refresh_position(self):
        image_rgb = self.kinect.grab_new_image(True)
        image_hsv = VisionTools().get_hsv_image(image_rgb)
        for cube in self.cubes:
            cube.find_position(image_hsv, self.kinect)
            # print(cube.color + str(cube.position))


class DemoCubeFinder(CubeFinder):
    def __init__(self, kinect):
        CubeFinder.__init__(self, kinect)
        self.add_cube(Cube('red'))
        # self.add_cube(Cube('green'))
        # self.add_cube(Cube('blue'))
        # self.add_cube(Cube('yellow'))
        # self.add_cube(WhiteCube())
        # self.add_cube(BlackCube())
