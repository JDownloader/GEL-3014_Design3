import sys
import numpy as np
import math
import cv2
import time


RANGES = {'red': ([170, 80, 80], [180, 255, 255]),
          'green': ([30, 100, 100], [50, 255, 255]),
          'blue': ([90, 130, 150], [140, 255, 255]),
          'yellow': ([20, 60, 190], [30, 255, 255]),
          'white': ([0, 0, 0], [0, 0, 0]),
          'black':([90, 60, 30], [110, 255, 255])}


class Kinect():

    def __init__(self):
        self.angle = -22.75/180*math.pi
        # self.transX = 0.105
        # self.transZ = -0.535
        # self.angle = -0.6216
        self.transX = 0.1623
        self.transZ = -0.4582
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

    def apply_matrix_transformation(self, point_reference):
        trans_rot = [[math.cos(self.angle), -math.sin(self.angle), self.transX],
                    [math.sin(self.angle), math.cos(self.angle), self.transZ],
                    [0, 0 , 1]]

        matrix_transformation = np.dot(trans_rot, point_reference)

        return matrix_transformation


    def get_position_object(self, matrix):

        position_object = [matrix[0], matrix[1]]
        return position_object


    def get_centre_object(self, img_mask):
        moments = cv2.moments(img_mask)
        area = moments['m00']

        if(area < 2000000):

            #Centre de l'objet, x, y del objeto
            x = int(moments['m10']/moments['m00'])
            y = int(moments['m01']/moments['m00'])

        centre = (x, y)

        return centre
