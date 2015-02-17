import sys
import numpy as np
import math
import cv2
import time


class Camera():

    def __init__(self):

        self.capt_obj = cv2.VideoCapture(0)
        flags, img = self.capt_obj.read()
        if flags == False:
            print >> sys.stderr, "Error with the capture of video"
            return None
        time.sleep(1)


    def grab_new_image(self):
        self.capt_obj.grab()

