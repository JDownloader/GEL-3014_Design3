from kinect import Kinect, RANGES
import numpy as np
import cv2
import time
import math
from visiontools import VisionTools

def calculate_calibration_values(x1, x2, y1, y2):
    opposite_value_of_upper_triangle = math.fabs(x2 - y2)
    adjacent_value_of_upper_triangle = math.fabs(x2 - x1)
    print "opp" + str(opposite_value_of_upper_triangle) + "adj: " + str(adjacent_value_of_upper_triangle)
    angle_between_kinect_and_table =  (opposite_value_of_upper_triangle/float(adjacent_value_of_upper_triangle))

    hypotenuse_of_upper_triangle = math.sqrt(math.pow(x1, 2) + math.pow(x2, 2))
    print(hypotenuse_of_upper_triangle)
    opposite_value_of_lower_triangle = math.tan(angle_between_kinect_and_table) * (662 - hypotenuse_of_upper_triangle)
    adjacent_overlay = math.tan(angle_between_kinect_and_table) * float(opposite_value_of_lower_triangle - 290)
    distance_between_center_of_kinect_and_origin_of_table = 294 - adjacent_overlay
    print "angle:" + str(angle_between_kinect_and_table) + \
          " distance_x:" + str(distance_between_center_of_kinect_and_origin_of_table) + \
          " distance_z:" + str(y1 - hypotenuse_of_upper_triangle)

if __name__ == "__main__":
    # calculate_calibration_values(124.88, 414.59, 765.0, 1581.0)
    # calculate_calibration_values(124.88, 414.59, 775.0, 1591.0)
    # calculate_calibration_values(-150.0, 770.0, 330.0, 1000.0)

    vision = VisionTools()
    cv2.namedWindow('BGR', cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow('blue_layer', cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow('red_layer', cv2.WINDOW_AUTOSIZE)
    ma_kinect = Kinect()

    while True:

        ma_kinect.grab_new_image()

        img_cloud_map = ma_kinect.get_img_cloud_map()

        image_rgb = vision.get_image_rgb(ma_kinect.capt_obj)

        color_range = RANGES.get('blue')

        lower_color = np.array(color_range[0])
        upper_color = np.array(color_range[1])

        image_hsv = vision.get_hsv_image(image_rgb)
        mask_blue = vision.get_mask(image_hsv, lower_color, upper_color)
        mask_blue = vision.get_color_object_bleu(mask_blue)




        color_range = RANGES.get('red')

        lower_color = np.array(color_range[0])
        upper_color = np.array(color_range[1])

        mask_red = vision.get_mask(image_hsv, lower_color, upper_color)
        mask_red = vision.get_color_object_bleu(mask_red)
        # cv2.fastNlMeansDenoisingColored(mask_red,mask_red)
        # img_seg = vision.get_color_object_bleu(mask_blue)

        cv2.imshow('BGR', image_rgb)
        cv2.imshow('red_layer', mask_red)
        cv2.imshow('blue_layer', mask_blue)
        cv2.imwrite('xxx_rgb.png', image_rgb)
        cv2.imwrite('xxx_hsv.png', image_hsv)

        key = cv2.waitKey(5) & 0xFF
        if key == 27:
            break

    cv2.destroyAllWindows()

    point_centre = ma_kinect._get_centre_object(mask_blue)

    pixel_cloud = img_cloud_map[point_centre[1], point_centre[0]]

    point1Ref = [[-pixel_cloud[0]], [pixel_cloud[2]], [1]]
    blue_in_world = np.mat(point1Ref)
    matrix = ma_kinect._apply_matrix_transformation(blue_in_world)

    # position_blue = ma_kinect.get_position_object(matrix)
    position_blue = blue_in_world

    # print pixel_cloud
    print "blue" + str(position_blue)

    point_centre = ma_kinect._get_centre_object(mask_red)

    pixel_cloud = img_cloud_map[point_centre[1], point_centre[0]]

    point1Ref = [[-pixel_cloud[0]], [pixel_cloud[2]], [1]]
    red_in_world = np.mat(point1Ref)
    matrix = ma_kinect._apply_matrix_transformation(red_in_world)


    # print pixel_cloud
    position_red = red_in_world
    print "red" + str(position_red)
    print calculate_calibration_values(position_red[0], position_red[1], blue_in_world[0], blue_in_world[1])

    position_red = matrix[0], matrix[1]
    print "red" + str(position_red)