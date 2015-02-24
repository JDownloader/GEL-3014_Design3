from kinect import Kinect, NoKinectDetectedException
import cv2
from cube import Cube
import math
from visiontools import VisionTools

def calculate_calibration_values(x1, x2, y1, y2):
    opposite_value_of_upper_triangle = math.fabs(x2 - y2)
    adjacent_value_of_upper_triangle = math.fabs(x2 - x1)
    print "opp" + str(opposite_value_of_upper_triangle) + "adj: " + str(adjacent_value_of_upper_triangle)
    angle_between_kinect_and_table =  (opposite_value_of_upper_triangle/float(adjacent_value_of_upper_triangle))

    hypotenuse_of_upper_triangle = math.sqrt(math.pow(x1, 2) + math.pow(x1 * math.sinh(angle_between_kinect_and_table), 2))
    print(hypotenuse_of_upper_triangle)
    opposite_value_of_lower_triangle = math.tan(angle_between_kinect_and_table) * (662 - hypotenuse_of_upper_triangle)
    adjacent_overlay = math.tan(angle_between_kinect_and_table) * float(opposite_value_of_lower_triangle - 225)
    distance_between_center_of_kinect_and_origin_of_table = 225 - adjacent_overlay
    print "angle:" + str(angle_between_kinect_and_table) + \
          " distance_x:" + str(distance_between_center_of_kinect_and_origin_of_table) + \
          " distance_z:" + str(y1 - hypotenuse_of_upper_triangle)

if __name__ == "__main__":
    # calculate_calibration_values(124.88, 414.59, 765.0, 1581.0)
    # calculate_calibration_values(124.88, 414.59, 775.0, 1591.0)
    # calculate_calibration_values(-150.0, 770.0, 330.0, 1000.0)
    visionReady = True
    vision = VisionTools()
    cv2.namedWindow('BGR', cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow('blue_layer', cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow('red_layer', cv2.WINDOW_AUTOSIZE)
    try:
        ma_kinect = Kinect()
    except NoKinectDetectedException as e:
        print "No kinect detected"
        visionReady = False

    while visionReady:
        ma_kinect.grab_new_image()
        image_rgb = vision.get_image_rgb(ma_kinect.capt_obj)
        image_hsv = vision.get_hsv_image(image_rgb)

        red_cube = Cube('red')
        blue_cube = Cube('blue')
        mask_red = red_cube.apply_filters(image_hsv)
        mask_blue = blue_cube.apply_filters(image_hsv)

        cv2.imshow('BGR', image_rgb)
        cv2.imshow('red_layer', mask_red)
        cv2.imshow('blue_layer', mask_blue)
        # cv2.imwrite('xxx_rgb.png', image_rgb)
        # cv2.imwrite('xxx_hsv.png', image_hsv)

        key = cv2.waitKey(5) & 0xFF
        if key == 27:
            break

    cv2.destroyAllWindows()

    position_blue = blue_cube._find_position_in_world(image_hsv, ma_kinect)

    # print pixel_cloud
    print "blue" + str(position_blue)

    position_red = red_cube._find_position_in_world(image_hsv, ma_kinect)


    # print pixel_cloud
    print "red" + str(position_red)
    blue_in_world = blue_cube._find_position_in_world(image_hsv, ma_kinect)
    red_in_world = red_cube._find_position_in_world(image_hsv, ma_kinect)
    print calculate_calibration_values(red_in_world[0], red_in_world[1], blue_in_world[0], blue_in_world[1])
