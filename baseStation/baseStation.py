from vision.kinect import Kinect, NoKinectDetectedException
from tests.test_vision_kinect import FakeKinect
from cubeFinder import DemoCubeFinder
from flag import Flag


class BaseStation():
    def __init__(self):
        try:
            self.kinect = Kinect('4')
        except NoKinectDetectedException:
            self.kinect = FakeKinect()
        self.cube_finder = DemoCubeFinder(self.kinect)
        self.flag = Flag('Canada')
        self.question = ''
        self.answer = ''

    def change_question(self, question, answer):
        self.question = question
        self.answer = answer