import cv2
import numpy as np

RANGES_FOR_COLOR_FILTER = {'red': [([169, 73, 92], [179, 255, 255]), ([0, 73, 92], [2, 255, 255])],
                           'green': [([30, 110, 110], [50, 255, 255])],
                           'blue': [([95, 80, 80], [115, 255, 255])],
                           'yellow': [([22, 130, 130], [32, 255, 255])]}

PARAMETERS_FOR_FORM_FILTER = {'red': [2, 9, 3],
                              'green': [5, 8, 3],
                              'blue': [5, 8, 3],
                              'yellow': [2, 4, 3]}


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


class FormFilter:
    def __init__(self, iteration_range):
        self.erode_iteration = np.array(iteration_range[0])
        self.dilate_iteration = np.array(iteration_range[1])
        self.rectangle_size = iteration_range[2]

    def apply(self, img_mask):
        self._apply_stencil(img_mask)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (self.rectangle_size, self.rectangle_size))
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
        self.white_filter = ColorFilter([([0, 0, 200], [180, 27, 255])])
        self.black_filter = ColorFilter([([0, 0, 0], [180, 256, 170])])
        self.form_filter = FormFilter([4, 4, 2])
        self.black_form_filter = FormFilter([0, 5, 3])

    def apply_filters(self, img_hsv):
        img_mask = cv2.bilateralFilter(img_hsv, 20, 75, 75)
        img_mask_white = self.white_filter.apply(img_mask)
        img_mask_black = self.black_filter.apply(img_mask)
        img_mask_black = self.black_form_filter.apply(img_mask_black)
        img_mask = self.filter_white_cube(img_mask_white, img_mask_black)
        img_mask = cv2.cvtColor(img_mask, cv2.COLOR_BGR2GRAY)
        img_mask = self.form_filter.apply(img_mask)
        return img_mask

    def filter_white_cube(self, mask_white, mask_black):
        b_and_w_junction = np.zeros((mask_white.shape[0], mask_white.shape[1], 3), np.uint8)
        for i in range(0, b_and_w_junction.shape[0]):
            for j in range(0, b_and_w_junction.shape[1] - 1):
                # b_and_w_junction[i, j][0] = mask_white[i, j]
                # b_and_w_junction[i, j][2] = mask_black[i, j]
                if mask_black[i, j] and mask_white[i, j]:
                    draw_line = False
                    for x in range(min(b_and_w_junction.shape[1], j + 50) - 1, j, -1):
                        if mask_black[i, x] and mask_white[i, x]:
                            draw_line = True
                        if draw_line and mask_white[i, x]:
                            b_and_w_junction[i, x][1] = 255
        return b_and_w_junction


class BlackCube(Cube):
    def __init__(self):
        self.color = 'black'
        self.position = None
        self.color_filter = ColorFilter([([0, 0, 0], [180, 256, 170])])
        self.form_filter = FormFilter([0, 5, 3])

    def apply_filters(self, img_hsv):
        img_mask = cv2.bilateralFilter(img_hsv, 20, 75, 75)
        img_mask = self.color_filter.apply(img_mask)
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
        # img_mask = cv2.erode(img_mask, kernel, iterations=1)
        img_mask = self.form_filter.apply(img_mask)
        return img_mask

