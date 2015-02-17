import sys
import numpy as np
import math
import cv2
import time
from visiontools import VisionTools


RANGES = {'red': ([170, 80, 80], [180, 255, 255]),
          'green': ([30, 100, 100], [50, 255, 255]),
          'bleu': ([100, 160, 160], [130, 255, 255]),
          'yellow': ([20, 60, 190], [30, 255, 255]),
          'white': ([0, 0, 0], [0, 0, 0]),
          'black':([90, 60, 30], [110, 255, 255])}


class Kinect():

    def __init__(self):
        self.angle = -22.75*math.pi/180
        self.transX = 0.135
        self.transZ = -0.545
        self.capt_obj = cv2.VideoCapture(cv2.cv.CV_CAP_OPENNI)

        flags, img = self.capt_obj.read()
        if flags == False:
            print >> sys.stderr, "Error with the capture of video"
            return None

        time.sleep(1)


    def grab_new_image(self):
        self.capt_obj.grab()

    def get_img_cloud_map(self):
        flags_p, img_cloud_map = self.capt_obj.retrieve(None, cv2.cv.CV_CAP_OPENNI_POINT_CLOUD_MAP)
        return img_cloud_map

    def get_matriz_transformation(self, point_reference):
        trans_rot = [[math.cos(self.angle), -math.sin(self.angle), self.transX],
                    [math.sin(self.angle), math.cos(self.angle), self.transZ],
                    [0, 0 , 1]]

        matrix_transformation = np.dot(trans_rot, point_reference)

        return matrix_transformation


    def get_position_object(self, matrix):

        position_object = [matrix[0], matrix[1]]
        return position_object


    def get_centre_object(self, img_mask):
        moments = cv2.moments(mask)
        area = moments['m00']

        if(area < 2000000):

            #Centre de l'objet, x, y del objeto
            x = int(moments['m10']/moments['m00'])
            y = int(moments['m01']/moments['m00'])

        centre = tuple(x, y)

        return centre



if __name__ == "__main__":

    vision = VisionTools()
    cv2.namedWindow('BGR', cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow('profondeur', cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow('ouverture', cv2.WINDOW_AUTOSIZE)
    ma_kinect = Kinect()

    while True:

        ma_kinect.grab_new_image()
        img_cloud_map = ma_kinect.get_img_cloud_map()

        image_rgb = vision.get_image_rgb(ma_kinect.capt_obj)

        color = RANGES.get('bleu')

        lower_color = np.array(color[0])
        upper_color = np.array(color[1])

        image_hsv = vision.get_hsv_image(image_rgb)
        mask = vision.get_mask(image_hsv, lower_color, upper_color)
        img_seg = vision.get_color_object_bleu(mask)

        cv2.imshow('BGR', image_rgb)
        cv2.imshow('ouverture', image_hsv)


        key = cv2.waitKey(5) & 0xFF
        if key == 27:
            break

    cv2.destroyAllWindows()

    point_centre = ma_kinect.get_centre_object(mask)

    pixel_cloud = img_cloud_map[point_centre(1), point_centre(0)]

    point1Ref = [[-pixel_cloud[0]], [pixel_cloud[2]], [1]]
    pointMonde = np.mat(point1Ref)
    matrix = ma_kinect.get_matriz_transformation(pointMonde)

    position = ma_kinect.get_position_object(matrix)

    print pixel_cloud
    print pixel_cloud[0]
    print pixel_cloud[2]
    print position






