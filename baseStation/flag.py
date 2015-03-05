import json
from os import path

here = path.abspath(path.dirname(__file__))


class Flag():
    FLAGS_FILE = 'flags.json'

    def __init__(self, country):
        json_data=open(self.FLAGS_FILE)
        data = json.load(json_data)
        self.flag_matrix = data[country]
        print self.flag_matrix
        print type(self.flag_matrix)

    def get_matrix(self):
        return self.flag_matrix