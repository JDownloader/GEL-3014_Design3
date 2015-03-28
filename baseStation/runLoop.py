import time
import random
from baseStation.pathFinding import pathFinding
from vision.kinect import Kinect, NoKinectDetectedException
from tests.test_vision import FakeKinect
from cubeFinder import CubeFinder, DemoCubeFinder
from time import gmtime, strftime
from flagCycle import FlagCycle
from controller.serialCom import Robot
import constants

class RunLoop:
    startTime = None;

    def __init__(self):
        self.flag_loop = FlagCycle()
        try:
            self.kinect = Kinect()
        except NoKinectDetectedException:
            self.kinect = FakeKinect()
        self.cube_finder = DemoCubeFinder(self.kinect)
        self.robot = Robot()

    def start(self):
        self.startTime = time.time()
        answer = self.fetch_answer()
        self.construct_flag(answer)

    def get_time(self):
        if self.startTime is None:
            return 0
        return time.time()-self.startTime

    def _get_current_flag(self):
        return self.flag_loop.get_flag()

    def get_status(self, robot_ip):
        pos_y = random.randrange(0, 400, 1)
        run_time = self.get_time()
        sample_status = { 'top': 30,
                          'left': pos_y,
                          'kinect_is_fake': self.is_fake_kinect(),
                          'chrono': strftime('%Mm%Ss', gmtime(run_time)),
                          'robotIP': robot_ip,
                          'flag': self._get_current_flag(),
                          'cubes': self.get_cubes()}
        return sample_status

    def get_cubes(self):#TODO
        self.cube_finder.refresh_position()
        cubes_positions = []
        for cube in self.cube_finder.cubes:
            cubes_positions.append([cube.position[0], cube.position[1], cube.color])
        return cubes_positions

    def is_fake_kinect(self):
        if isinstance(self.kinect, FakeKinect):
            return True
        return False

    def fetch_answer(self):
        actual_position = ''
        self.move_to(actual_position, constants.ATLAS_ZONE)
        flags = FlagCycle()
        return flags.get_flag()

    def construct_flag(self, flag):
        pass

    def move_to(actual_position, target_position):
        pathFinder = pathFinding()
        path = pathFinder.process_path_to(actual_position, target_position)