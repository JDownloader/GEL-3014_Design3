import json
from flag import Flag


class FlagLoop():
    def __init__(self):
        self.flag = Flag('Canada')

    def get_json_flag(self):
        return self.flag.get_matrix()