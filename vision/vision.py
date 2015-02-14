import sys
import time
import numpy as np
import cv2


class Vision:

    def __init__(self, a_cam_id):
        self.cam_id = a_cam_id

    def open_camera(self):
        cap = cv2.VideoCapture(self.cam_id)
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



    def mouse_click_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            print "Click at %d, %d" % (x, y)

    def new_rgb_image(self, width, height):
        image = np.zeros((height, width, 3), np.uint8)
        return image

    def get_hsv_image(self, image_rgb):
        hsv_image = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2HSV)
        return hsv_image

    def get_color_object(self, image, lower_color, upper_color):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv, lower_color, upper_color)

        imgGrey = mask
        ret, thresh = cv2.threshold(mask, 127, 255, cv2.cv.CV_THRESH_BINARY)


        kernel = cv2.getStructuringElement(cv2.MORPH_TOPHAT, (5, 5))
        # array([[0, 0, 1, 0, 0],
        # [0, 0, 1, 0, 0],
        # [1, 1, 1, 1, 1],
        # [0, 0, 1, 0, 0],
        # [0, 0, 1, 0, 0]], dtype=uint8)


        image_erode = cv2.erode(thresh, kernel, iterations=2)
        image_dilate = cv2.dilate(image_erode, kernel, iterations=2)

        #kernel = np.ones((5,5),np.uint8)
        #erosion = cv2.erode(img,kernel,iterations = 1)
        #opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)


        # contours, hierarchy = cv2.findContours(image_erode, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)
        #
        #
        # result_image = self.new_rgb_image(thresh.shape[1], thresh.shape[0])
        # #result_image = self.new_rgb_image(thresh.shape[1], thresh.shape[0])
        # cv2.drawContours(result_image, contours, -1, (100, 250, 0), 2)

        return thresh





