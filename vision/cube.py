import cv2
import numpy as np
from robotLocator import Position

RANGES_FOR_COLOR_FILTER = {'red': [([169, 73, 92], [179, 255, 255]), ([0, 73, 92], [2, 255, 255])],
                           'green': [([30, 110, 110], [50, 255, 255])],
                           'blue': [([95, 80, 80], [115, 255, 255])],
                           'yellow': [([22, 130, 130], [32, 255, 255])],
                           'orange': [([7, 80, 60], [17, 255, 255])],
                           'purple': [([120, 60, 60], [130, 255, 255])],
                           'forest_green': [([53, 25, 40], [75, 255, 255])]}

PARAMETERS_FOR_FORM_FILTER = {'red': [2, 9, 3, 3],
                              'green': [5, 8, 3, 3],
                              'blue': [5, 8, 3, 3],
                              'yellow': [2, 4, 3, 3],
                              'orange': [4, 3, 3, 7],
                              'purple': [2, 3, 3, 5],
                              'forest_green': [2, 3, 3, 5]}

TABLE_STENCIL = {'1': [np.array([[0, 0], [640, 0], [640, 289], [607, 273], [607, 210], [0, 210]], np.int32),  # Not set yet
                      np.array([[0, 293], [640, 322], [640, 480], [0, 480]], np.int32)],
                 '2': [np.array([[0, 0], [640, 0], [640, 289], [607, 273], [607, 210], [77, 210], [77, 273], [0, 280]], np.int32),
                      np.array([[0, 293], [640, 322], [640, 480], [0, 480]], np.int32)],
                 '3': [np.array([[0, 0], [640, 0], [640, 301], [621, 291], [621, 220], [102, 220], [102, 273], [0, 280]], np.int32),
                      np.array([[0, 296], [640, 325], [640, 480], [0, 480]], np.int32)],
                 '4': [np.array([[0, 0], [640, 0], [640, 293], [618, 283], [618, 220], [92, 220], [92, 282], [0, 290]], np.int32),  # Not set yet
                      np.array([[0, 298], [640, 314], [640, 480], [0, 480]], np.int32)],
                 '5': [np.array([[0, 0], [640, 0], [640, 289], [607, 273], [607, 210], [0, 210]], np.int32),  # Not set yet
                      np.array([[0, 293], [640, 322], [640, 480], [0, 480]], np.int32)],
                 '6': [np.array([[0, 0], [640, 0], [640, 227], [366, 233], [108, 193], [104, 292], [0, 296]], np.int32),
                      np.array([[0, 304], [640, 324], [640, 480], [0, 480]], np.int32)]}

TABLE_BACK_POSITION = {'1': [],
                       '2': [range(351, 560, 3), 262],
                       '3': [],
                       '4': [range(247, 566, 3), 269],
                       '5': [],
                       '6': []}


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
        self.rectangle_width = iteration_range[2]
        self.rectangle_height = iteration_range[3]

    def apply(self, img_mask):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (self.rectangle_width, self.rectangle_width))
        image_erode = cv2.erode(img_mask, kernel, iterations=self.erode_iteration)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (self.rectangle_width, self.rectangle_height))
        image_dilate = cv2.dilate(image_erode, kernel, iterations=self.dilate_iteration)
        return image_dilate


class FormStencil:
    def __init__(self, poly_lines):
        self.poly_lines = []
        for poly_line in poly_lines:
            poly_line_reshaped = poly_line.reshape((-1, 1, 2))
            self.poly_lines.append(poly_line_reshaped)

    def apply(self, img_mask):
        img_result = np.copy(img_mask)
        cv2.fillPoly(img_result, self.poly_lines, (0, 0, 0))
        return img_result


class Cube:
    NEGATIVE_POSITION_TOLERANCE_IN_MM = -100
    NO_POSITION_TOLERANCE = 4

    def __init__(self, a_color):
        self.color = a_color
        self.position = None
        self.attempt_without_position_remaining = 0
        self.color_filter = ColorFilter(RANGES_FOR_COLOR_FILTER.get(a_color))
        self.form_filter = FormFilter(PARAMETERS_FOR_FORM_FILTER.get(a_color))

    def apply_filters(self, img_hsv, kinect=None):
        img_mask = self.color_filter.apply(img_hsv)
        img_mask = self.form_filter.apply(img_mask)
        if kinect is not None:
            img_mask = FormStencil(TABLE_STENCIL.get(kinect.table)).apply(img_mask)
        return img_mask

    def find_position(self, img_hvg, kinect, x_shift=0):
        img_mask = self.apply_filters(img_hvg, kinect)
        new_position = kinect.find_object_position(img_mask)
        self.adjust_position(new_position)
        return self.position

    def adjust_position(self, position):
        if self.is_valid_position(position):
            self.position = position
            self.attempt_without_position_remaining = self.NO_POSITION_TOLERANCE
        elif self.attempt_without_position_remaining == 0:
            self.position = (-500, -500)
        else:
            self.attempt_without_position_remaining -= 1

    def is_valid_position(self, position):
        return position[0] > self.NEGATIVE_POSITION_TOLERANCE_IN_MM \
            and position[1] > self.NEGATIVE_POSITION_TOLERANCE_IN_MM


class WhiteCube(Cube):
    def __init__(self):
        self.color = 'white'
        self.position = None
        self.attempt_without_position_remaining = 0
        self.white_filter = ColorFilter([([0, 0, 190], [180, 25, 255])])
        self.black_filter = ColorFilter([([0, 0, 0], [180, 256, 120])])
        self.form_filter = FormFilter([4, 4, 3, 2])
        self.black_form_filter = FormFilter([0, 5, 3, 3])
        self.max_pixel_length = 50

    def apply_filters(self, img_hsv, kinect=None):
        img_mask_white = self.white_filter.apply(img_hsv)
        img_mask_black = self.black_filter.apply(img_hsv)
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


class WhiteCubeForInBoardCamera(WhiteCube):
    def __init__(self):
        WhiteCube.__init__(self)
        self.black_form_filter = FormFilter([0, 3, 4, 4])
        self.white_filter = ColorFilter([([0, 0, 150], [180, 40, 255])])
        self.max_pixel_length = 200


class BlackCube(Cube):
    CALIBRATION_ATTEMPT = 25

    def __init__(self):
        self.color = 'black'
        self.position = None
        self.always_black_mask = None
        self.calibration_attempt_remaining = self.CALIBRATION_ATTEMPT
        self.attempt_without_position_remaining = 0
        self.color_filter = ColorFilter([([0, 0, 0], [180, 256, 120])])
        self.form_filter = FormFilter([3, 1, 3, 3])

    def apply_filters(self, img_hsv, kinect=None):
        img_mask = self.color_filter.apply(img_hsv)
        if self.calibration_attempt_remaining > self.CALIBRATION_ATTEMPT-5:
            self.calibration_attempt_remaining -= 1
            self.always_black_mask = img_mask
        elif self.calibration_attempt_remaining > 0:
            self.always_black_mask = cv2.bitwise_or(self.always_black_mask, img_mask)
            self.calibration_attempt_remaining -= 1
        else:
            img_mask = cv2.bitwise_and(cv2.bitwise_xor(img_mask, self.always_black_mask), img_mask)
        img_mask = self.form_filter.apply(img_mask)
        return img_mask

    def find_position(self, img_hvg, kinect, x_shift=0):
        x_values = []
        y_values = []
        table_back = TABLE_BACK_POSITION.get(kinect.table)
        for x in table_back[0]:
            pixel_position = (x, table_back[1])
            position = kinect._apply_matrix_transformation(kinect._get_world_in_cloud(pixel_position))
            if Position(position[0], position[1]).is_valid():
                if position[1]> 850 and position[1]<2000 and self.verify_color(img_hvg, pixel_position):
                    x_values.append(position[0])
                    y_values.append(position[1])
        if x_values.__len__() > 0:
            return (self.get_median(x_values), self.get_median(y_values))
        return (0, 0)

    def get_median(self, values):
        return np.median(np.array(values))

    def verify_color(self, image_hsv, position):
        pixel = image_hsv[position[1], position[0]]
        if pixel[2] < 120:
            return True
        return False
