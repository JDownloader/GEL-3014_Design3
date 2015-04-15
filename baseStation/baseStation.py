from vision.kinect import Kinect, NoKinectDetectedException
from tests.test_vision_kinect import FakeKinect
from cubeFinder import DemoCubeFinder, CubeFinder
from vision.robotLocator import RobotPosition
from flag import Flag


class BaseStation():
    def __init__(self):
        try:
            self.kinect = Kinect('3')
        except NoKinectDetectedException:
            self.kinect = FakeKinect()
        self.cube_finder = CubeFinder(self.kinect)
        self.flag = None
        self.question = ''
        self.answer = ''
        self.robot_position = None

    def set_question(self, question, answer):
        self.question = question
        self.answer = answer
        self.flag = Flag(answer)

    def set_robot_position(self, x, y, angle):
        self.robot_position = RobotPosition(x, y, angle)
