import cv2
import numpy as np

RANGES_FOR_COLOR_FILTER = {'red': [([169, 73, 92], [179, 255, 255]), ([0, 73, 92], [2, 255, 255])],
                           'green': [([30, 110, 110], [50, 255, 255])],
                           'blue': [([95, 80, 80], [115, 255, 255])],
                           'yellow': [([22, 130, 130], [32, 255, 255])]}

PARAMETERS_FOR_FORM_FILTER = {'red': ([2], [9]),
                              'green': ([5], [8]),
                              'blue': ([5], [8]),
                              'yellow': ([2], [4])}


class ColorFilter:
    def __init__(self, color_range):
        self.color_range = color_range

    def apply(self, img_hsv):
        img_mask = None
        for range in self.color_range:
            lower_color = np.array(range[0])
            upper_color = np.array(range[1])
            if img_mask is None:
                img_mask = cv2.inRange(img_hsv, lower_color, upper_color)
            else:
                img_mask += cv2.inRange(img_hsv, lower_color, upper_color)
        return img_mask

    def applyCamera(self, image):
        img = cv2.GaussianBlur(image, (5, 5), 0)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        for range in self.color_range:
            lower_blue = np.array(range[0], np.uint8)
            upper_blue = np.array(range[1], np.uint8)
            img_binary = cv2.inRange(img, lower_blue, upper_blue)
        return img_binary


class FormFilter:
    def __init__(self, iteration_range):
        self.erode_iteration = np.array(iteration_range[0])
        self.dilate_iteration = np.array(iteration_range[1])

    def apply(self, img_mask):
        rect_size = 3
        self._apply_stencil(img_mask)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (rect_size, rect_size))
        image_erode = cv2.erode(img_mask, kernel, iterations=self.erode_iteration)
        image_dilate = cv2.dilate(image_erode, kernel, iterations=self.dilate_iteration)
        return image_dilate

    def _apply_stencil(self, img_mask):
        poly_top = np.array([[0, 0], [640, 0], [640, 289], [607, 273], [607, 210], [0, 210]], np.int32)
        poly_top = poly_top.reshape((-1,1,2))
        poly_bottom = np.array([[0, 293], [640, 322], [640, 480], [0, 480]], np.int32)
        poly_bottom = poly_bottom.reshape((-1,1,2))
        cv2.fillPoly(img_mask, [poly_top, poly_bottom], (0, 0, 0))


class Cube:
    def __init__(self, a_color):
        self.color = a_color
        self.position = None
        self.color_filter = ColorFilter(RANGES_FOR_COLOR_FILTER.get(a_color))
        self.form_filter = FormFilter(PARAMETERS_FOR_FORM_FILTER.get(a_color))  

    def apply_filters(self, img_hsv):
        img_mask = self.color_filter.apply(img_hsv)
        img_mask = self.form_filter.apply(img_mask)
        return img_mask

    def find_position(self, img_hvg, kinect):
        position_in_world = self._find_position_in_world(img_hvg, kinect)
        position = kinect._apply_matrix_transformation(position_in_world)
        self.position = (int(position[0]*1000), int(position[1]*1000+40))
        return self.position

    def _find_position_in_world(self, img_hvg, kinect):
        img_mask = self.apply_filters(img_hvg)
        point_centre = kinect._get_centre_object(img_mask)
        pixel_cloud = kinect.get_img_cloud_map()
        point_world = pixel_cloud[point_centre[1], point_centre[0]]
        point1_ref = [[-point_world[0]], [point_world[2]], [1]]
        return np.mat(point1_ref)


class WhiteCube(Cube):
    def __init__(self):
        self.color = 'white'
        self.position = None
        self.color_filter = ColorFilter([([0, 0, 230], [180, 20, 255])])
        self.form_filter = FormFilter((5, 3))

    def apply_filters(self, img_hsv):
        img_mask = cv2.bilateralFilter(img_hsv, 20, 75, 75)
        img_mask = self.color_filter.apply(img_mask)
        img_mask = self.form_filter.apply(img_mask)
        return img_mask


class BlackCube(Cube):
    def __init__(self):
        self.color = "black"
        self.position = None



