import sys
import numpy as np
import cv2


class VisionTools:

    def __init__(self):
        pass

    def get_image_rgb(self, cap):
        flags, img = cap.retrieve(None, cv2.cv.CV_CAP_OPENNI_BGR_IMAGE)
        if not flags:
            print >> sys.stderr, "Error with RGB image"
            return None
        return img

    def get_hsv_image(self, image_rgb):
        hsv_image = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2HSV)
        return hsv_image

    def find_contours(self, img):
        contours, hierarchy = cv2.findContours(img, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)
        return contours

    def mouse_click_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            print "Click at %d, %d" % (x, y)
