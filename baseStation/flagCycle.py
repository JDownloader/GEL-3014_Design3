import json
from flag import Flag


class FlagCycle():
    def __init__(self):
        self.flag = Flag('Saudi Arabia')

    def get_flag(self):
        return self.flag.get_matrix()