import time

class RunLoop:
    startTime = None;

    def __init__(self):
        return None

    def start(self):
        self.startTime = time.time()

    def getTime(self):
        return time.time()-self.startTime;