from kinect import Kinect, NoKinectDetectedException
import cv2
import numpy as np
from cube import Cube
from visiontools import VisionTools

if __name__ == "__main__":
    visionReady = True
    vision = VisionTools()
    cv2.namedWindow('BGR', cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow('blue_layer', cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow('red_layer', cv2.WINDOW_AUTOSIZE)
    try:
        ma_kinect = Kinect('2')
    except NoKinectDetectedException:
        print "No kinect detected"
        visionReady = False

    while visionReady:
        image_rgb = ma_kinect.grab_new_image()
        image_hsv = VisionTools().get_hsv_image(image_rgb)

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
            cv2.imwrite('xxx_rgb.png', image_rgb    )
            break

    cv2.destroyAllWindows()
    cv2.imwrite('4_different_cubes.png', image_rgb)
    position_blue = blue_cube.find_position(image_hsv, ma_kinect)

    # print pixel_cloud
    print "blue" + str(position_blue)

    position_red = red_cube.find_position(image_hsv, ma_kinect)


    # print pixel_cloud
    print "red" + str(position_red)
    blue_in_world = blue_cube.find_position(image_hsv, ma_kinect)
    red_in_world = red_cube.find_position(image_hsv, ma_kinect)


    # f = open("output.txt", "w")
    list = ma_kinect.get_img_cloud_map()
    # outfile = open('kinect_cloud_map.npy', 'w')
    np.save('kinect_cloud_map.npy', list)
    # outfile.close()
    # for e in list:
    #         f.write(list+'\n')


    # f.close()
