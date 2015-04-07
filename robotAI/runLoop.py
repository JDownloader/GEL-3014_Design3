from vision.kinect import Kinect, NoKinectDetectedException
from tests.test_vision_kinect import FakeKinect
from cubeFinder import DemoCubeFinder
from contextProvider import ContextHelper
from flagProcessor import FlagProcessor
from robotAI.flagConstructionCycle import *
from pathfinding.pathfinding import Pathfinding
import pathfinding.constants
from movementProcessor import MovementProcessor
from robotStatus import RobotStatus

class RunLoop:
    startTime = None

    def __init__(self):
        self.flag_loop = FlagProcessor()
        self.pathfinder = Pathfinding()
        self.flag_cycle = FlagConstructionCycle
        self.movement_processor = None
        self.robot_status = None
        try:
            self.kinect = Kinect('4')
        except NoKinectDetectedException:
            self.kinect = FakeKinect()
        self.cube_finder = DemoCubeFinder(self.kinect)

    def start(self, robot_connection):
        self.start_timer()
        self.robot_status = RobotStatus(robot_connection)
        while not self.robot_status.angle_and_position.is_valid():
            self.robot_status.update_position_with_kinect(self.kinect)
            self.robot_status.update_position_with_kinect(self.kinect)
        self.movement_processor = MovementProcessor(robot_connection)
        answer = self.fetch_answer()
        self.construct_flag(answer)

    def start_timer(self):
        self.startTime = time.time()

    def get_time(self):
        if self.startTime is None:
            return 0
        return time.time()-self.startTime

    def get_context(self, robot_ip):
        context_helper = ContextHelper(self)
        self.cube_finder.refresh_position()
        if self.robot_status is not None:
            self.robot_status.update_position_with_kinect(self.kinect)
        return context_helper.get_context(robot_ip)

    def fetch_answer(self):
        self.move_robot_to_atlas_zone()
        return self.flag_loop.get_flag()
    
    def construct_flag(self, flag):
        flag_cycle = FlagConstructionCycle(flag, self.robot_status, self.kinect)
        flag_cycle.flag_construction_sequence()

    def move_robot_to_atlas_zone(self):
        self.move_robot_forward_to_point(self.robot_status.position,
                                         pathfinding.constants.ATLAS_ZONE_COORDINATES)

    def move_robot_forward_to_point(self, actual_robot_position, target_position):
        path = self.pathfinder.find_path_to_point(actual_robot_position, target_position)
        self.movement_processor.move(path, self.robot_status.position)