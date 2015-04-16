from kinect import Kinect, NoKinectDetectedException
import cv2
import numpy as np
from cube import Cube, WhiteCube, BlackCube, FormFilter, FormStencil, TABLE_STENCIL, ColorFilter, RANGES_FOR_COLOR_FILTER,PARAMETERS_FOR_FORM_FILTER
from visiontools import VisionTools
import time, datetime
import math
from tests.test_vision_kinect import FakeKinect
from baseStation.cubeFinder import TABLE_FLAG_STENCIL
import robotLocator


def mouse_click_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print "Click at %d, %d" % (x, y)
        print param[x, y]

def save_kinect_capture(kinect, file_name, img_rgb=None):
    map = kinect.get_img_cloud_map()
    np.save(file_name + '.npy', map)
    if img_rgb is None:
        img_rgb = kinect.grab_new_image()
    cv2.imwrite(file_name + '.png', img_rgb)

if __name__ == "__main__":
    visionReady = True
    vision = VisionTools()
    cv2.namedWindow('BGR1', cv2.WINDOW_AUTOSIZE)
    # cv2.namedWindow('BGR2', cv2.WINDOW_AUTOSIZE)
    # cv2.namedWindow('mask1', cv2.WINDOW_AUTOSIZE)
    # cv2.namedWindow('mask2', cv2.WINDOW_AUTOSIZE)
    # cv2.setMouseCallback('red_layer', mouse_click_callback, image_hsv2)
    try:
        ma_kinect = Kinect('4')
        # ma_kinect = FakeKinect()
    except NoKinectDetectedException:
        print "No kinect detected"
        visionReady = False

    blackCube = BlackCube()
    robot_locator = robotLocator.RobotLocator()
    image_number = 0
    while visionReady:
        # image_rgb1 = cv2.imread('rgb_robot1.png')
        # image_rgb2 = cv2.imread('rgb_robot2.png')
        a = datetime.datetime.now()
        image_rgb1 = ma_kinect.grab_new_image(bilateral_filter_activated=True)
        b = datetime.datetime.now()
        c=b-a
        print 't-> ' + str(c.seconds) + '.' + str(c.microseconds)
        # image_mask2 = image_rgb1
        image_hsv1 = cv2.cvtColor(image_rgb1, cv2.COLOR_BGR2HSV)
        image_hsv2 = cv2.cvtColor(image_rgb1, cv2.COLOR_BGR2HSV)

        # print '***'
        # a = datetime.datetime.now()
        # robot_position = robot_locator.get_position(ma_kinect)
        # b = datetime.datetime.now()
        # c=b-a
        # print 't-> ' + str(c.seconds) + '.' + str(c.microseconds)
        # print robot_position.get_angle_in_deg()
        # print robot_position.position
        # print '***'
        # formFilter = FormStencil(TABLE_STENCIL.get('4'))
        # image_mask2 = formFilter.apply(image_mask2)
        # greenCorner = Cube('forest_green')
        # orange_corner = Cube('orange')
        # image_mask1 = orange_corner.apply_filters(image_hsv1, ma_kinect)
        # green_corner = Cube('purple')
        # image_mask2 = green_corner.apply_filters(image_hsv1, ma_kinect)
        # purple_corner = Cube('forest_green')
        # image_mask3 = purple_corner.apply_filters(image_hsv1, ma_kinect)

        image_mask3 = WhiteCube().apply_filters(image_hsv1)
        cv2.imshow('BGR1', image_rgb1)
        # cv2.imshow('BGR2', image_rgb2)
        # cv2.imshow('orange', image_mask1)
        # cv2.imshow('purple', image_mask2)
        cv2.imshow('white', image_mask3)
        # cv2.imshow('fuck', robot_locator.get_rgb_calibration(image_hsv2))

        time.sleep(0.3)
        key = cv2.waitKey(5) & 0xFF
        if key == 99:  # 'c'
            print 'image saved-> '+str(image_number)
            save_kinect_capture(ma_kinect, 'img'+str(image_number))
            image_number += 1
        elif key == 27:
            break

    cv2.destroyAllWindows()