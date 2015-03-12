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

    def get_cubes_positions(self):
        self.refresh_position()
        cubes_positions = []
        for cube in self.cubes:
            cubes_positions.append([cube.position[0], cube.position[1], cube.color])
        return cubes_positions

    def refresh_position(self):
        image_rgb = VisionTools().get_image_rgb(self.kinect.grab_new_image())
        image_hsv = VisionTools().get_hsv_image(image_rgb)
        for cube in self.cubes:
            cube.find_position(image_hsv, self.kinect)
            print(cube.color + str(cube.position))


class DemoCubeFinder(CubeFinder):
    def __init__(self, kinect):
        CubeFinder.__init__(self, kinect)
        red_cube = Cube('red')
        green_cube = Cube('green')
        blue_cube = Cube('blue')
        yellow_cube = Cube('yellow')
        self.add_cube(red_cube)
        self.add_cube(green_cube)
        self.add_cube(blue_cube)
        self.add_cube(yellow_cube)