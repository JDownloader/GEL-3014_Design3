import time
from vision.kinect import Kinect, NoKinectDetectedException
from tests.test_vision import FakeKinect
from cubeFinder import CubeFinder, DemoCubeFinder
from PathFinding import PathFinding
from controller.serialCom import Robot
from contextHelper import ContextHelper
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

    def get_context(self, robot_ip):
        context_helper = ContextHelper(self)
        self.cube_finder.refresh_position()
        return context_helper.get_context(robot_ip)

    def fetch_answer(self):
        actual_position = ''
        self.move_to(actual_position, constants.ATLAS_ZONE)
        flags = FlagCycle()
        return flags.get_flag()

    def construct_flag(self, flag):
        pass

    def move_to(actual_position, target_position):
        pathFinder = PathFinding()
        path = pathFinder.process_path_to(actual_position, target_position)
