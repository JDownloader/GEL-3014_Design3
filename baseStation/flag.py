import json
from os import path

here = path.abspath(path.dirname(__file__))


class Flag():
    FLAGS_FILE = here + '/flags.json'
    cubes_of_tiles = [None]*9;

    def __init__(self, country):
        json_data=open(self.FLAGS_FILE)
        data = json.load(json_data)
        self.flag_matrix = data[country]

    def get_matrix(self):
        tiles = [None]*9
        i = 0
        for tile in tiles:
            if self.cubes_of_tiles[i] is None and self.flag_matrix[i] is not None:
                tiles[i] = self.flag_matrix[i]+'_p'
            else:
                tiles[i] = self.flag_matrix[i]
            i += 1
        return tiles