import time
import random
from vision.kinect import Kinect
from cubeFinder import CubeFinder, DemoCubeFinder
from time import gmtime, strftime
from flagLoop import FlagLoop

class RunLoop:
    startTime = None;

    def __init__(self):
        self.flag_loop = FlagLoop()
        self.kinect = Kinect()
        self.cube_finder = DemoCubeFinder(self.kinect)

    def start(self):
        self.startTime = time.time()

    def get_time(self):
        if self.startTime is None:
            return 0
        return time.time()-self.startTime;

    def _get_current_flag(self):
        return self.flag_loop.get_flag()

    def get_status(self, robot_ip):
        pos_y = random.randrange(0, 400, 1)
        run_time = self.get_time()
        sample_status = { "top": 30,
                          "left": pos_y,
                          "chrono": strftime("%Mm%Ss",gmtime(run_time)),
                          "robotIP": robot_ip,
                          "flag": self._get_current_flag(),
                          "cubes": self.cube_finder.get_cubes_positions()}
        # "cubes": [[20, 20 , 'red'], [20, 100, 'blue']]
        return sample_status