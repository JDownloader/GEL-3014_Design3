from vision.cube import Cube
from vision.visiontools import VisionTools


class CubeFinder():
    def __init__(self, kinect):
        self.kinect = kinect
        self.cubes = []

    def get_all_cubes(self):
        return self.cubes

    def add_cube(self, cube):
        if cube not in self.cubes:
            self.cubes.append(cube)

    def refresh_position(self):
        image_rgb = VisionTools().get_image_rgb(self.kinect.grab_new_image())
        image_hsv = VisionTools().get_hsv_image(image_rgb)
        for cube in self.cubes:
            cube.find_position(image_hsv, self.kinect)
            print(cube.color + str(cube.position))


class DemoCubeFinder(CubeFinder):
    def __init__(self, kinect):
        CubeFinder.__init__(self, kinect)
        self.add_cube(Cube('red'))
        self.add_cube(Cube('green'))
        self.add_cube(Cube('blue'))
        self.add_cube(Cube('yellow'))
