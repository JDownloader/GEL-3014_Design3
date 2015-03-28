import cv2
from cube import Cube
from kinect import Kinect
from visiontools import VisionTools


class RobotLocator():
    def __init__(self):
        pass

    def get_position(self, kinect):
        img = kinect.grab_new_image()
        img_hsv = VisionTools.get_hsv_image(img)
        purple_corner = Cube('purple')
        green_corner = Cube('forest_green')
        purple_position = purple_corner.find_position(img_hsv, kinect)
        green_position = green_corner.find_position(img_hsv, kinect)
        if purple_corner.is_valid_position(purple_position):
            found_corner_x_position = purple_corner._find_center_in_img(img_hsv, kinect)[0]
            maybe_left_corner_position = self.find_left_orange_corner(kinect, found_corner_x_position)
            maybe_right_corner_position = self.find_right_orange_corner(kinect, found_corner_x_position)
        elif green_corner.is_valid_position(green_corner):
            found_corner_x_position = green_corner._find_center_in_img(img_hsv, kinect)[0]

    def find_left_orange_corner(self, kinect, x_limit):
        return (-500, -500)

    def find_right_orange_corner(self):
        return (-500, -500)


class Position():
    def __init__(self, x, y, angle):
        self.position = (x,y)
        self.angle = angle