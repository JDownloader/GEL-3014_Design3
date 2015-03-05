import time
from flagLoop import FlagLoop

class RunLoop:
    startTime = None;

    def __init__(self):
        self.flag_loop = FlagLoop()

    def start(self):
        self.startTime = time.time()

    def get_time(self):
        if self.startTime is None:
            return 0
        return time.time()-self.startTime;

    def get_current_json_flag(self):
        return self.flag_loop.get_json_flag()