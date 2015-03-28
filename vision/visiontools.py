import sys
import numpy as np
import cv2


class VisionTools:

    def __init__(self):
        pass

    def get_hsv_image(self, image_rgb):
        hsv_image = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2HSV)
        return hsv_image