import os
import cv2
import numpy as np
import math
import time
from vision.cube import FormStencil


class NoCameraDetectedException(Exception):
    def __init__(self):
        pass


class Camera():

    def __init__(self):
        self.capt_obj = cv2.VideoCapture(0)
        flags, img = self.capt_obj.read()
        if flags is False:
            raise NoCameraDetectedException()

    def getCapt(self):
        self.capt_obj.grab()
        return self.capt_obj

    def apply_filter_color_cubes(self, img_rgb, cube):
        img = cv2.GaussianBlur(img_rgb, (3, 3), 10)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        img_binary = cube.color_filter.apply(img)
        dilation = np.ones((3, 3), "uint8")
        img_binary = cv2.dilate(img_binary, dilation)
        return img_binary

    def apply_filter_black_cube(self, img_rgb, cube):
        img_hsv = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2HSV)
        img_mask = cube.apply_filters(img_hsv)
        img_mask = self.apply_polyline([np.array([[460, 354], [502, 478], [449, 480], [441, 402]], np.int32)], img_mask)
        img_mask = self.apply_polyline([np.array([[0, 0], [640, 0], [640,130], [0, 130]], np.int32)], img_mask)
        img_mask = self.apply_polyline([np.array([[259, 334], [281, 348], [283,480], [198, 480]], np.int32)], img_mask)
        return img_mask

    def apply_polyline(self, polyline, image):
        stencil = FormStencil(polyline)
        mask = stencil.apply(image)
        return mask

    def find_contour_cube_black(self, image):
        contours, hierarchy = cv2.findContours(image,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        approx = None
        max_area = 0
        for i in contours:
            area = cv2.contourArea(i)
            if area > 5000 and area < 100000 :
                peri = cv2.arcLength(i,True)
                approx = cv2.approxPolyDP(i,0.02*peri,True)
                if area > max_area and len(approx)==4:
                    max_area = area
        return approx

    def find_largest_contour_color(self, img_binary):
        contours, hierarchy = cv2.findContours(img_binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        max_area = 0
        largest_contour = None
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > max_area:
                max_area = area
                largest_contour = contour
        return largest_contour