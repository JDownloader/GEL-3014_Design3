import cv2
# from angletest2 import green_corner
from cube import Cube, FormStencil, FormFilter
from kinect import Kinect
from visiontools import VisionTools
import numpy as np
import math


class RobotLocator():
    PIXEL_SHIFT = 3
    def __init__(self):
        self.position = RobotPosition()

    def get_position(self, kinect):
        self.position = RobotPosition()
        for x in range(0, 5):
            position = self.attempt_get_position(kinect)
            if position.is_valid():
                for y in range(0, 3):
                    second_position = self.attempt_get_position(kinect)
                    if second_position.is_valid() and second_position.is_like(position):
                        self.position = self.merge_position(position, second_position)
                        return self.position
        self.position = RobotPosition()
        return self.position

    def merge_position(self, position_1, position_2):
        pos_x = int((position_1.position[0]+position_2.position[1])/2)
        pos_y = int((position_1.position[0]+position_2.position[1])/2)
        angle = float((position_1.angle+position_2.angle)/float(2))
        return RobotPosition(pos_x, pos_y, angle)

    def attempt_get_position(self, kinect):
        new_position = None
        img_hsv = self.get_masked_hsv(kinect)
        purple_corner = Cube('purple')
        green_corner = Cube('forest_green')
        purple_position = purple_corner.find_position(img_hsv, kinect)
        green_position = green_corner.find_position(img_hsv, kinect)
        if purple_corner.is_valid_position(purple_position):
            new_position = self.test_other_corners(img_hsv, kinect, purple_corner, 0)
        elif green_corner.is_valid_position(green_position):
            new_position = self.test_other_corners(img_hsv, kinect, green_corner, math.pi / 2)
        return new_position

    def get_masked_hsv(self, kinect):
        img = kinect.grab_new_image(bilateral_filter_activated=True)
        img_hsv = VisionTools().get_hsv_image(img)
        polyline = np.array([[0, 280], [640, 280], [640, 480], [0, 480]], np.int32)
        stencil = FormStencil([polyline])
        return stencil.apply(img_hsv)

    def test_other_corners(self, img_hsv, kinect, found_corner, angle_modificator=0):
        new_position = RobotPosition()
        found_corner_x_position = found_corner._find_center_in_img(img_hsv, kinect)[0]
        if angle_modificator == 0:
            maybe_first_corner_position = self.find_left_orange_corner(img_hsv, kinect, found_corner_x_position)
            maybe_second_corner_position = self.find_right_orange_corner(img_hsv, kinect, found_corner_x_position)
        else:
            maybe_first_corner_position = self.find_right_orange_corner(img_hsv, kinect, found_corner_x_position)
            maybe_second_corner_position = self.find_left_orange_corner(img_hsv, kinect, found_corner_x_position)

        if self.position.is_valid_position(maybe_first_corner_position):#  TODO
            if angle_modificator == 0:
                found_corner.find_position(img_hsv, kinect, self.PIXEL_SHIFT)
                new_position.set_from_points(maybe_first_corner_position, found_corner.position, 0)
                # print 'purple first'
            else:
                new_position.set_from_points(maybe_first_corner_position, found_corner.position, math.pi/2)
                found_corner.find_position(img_hsv, kinect, -self.PIXEL_SHIFT)
                # print 'green first'
        elif self.position.is_valid_position(maybe_second_corner_position):#  TODO
            if angle_modificator == 0:
                found_corner.find_position(img_hsv, kinect, -self.PIXEL_SHIFT)
                new_position.set_from_points(maybe_second_corner_position, found_corner.position, math.pi*3/2)
                # print 'purple second'
            else:
                found_corner.find_position(img_hsv, kinect, self.PIXEL_SHIFT)
                new_position.set_from_points(maybe_second_corner_position, found_corner.position, math.pi)
                # print 'green second'
        return new_position

    def find_left_orange_corner(self,img_hsv, kinect, x_limit):
        polyline = np.array([[0, 0], [x_limit, 0], [x_limit, 480], [0, 480]], np.int32)
        return self.find_orange_corner(img_hsv, kinect, polyline, True)

    def find_right_orange_corner(self, img_hsv, kinect, x_limit):
        polyline = np.array([[x_limit, 0], [640, 0], [640, 480], [x_limit, 480]], np.int32)
        return self.find_orange_corner(img_hsv, kinect, polyline, False)

    def find_orange_corner(self, img_hsv, kinect, polyline, is_left):
        stencil = FormStencil([polyline])
        img_hsv_mask = stencil.apply(img_hsv)
        orange_corner = Cube('orange')
        if is_left:
            return orange_corner.find_position(img_hsv_mask, kinect, self.PIXEL_SHIFT)
        return orange_corner.find_position(img_hsv_mask, kinect, -self.PIXEL_SHIFT)

    def get_rgb_calibration(self, img_hsv, form_filter=True):
        rgb_result = np.zeros((img_hsv.shape[0], img_hsv.shape[1], 3), np.uint8)
        orange_cube = Cube('orange')
        green_cube = Cube('forest_green')
        purple_cube = Cube('purple')
        if form_filter == False:
            orange_cube.form_filter = FormFilter([0, 0, 1, 1])
            green_cube.form_filter = FormFilter([0, 0, 1, 1])
            purple_cube.form_filter = FormFilter([0, 0, 1, 1])
        orange_filter = orange_cube.apply_filters(img_hsv)
        green_filter = green_cube.apply_filters(img_hsv)
        purple_filter = purple_cube.apply_filters(img_hsv)
        for i in range(180, rgb_result.shape[0]-205):
            for j in range(0, rgb_result.shape[1]):
                rgb_result[i, j][1] += int(orange_filter[i, j] * 0.5)
                rgb_result[i, j][2] += orange_filter[i, j]
                rgb_result[i, j][0] += int(purple_filter[i, j] * 0.5)
                rgb_result[i, j][2] += int(purple_filter[i, j] * 0.5)
                rgb_result[i, j][1] += int(green_filter[i, j] * 0.25)
        return rgb_result



class Position():
    NEGATIVE_POSITION_TOLERANCE_IN_MM = -100
    NO_POSITION_TOLERANCE = 4

    def __init__(self, x=None, y=None, angle=None):
        self.position = (x, y)
        self.angle = angle

    def set_angle_from_points(self, point_1, point_2):
        delta_x = point_1[1] - point_2[1]
        delta_y = point_1[0] - point_2[0]
        self.angle = math.atan2(delta_y, delta_x)

    def set_position(self, x, y):
        self.position = (x, y)

    def get_angle_in_deg(self):
        if self.angle is None:
            return None
        return self.angle * 180 / math.pi

    def is_valid(self):
        return self.is_valid_position(self.position)

    def is_valid_position(self, position):
        if position is None:
            return False
        if position[0] is None or position[1] is None:
            return False
        if position[0] > self.NEGATIVE_POSITION_TOLERANCE_IN_MM \
                and position[1] > self.NEGATIVE_POSITION_TOLERANCE_IN_MM \
                and position[0] < 1220 \
                and position[1] < 2450:
            return True
        return False

    def normalize_angle(self):
        if self.angle < -math.pi:
            self.angle += 2 * math.pi
        elif self.angle > math.pi:
            self.angle -= 2 * math.pi


class RobotPosition(Position):
    ROBOT_DIMENSION = 220
    ANGLE_TOLERANCE = math.radians(5)
    DISTANCE_TOLERANCE = 50

    def __init__(self, x=None, y=None, angle=None):
        Position.__init__(self, x, y, angle)

    def set_from_points(self, point_1, point_2, angle_modificator):
        self.set_angle_from_points(point_1, point_2)
        self.angle += angle_modificator
        diagonal = math.sqrt(2) * self.ROBOT_DIMENSION / 2
        if angle_modificator < math.pi:
            x_value = point_1[0] + diagonal * math.cos(self.angle + math.pi/float(4))
            y_value = point_1[1] - diagonal * math.sin(self.angle + math.pi/float(4))
        else:

            x_value = point_1[0] - diagonal * math.cos(self.angle + math.pi/float(4))
            y_value = point_1[1] + diagonal * math.sin(self.angle + math.pi/float(4))
        self.position = (x_value, y_value)
        self.normalize_angle()

    def update_with_pathfinding_tuple(self, pathfinding_tuple):
        self.angle += pathfinding_tuple[0]
        self.position = (self.position[0] + math.sin(math.radians(self.angle)) * pathfinding_tuple[1],
                             self.position[1] + math.cos(math.radians(self.angle)) * pathfinding_tuple[1])

        self.normalize_angle()

    def update_with_kinect(self, kinect_position, kinect_angle):
        temp_pos = Position(kinect_position[0], kinect_position[1], math.radians(kinect_angle))
        temp_pos.normalize_angle()
        if temp_pos.is_valid():
            self.angle = math.degrees(temp_pos.angle)
            self.position = temp_pos.position
            return True
        else:
            return False

    def is_like(self, other_position):
        if abs(self.angle-other_position.angle) < self.ANGLE_TOLERANCE and \
                        abs(self.position[0]-other_position.position[0]) < self.DISTANCE_TOLERANCE and \
                        abs(self.position[1]-other_position.position[1]) < self.DISTANCE_TOLERANCE:
            return True
        return False