import json
from flag import Flag


class FlagLoop():
    def __init__(self):
        self.flag = Flag('Saudi Arabia')

    def get_flag(self):
        return self.flag.get_matrix()