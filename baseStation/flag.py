import json
from os import path

here = path.abspath(path.dirname(__file__))


class Flag():
    FLAGS_FILE = here + '/flags.json'
    NUMBER_OF_TILES_IN_FLAG = 9
    cubes_of_tiles = [None]*NUMBER_OF_TILES_IN_FLAG

    def __init__(self, country):
        json_data=open(self.FLAGS_FILE)
        data = json.load(json_data)
        self.flag_matrix = data[country]

    def get_matrix(self):
        tiles = [None]*self.NUMBER_OF_TILES_IN_FLAG
        i = 0
        for tile in tiles:
            if self.cubes_of_tiles[i] is None and self.flag_matrix[i] is not None:
                tiles[i] = self.flag_matrix[i]+'_p'
            else:
                tiles[i] = self.flag_matrix[i]
            i += 1
        return tiles