from vision.cube import Cube, WhiteCube, BlackCube, FormStencil
from vision.visiontools import VisionTools
from vision.robotLocator import Position
import time
import numpy as np
from vision.kinectCaptureHelper import KinectCaptureHelper
from vision.kinect import Kinect

TABLE_FLAG_STENCIL = {'1': [np.array([[0, 258], [366, 258], [366, 480], [0, 480]], np.int32)],  # not tested
                      '2': [np.array([[0, 258], [366, 258], [366, 480], [0, 480]], np.int32)],
                      '3': [np.array([[0, 258], [366, 258], [366, 480], [0, 480]], np.int32)],
                      '4': [np.array([[0, 266], [362, 266], [362, 480], [0, 480]], np.int32)],
                      '5': None,
                      '6': None}


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
            # cube = WhiteCube()
            x_positions = []
            y_positions = []
            for x in range(0, 10):
                image_hsv = self.get_hsv_with_stencil(color)
                KinectCaptureHelper().save_kinect_capture(self.kinect, str(time.time()), image_hsv)
                # new_kinect = Kinect('1')
                # image_rgb = new_kinect.grab_new_image(bilateral_filter_activated=True)
                # image_hsv = VisionTools().get_hsv_image(image_rgb)
                new_position = WhiteCube().find_position(image_hsv, self.kinect)
                if new_position is not None:
                    if Position(new_position[0], new_position[1]).is_valid():
                        x_positions.append(new_position[0])
                        y_positions.append(new_position[1])
            print x_positions.__len__()
            if x_positions.__len__() > 3:
                return (self.get_median(x_positions), self.get_median(y_positions))
            return (None, None)
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

    def get_median(self, values):
        return np.median(np.array(values))

    def get_hsv_with_stencil(self, color):
        image_rgb = self.kinect.grab_new_image(bilateral_filter_activated=True)
        image_hsv = VisionTools().get_hsv_image(image_rgb)
        if self.color_already_there(color):
            stencil = TABLE_FLAG_STENCIL.get(str(self.kinect.table))
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

class CubeFinder2():
    def __init__(self, kinect):
        self.kinect = kinect
        self.cubes = []

    def get_all_cubes(self):
        return self.cubes

    def add_cube(self, cube):
        if cube not in self.cubes:
            self.cubes.append(cube)

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
