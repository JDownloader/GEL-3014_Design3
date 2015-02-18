import sys
import time
import numpy as np
import cv2


class VisionTools:

    def __init__(self):
        pass

    def open_camera(self, a_cam_id):
        cap = cv2.VideoCapture(a_cam_id)
        return cap

        #Obtention de la capture de l'image
    def get_frame(self, cap):
        ret, image = cap.read()
        if ret == False:
            print >> sys.stderr, "Error with the capture of video"
            return None
        return image

    def get_image_rgb(self, cap):
        flags, img = cap.retrieve(None, cv2.cv.CV_CAP_OPENNI_BGR_IMAGE)
        if not flags:
            print >> sys.stderr, "Error with RGB image"
            return None
        return img


    def new_rgb_image(self, width, height):
        image = np.zeros((height, width, 3), np.uint8)
        return image

    def get_hsv_image(self, image_rgb):
        hsv_image = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2HSV)
        return hsv_image

    def get_mask(self, image_hsv, lower_color, upper_color):
        mask = cv2.inRange(image_hsv, lower_color, upper_color)
        return mask


    def find_contours(self, img):
        contours, hierarchy = cv2.findContours(img, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)
        return contours

    def mouse_click_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            print "Click at %d, %d" % (x, y)

    def get_color_object_bleu(self, mask):
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        image_erode = cv2.erode(mask, kernel, iterations=2)
        image_dilate = cv2.dilate(image_erode, kernel, iterations=6)

        return image_dilate





    def get_color_object_red(self, image_rgb, lower_color, upper_color):
        image_hsv = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(image_hsv, lower_color, upper_color)

        kernelErode = cv2.getStructuringElement(cv2.MORPH_ERODE, (3, 3))
        kernelDilate = cv2.getStructuringElement(cv2.MORPH_DILATE, (3, 3))

        image_erode = cv2.erode(mask, kernelErode, iterations=2)
        image_dilate = cv2.dilate(mask, kernelDilate, iterations=2)

        return image_dilate


    def get_color_object_green(self, image_rgb, lower_color, upper_color):
        image_hsv = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(image_hsv, lower_color, upper_color)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        image_erode = cv2.erode(mask, kernel, iterations=2)
        image_dilate = cv2.dilate(mask, kernel, iterations=2)

        return image_dilate








