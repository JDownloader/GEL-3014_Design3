import time
from vision.kinect import Kinect, NoKinectDetectedException
from tests.test_vision_kinect import FakeKinect
from cubeFinder import CubeFinder, DemoCubeFinder
from contextProvider import ContextHelper
from flagProcessor import FlagProcessor
from baseStation.flagCycle import *
from baseStation.robotConnection import RobotConnection
import exceptions
import constants
from pathfinding.pathfinding import Pathfinding
from pathfinding.point import Point
import pathfinding.constants
from movementProcessor import MovementProcessor



class RunLoop:
    startTime = None;

    def __init__(self):
        self.flag_loop = FlagProcessor()
        self.pathfinder = Pathfinding()
        self.flag_cycle = FlagCycle
        self.movement_processor = None
        self.robot_position = Point(0, 0)
        try:
            self.kinect = Kinect('2')
        except NoKinectDetectedException:
            self.kinect = FakeKinect()
        self.cube_finder = DemoCubeFinder(self.kinect)

    def start(self, robot_connection):
        self.startTime = time.time()
        self.movement_processor = MovementProcessor(robot_connection)
        self.move_robot_to_atlas_zone()
        answer = self.fetch_answer()
        self.construct_flag(answer, robot_connection)

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
        self.move_robot_to_atlas_zone()
        return self.flag_loop.get_flag()

    def construct_flag(self, flag, robot_connection):
        flag_cycle = FlagCycle(flag, robot_connection)
        flag_cycle.start()

    def move_robot_to_atlas_zone(self):
        self.move_forward_robot_center_to_point(self.robot_position, pathfinding.constants.ATLAS_ZONE_COORDINATES)

    def move_forward_robot_center_to_point(self, actual_robot_center_position, target_position):
        path = self.pathfinder.pathfind_to_point(actual_robot_center_position, target_position)
        self.movement_processor.physical_movement_processor(path)