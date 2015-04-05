import json
from flag import Flag


class FlagProcessor():
    def __init__(self):
        self.flag = Flag('Australia')

    def get_flag(self):
        return self.flag.get_matrix()