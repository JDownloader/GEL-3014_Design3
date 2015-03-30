import cv2
from cube import Cube, FormStencil
from kinect import Kinect
from visiontools import VisionTools
import numpy as np
import math


class RobotLocator():
    def __init__(self):
        self.position = RobotPosition()

    def get_position(self, kinect):
        img = kinect.grab_new_image()
        img_hsv = VisionTools().get_hsv_image(img)
        purple_corner = Cube('purple')
        green_corner = Cube('forest_green')
        purple_position = purple_corner.find_position(img_hsv, kinect)
        green_position = green_corner.find_position(img_hsv, kinect)
        if purple_corner.is_valid_position(purple_position):
            self.test_other_corners(img_hsv, kinect, purple_corner)
        elif green_corner.is_valid_position(green_position):
            self.test_other_corners(img_hsv, kinect, green_corner)
        return self.position

    def test_other_corners(self, img_hsv, kinect, found_corner):
        found_corner_x_position = found_corner._find_center_in_img(img_hsv, kinect)[0]
        maybe_orange_position = self.find_orange_position(img_hsv, kinect, found_corner_x_position)
        if self.position.is_valid_position(maybe_orange_position):#  TODO
            self.position.set_from_points(maybe_orange_position, found_corner.position)

    def find_orange_position(self,img_hsv, kinect, found_corner_x_position):
        maybe_left_corner_position = self.find_left_orange_corner(img_hsv, kinect, found_corner_x_position)
        maybe_right_corner_position = self.find_right_orange_corner(img_hsv, kinect, found_corner_x_position)
        if self.position.is_valid_position(maybe_left_corner_position):#  TODO
            return maybe_left_corner_position
        elif self.position.is_valid_position(maybe_right_corner_position):#  TODO
            return maybe_right_corner_position
        return (-500, -500)

    def find_left_orange_corner(self,img_hsv, kinect, x_limit):
        polyline = np.array([[0, 0], [x_limit, 0], [x_limit, 480], [0, 480]], np.int32)
        return self.find_orange_corner(img_hsv, kinect, polyline)

    def find_right_orange_corner(self, img_hsv, kinect, x_limit):
        polyline = np.array([[x_limit, 0], [640, 0], [640, 480], [x_limit, 480]], np.int32)
        return self.find_orange_corner(img_hsv, kinect, polyline)

    def find_orange_corner(self, img_hsv, kinect, polyline):
        stencil = FormStencil([polyline])
        img_hsv_mask = stencil.apply(img_hsv)
        orange_corner = Cube('orange')
        return orange_corner.find_position(img_hsv_mask, kinect)


class Position():
    NEGATIVE_POSITION_TOLERANCE_IN_MM = -100
    NO_POSITION_TOLERANCE = 4

    def __init__(self, x=None, y=None, angle=None):
        self.position = (x,y)
        self.angle = angle

    def set_angle_from_points(self, point_1, point_2):
        delta_x = point_1[1] - point_2[1]
        delta_y = point_1[0] - point_2[0]
        self.angle = math.atan2(delta_y, delta_x)

    def get_angle_in_deg(self):
        if self.angle is None:
            return None
        return self.angle * 180 / math.pi

    def is_valid_position(self, position):
        if position is None:
            return False
        if position[0] is None or position[1] is None:
            return False
        return position[0] > self.NEGATIVE_POSITION_TOLERANCE_IN_MM \
            and position[1] > self.NEGATIVE_POSITION_TOLERANCE_IN_MM


class RobotPosition(Position):
    ROBOT_DIMENSION = 220

    def __init__(self):
        Position.__init__(self, x=None, y=None, angle=None)

    def set_from_points(self, point_1, point_2):
        self.set_angle_from_points(point_1, point_2)
        if point_1[0] > point_2[0]:
            self._set_from_points_ordered(point_1, point_2)
        else:
            self._set_from_points_ordered(point_2, point_1)

    def _set_from_points_ordered(self, point_1, point_2):
        x_value = point_1[0] - self.ROBOT_DIMENSION / 2 * abs(math.cos(self.angle))
        y_value = point_1[0] + self.ROBOT_DIMENSION / 2 * abs(math.cos(self.angle))
        self.position = (int(x_value), int(y_value))