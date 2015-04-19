from os import path
import cv2
import numpy as np
from unittest import TestCase
from vision.cube import Cube
from vision.kinect import Kinect
from vision.distanceCalibration import DistanceCalibration
from vision.visiontools import VisionTools

here = path.abspath(path.dirname(__file__))


class FakeKinect(Kinect):
    def __init__(self):
        self.table = '1'
        self.distanceCalibration = DistanceCalibration(self.table)
        self.cloud_map = np.load(here + '/kinect_cloud_map.npy')
        self.img = self.img = cv2.imread(here + '/4_different_cubes.png')

    def get_img_cloud_map(self):
        return self.cloud_map

    def grab_new_image(self, bilateral_filter_activated=False, median_filter_activated=False):
        return self.img


class TestSimple(TestCase):
    ALLOWED_IMPRECISION = 80

    def setUp(self):
        self.fake_kinect = FakeKinect()
        self.img_hsv = VisionTools().get_hsv_image(self.fake_kinect.grab_new_image())
        self.red_cube = Cube('red')
        self.blue_cube = Cube('blue')
        self.yellow_cube = Cube('yellow')
        self.green_cube = Cube('green')

    def test_detect_red_cube(self):
        position_actual = self.red_cube.find_position(self.img_hsv, self.fake_kinect)
        position_desired = (840, 240)
        assert abs(position_actual[0] - position_desired[0]) < self.ALLOWED_IMPRECISION
        assert abs(position_actual[1] - position_desired[1]) < self.ALLOWED_IMPRECISION

    def test_detect_blue_cube(self):
        position_actual = self.blue_cube.find_position(self.img_hsv, self.fake_kinect)
        position_desired = (240, 240)
        assert abs(position_actual[0] - position_desired[0]) < self.ALLOWED_IMPRECISION
        assert abs(position_actual[1] - position_desired[1]) < self.ALLOWED_IMPRECISION

    def test_detect_yellow_cube(self):
        position_actual = self.yellow_cube.find_position(self.img_hsv, self.fake_kinect)
        position_desired = (240, 810)
        assert abs(position_actual[0] - position_desired[0]) < self.ALLOWED_IMPRECISION
        assert abs(position_actual[1] - position_desired[1]) < self.ALLOWED_IMPRECISION

    def test_detect_green_cube(self):
        position_actual = self.green_cube.find_position(self.img_hsv, self.fake_kinect)
        position_desired = (840, 810)
        assert abs(position_actual[0] - position_desired[0]) < self.ALLOWED_IMPRECISION
        assert abs(position_actual[1] - position_desired[1]) < self.ALLOWED_IMPRECISION