from vision import cube




class CubeFinder():
    def __init__(self):
        self.cubes = []

    def get_all_cubes(self):
        return self.cubes

    def add_cube(self, cube):
        if cube not in self.cubes:
            self.cubes.append(cube)

    def get_cubes_positions(self):
        cubes_positions = []
        for cube in self.cubes:
            cubes_positions.append([cube.position[0], cube.position[1], cube.color])
        return cubes_positions


class DemoCubeFinder(CubeFinder):
    def __init__(self):
        CubeFinder.__init__(self)