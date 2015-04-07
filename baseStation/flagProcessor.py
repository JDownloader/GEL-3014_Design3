import json
from flag import Flag


class FlagProcessor():
    def __init__(self, country):
        self.flag = Flag(country)

    def get_flag(self):
        return self.flag.get_matrix()