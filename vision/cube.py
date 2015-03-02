import cv2
import numpy as np

RANGES_FOR_COLOR_FILTER = {'red': ([170, 80, 80], [179, 255, 255]),
                           'green': ([30, 110, 110], [50, 255, 255]),
                           'blue': ([95, 80, 80], [115, 255, 255]),
                           'yellow': ([22, 130, 130], [32, 255, 255])}

PARAMETERS_FOR_FORM_FILTER = {'red': ([8], [9]),
                              'green': ([5], [8]),
                              'blue': ([5], [8]),
                              'yellow': ([2], [4])}


class ColorFilter:
    def __init__(self, color_range):
        self.color_range = color_range

    def apply(self, img_hsv):
        lower_color = np.array(self.color_range[0])
        upper_color = np.array(self.color_range[1])
        img_mask = cv2.inRange(img_hsv, lower_color, upper_color)
        return img_mask


class FormFilter:
    def __init__(self, iteration_range):
        self.erode_iteration = np.array(iteration_range[0])
        self.dilate_iteration = np.array(iteration_range[1])

    def apply(self, img_mask):
        rect_size = 3
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (rect_size, rect_size))
        image_erode = cv2.erode(img_mask, kernel, iterations=self.erode_iteration)
        image_dilate = cv2.dilate(image_erode, kernel, iterations=self.dilate_iteration)
        return image_dilate


class Cube:
    def __init__(self, a_color):
        self.color = a_color
        self.position = None
        self.color_filter = ColorFilter(RANGES_FOR_COLOR_FILTER.get(a_color))
        self.form_filter = FormFilter(PARAMETERS_FOR_FORM_FILTER.get(a_color))  

    def apply_filters(self, img_hvg):
        img_mask = self.color_filter.apply(img_hvg)
        img_mask = self.form_filter.apply(img_mask)
        return img_mask

    def find_position(self, img_hvg, kinect):
        position_in_world = self._find_position_in_world(img_hvg, kinect)
        self.position = kinect._apply_matrix_transformation(position_in_world)
        return self.position

    def _find_position_in_world(self, img_hvg, kinect):
        img_mask = self.apply_filters(img_hvg)
        point_centre = kinect._get_centre_object(img_mask)
        pixel_cloud = kinect.get_img_cloud_map()
        point_world = pixel_cloud[point_centre[1], point_centre[0]]
        point1_ref = [[-point_world[0]], [point_world[2]], [1]]
        return np.mat(point1_ref)

