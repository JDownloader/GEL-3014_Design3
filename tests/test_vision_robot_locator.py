from os import path
import cv2
import numpy as np
from unittest import TestCase
from vision.robotLocator import RobotLocator
from vision.kinect import Kinect
from vision.distanceCalibration import DistanceCalibration
import math

here = path.abspath(path.dirname(__file__))


class FakeKinect2(Kinect):
    def __init__(self, file_name):
        self.table = '2'
        self.distanceCalibration = DistanceCalibration(self.table)
        self.cloud_map = np.load(here+'/robot_locator/' + file_name + '.npy')
        self.img = self.img = cv2.imread(here+'/robot_locator/' + file_name + '.png')

    def get_img_cloud_map(self):
        return self.cloud_map

    def grab_new_image(self, bilateral_filter_activated=False, median_filter_activated=False):
        return self.img


class TestSimple(TestCase):
    ALLOWED_IMPRECISION = 80
    ALLOWED_ANGLE_IMPRECISION = math.radians(5)

    def setUp(self):
        self.robot_locator = RobotLocator()

    def test_detect_robot_0(self):
        position_desired = (350, 350)
        self.position_test(0, position_desired)

    def test_detect_robot_90(self):
        position_desired = (350, 350)
        self.position_test(90, position_desired)

    def test_detect_robot_180(self):
        position_desired = (350, 350)
        self.position_test(180, position_desired)

    def test_detect_robot_270(self):
        position_desired = (350, 350)
        self.position_test(270, position_desired)

    def test_detect_robot_45(self):
        position_desired = (400, 400)
        self.position_test(45, position_desired)

    def test_detect_robot_135(self):
        position_desired = (400, 400)
        self.position_test(135, position_desired)

    def test_detect_robot_225(self):
        position_desired = (400, 400)
        self.position_test(225, position_desired)

    def test_detect_robot_315(self):
        position_desired = (400, 400)
        self.position_test(315, position_desired)

    def position_test(self, angle, position_desired):
        kinect = FakeKinect2('img' + str(angle))
        position_actual = self.robot_locator.get_position(kinect)
        angle_desired = math.radians(angle)
        if angle_desired > math.pi:
            angle_desired -= 2 * math.pi
        assert abs(position_actual.position[0] - position_desired[0]) < self.ALLOWED_IMPRECISION
        assert abs(position_actual.position[1] - position_desired[1]) < self.ALLOWED_IMPRECISION
        assert abs(position_actual.angle - angle_desired) < self.ALLOWED_ANGLE_IMPRECISION