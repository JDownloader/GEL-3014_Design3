import time

class RunLoop:
    startTime = None;

    def __init__(self):
        return None

    def start(self):
        self.startTime = time.time()

    def get_time(self):
        if self.startTime is None:
            return 0
        return time.time()-self.startTime;