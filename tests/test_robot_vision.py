from os import path
import cv2
#import numpy as np
from unittest import TestCase
from robotVision.visionRobot import VisionRobot
from robotVision.camera import Camera
from mock import Mock
#import math

here = path.abspath(path.dirname(__file__))

class FakeCamera(Camera):
    def __init__(self):
        self.capt_obj = cv2.VideoCapture(0)

class TestRobotVision(TestCase):

    def setUp(self):
        self.image = cv2.imread(here+'/yellow_cube.png')
        self.camera = FakeCamera()

    def get_contour(self, color):
        self.vision = VisionRobot(color, self.camera)
        contour = self.vision.find_contour_cube(self.image, self.vision.cube)
        return contour

    def test_set_cube_color(self):
        color = "red"
        vision = VisionRobot(color, self.camera)
        self.assertEqual(vision.cube.color, color)

    def test_set_white_cube(self):
        white_color = "white"
        vision = VisionRobot(white_color, self.camera)
        self.assertEqual(vision.cube.color, white_color)

    def test_find_contour_cube_empty(self):
        color = "blue"
        contour = self.get_contour(color)
        self.assertIsNone(contour)

    def test_find_contour_cube_no_empty(self):
        color = "yellow"
        contour = self.get_contour(color)
        self.assertIsNotNone(contour)

    def test_get_moment_when_contour_empty(self):
        color = "blue"
        contour = self.get_contour(color)
        moment = self.vision.get_moment(contour)
        self.assertIsNone(moment)

    def test_get_cube_center_delta(self):
        color = "red"
        contour = self.get_contour(color)
        moment = self.vision.get_moment(contour)
        delta = self.vision.find_cube_center_delta(self.image, moment)
        self.assertEqual(len(delta), 2)

    def test_get_white_cube_center_delta(self):
        color = "white"
        self.image = cv2.imread(here +'/white_cube.png')
        contour = self.get_contour(color)
        moment = self.vision.get_moment(contour)
        delta = self.vision.find_cube_center_delta(self.image, moment)
        self.assertEqual(len(delta), 2)



