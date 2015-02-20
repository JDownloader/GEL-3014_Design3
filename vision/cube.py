import cv2
import numpy as np

RANGES_FOR_COLOR_FILTER = {'red': ([165, 80, 80], [175, 255, 255]),
          'green': ([30, 100, 100], [50, 255, 255]),
          'blue': ([100, 80, 80], [115, 255, 255]),
          'yellow': ([20, 60, 190], [30, 255, 255]),
          'white': ([0, 0, 0], [0, 0, 0]),
          'black':([90, 60, 30], [110, 255, 255])}


class ColorFilter:
    def __init__(self, color_range):
        self.color_range = color_range

    def apply(self, img_hsv):
        lower_color = np.array(self.color_range[0])
        upper_color = np.array(self.color_range[1])
        img_mask = cv2.inRange(img_hsv, lower_color, upper_color)
        return img_mask

class FormFilter:
    def __init__(self, ellipse_size=3, erode_iteration=2, dilate_iteration=6):
        self.ellipse_size = ellipse_size
        self.erode_iteration = erode_iteration
        self.dilate_iteration = dilate_iteration

    def apply(self, img_mask):
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (self.ellipse_size, self.ellipse_size))
        image_erode = cv2.erode(img_mask, kernel, iterations=self.erode_iteration)
        image_dilate = cv2.dilate(image_erode, kernel, iterations=self.dilate_iteration)
        return image_dilate


class Cube:
    def __init__(self, a_color):
        self.color = a_color
        self.position = None
        self.color_filter = ColorFilter(RANGES_FOR_COLOR_FILTER.get(a_color))
        self.form_filter = FormFilter()

    def apply_filters(self, img_hvg):
        img_mask = self.color_filter.apply(img_hvg)
        img_mask = self.form_filter.apply(img_mask)
        return img_mask

    def find_position(self, img_hvg):
        img_mask = self.apply_filters(img_hvg)