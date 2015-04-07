from kinect import Kinect, NoKinectDetectedException
import cv2
import numpy as np
from cube import Cube, WhiteCube, BlackCube, FormFilter, FormStencil, TABLE_STENCIL, ColorFilter, RANGES_FOR_COLOR_FILTER,PARAMETERS_FOR_FORM_FILTER
from visiontools import VisionTools
import time, datetime
import math
from tests.test_vision_kinect import FakeKinect
import robotLocator


def mouse_click_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print "Click at %d, %d" % (x, y)
        print param[x, y]


if __name__ == "__main__":
    visionReady = True
    vision = VisionTools()
    cv2.namedWindow('BGR1', cv2.WINDOW_AUTOSIZE)
    # cv2.namedWindow('BGR2', cv2.WINDOW_AUTOSIZE)
    # cv2.namedWindow('mask1', cv2.WINDOW_AUTOSIZE)
    # cv2.namedWindow('mask2', cv2.WINDOW_AUTOSIZE)
    # cv2.setMouseCallback('red_layer', mouse_click_callback, image_hsv2)
    try:
        ma_kinect = Kinect('3')
        # ma_kinect = FakeKinect()
    except NoKinectDetectedException:
        print "No kinect detected"
        visionReady = False

    blackCube = BlackCube()
    robot_locator = robotLocator.RobotLocator()

    while visionReady:
        # image_rgb1 = cv2.imread('rgb_robot1.png')
        # image_rgb2 = cv2.imread('rgb_robot2.png')
        image_rgb1 = ma_kinect.grab_new_image(bilateral_filter_activated=True)
        # image_mask2 = image_rgb1
        image_hsv1 = cv2.cvtColor(image_rgb1, cv2.COLOR_BGR2HSV)
        image_hsv2 = cv2.cvtColor(image_rgb1, cv2.COLOR_BGR2HSV)

        print '***'
        robot_position = robot_locator.get_position(ma_kinect)
        print robot_position.get_angle_in_deg()
        print robot_position.position
        print '***'
        # formFilter = FormStencil(TABLE_STENCIL.get('4'))
        # image_mask2 = formFilter.apply(image_mask2)
        # greenCorner = Cube('forest_green')
        # orange_corner = Cube('orange')
        # image_mask1 = orange_corner.apply_filters(image_hsv1, ma_kinect)
        # green_corner = Cube('purple')
        # image_mask2 = green_corner.apply_filters(image_hsv1, ma_kinect)
        # purple_corner = Cube('forest_green')
        # image_mask3 = purple_corner.apply_filters(image_hsv1, ma_kinect)

        image_mask3 = WhiteCube().apply_filters(image_hsv1, ma_kinect)
        cv2.imshow('BGR1', image_rgb1)
        # cv2.imshow('BGR2', image_rgb2)
        # cv2.imshow('orange', image_mask1)
        # cv2.imshow('purple', image_mask2)
        cv2.imshow('white', image_mask3)
        # cv2.imshow('fuck', robot_locator.get_rgb_calibration(image_hsv2))

        time.sleep(0.3)
        key = cv2.waitKey(5) & 0xFF
        if key == 27:
            cv2.imwrite('rgb_robot_green.png', image_rgb1)
            break
        # break

    cv2.destroyAllWindows()
    # cv2.imwrite('4_different_cubes.png', image_rgb)
    # position_blue = blue_cube.find_position(image_hsv, ma_kinect)
    #
    # # print pixel_cloud
    # print "blue" + str(position_blue)
    #
    # position_red = red_cube.find_position(image_hsv, ma_kinect)
    #
    #
    # # print pixel_cloud
    # print "red" + str(position_red)
    # blue_in_world = blue_cube.find_position(image_hsv, ma_kinect)
    # red_in_world = red_cube.find_position(image_hsv, ma_kinect)
    #
    #
    # list = ma_kinect.get_img_cloud_map()
    # np.save('rgb_robot_green4.npy', list)