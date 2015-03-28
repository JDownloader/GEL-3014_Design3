import time
import random
from vision.kinect import Kinect, NoKinectDetectedException
from tests.test_vision import FakeKinect
from cubeFinder import CubeFinder, DemoCubeFinder
from time import gmtime, strftime
from flagLoop import FlagLoop
from controller.serialCom import Robot
from contextHelper import ContextHelper

class RunLoop:
    startTime = None;

    def __init__(self):
        self.flag_loop = FlagLoop()
        try:
            self.kinect = Kinect()
        except NoKinectDetectedException:
            self.kinect = FakeKinect()
        self.cube_finder = DemoCubeFinder(self.kinect)
        self.robot = Robot()

    def start(self):
        self.startTime = time.time()

    def get_time(self):
        if self.startTime is None:
            return 0
        return time.time()-self.startTime

    def get_context(self, robot_ip):
        context_helper = ContextHelper(self)
        self.cube_finder.refresh_position()
        return context_helper.get_context(robot_ip)