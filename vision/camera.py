import os
import cv2
import numpy as np
import math
import time

CAMERA_MATRIX = [[555.81341097, 0. ,323.81267756], [0., 555.07406939, 244.96419131], [0., 0.,1.]]
DIST_COEFS = [[0.26812386, -1.12309446,  0.00970802, -0.00178942,  0.97162928]]
POLYLINE = np.array([[0, 250], [640, 250], [640, 480], [0, 480]], np.int32)
ANGLE = 45

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


class NoCameraDetectedException(Exception):
    def __init__(self):
        pass


class Camera():

    def __init__(self):
        self.capt_obj = cv2.VideoCapture(0)
        self.camera_matrix = np.array(CAMERA_MATRIX)
        self.distortion_matrix = np.array(DIST_COEFS)
        self.polyline = POLYLINE
        flags, img = self.capt_obj.read()
        if flags is False:
            raise NoCameraDetectedException()

    def getCapt(self):
        self.capt_obj.grab()
        return self.capt_obj

    def remmaping_image(self, image):
        h,  w = image.shape[:2]
        newcameramtx, roi=cv2.getOptimalNewCameraMatrix(self.camera_matrix, self.distortion_matrix, (w, h), 1, (w, h))
        img_dst = cv2.undistort(image, self.camera_matrix, self.distortion_matrix, None, newcameramtx)
        # crop the image
        x,y,w,h = roi
        img_dst = img_dst[y:y+h, x:x+w]
        return img_dst

    def apply_filter_color_cubes(self, img_rgb, cube):
        img = cv2.GaussianBlur(img_rgb, (5, 5), 0)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        img_binary = cube.color_filter.apply(img)
        dilation = np.ones((3, 3), "uint8")
        img_binary = cv2.dilate(img_binary, dilation)
        img_binary = self.apply_polyline(img_binary)
        return img_binary

    def apply_filter_black_cube(self, img_rgb):
        img = cv2.GaussianBlur(img_rgb, (5, 5), 0)
        img2gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(img2gray, 100, 255, cv2.THRESH_BINARY)
        mask = self.apply_polyline(mask)
        return mask

    def apply_polyline(self, image):
        stencil = FormStencil([self.polyline])
        mask = stencil.apply(image)
        return mask

    def find_contour_cube(self, img_binary):
        edges = cv2.Canny(img_binary, 300, 300)
        contours, hierarchy = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        max_area = 0
        largest_contour = None
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > max_area:
                max_area = area
                largest_contour = contour
        if largest_contour is not None:
            cnt_len = cv2.arcLength(largest_contour, True)
            cnt = cv2.approxPolyDP(largest_contour, 0.02*cnt_len, True)
            new_cnt = self.define_contour_array(cnt)
        return new_cnt

    def define_contour_array(self, contour):
        contour_array = np.array(np.array(contour[0]))
        for x  in xrange(1,len(contour)):
            contour_array = np.concatenate((contour_array,np.array(contour[x])),axis=0)
        return contour_array


    def get_angle_cube(self, contour, corner):
        oposite_side = abs(contour[corner][1]-contour[corner+1][1])
        adjacent_side = abs(contour[corner][0]-contour[corner+1][0])
        angle = math.atan2(oposite_side, adjacent_side)
        angle = angle*180/math.pi
        return angle

    def find_distance(self, marker, height_img, width_img):
        box = cv2.cv.BoxPoints(marker)
        box = np.int0(box)
        topedge = pow((box[3][0] - box[2][0]) , 2) + pow((box[3][1] - box[2][1]) , 2)
        upedge = pow((box[0][0] - box[1][0]) , 2) + pow((box[0][1] - box[1][1]) , 2)
        widthTop = math.sqrt(topedge)
        widthBottom = math.sqrt(upedge)
        leftedge = pow((box[1][0] - box[2][0]) , 2) + pow((box[1][1] - box[2][1]) , 2)
        rigthedge = pow((box[0][0] - box[3][0]) , 2) + pow((box[0][1] - box[3][1]) , 2)
        heightLeft = math.sqrt(leftedge)
        heightRight = math.sqrt(rigthedge)
        dArea = height_img*width_img - ((heightLeft+heightRight)/2)*((widthTop+widthBottom)/2)
        dz = 30 + dArea/100
        dy = ((240 - ((box[2][1] + box[3][1])/2 + (heightLeft + heightRight)/4 ))*dz)/585
        angleB = math.atan(dy/dz)
        distance = ((dz/math.cos(-angleB))*math.cos(-ANGLE*math.pi/180+angleB))/100

        return distance

    def find_square_cube_white(self, image):
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        img_gray = self.apply_polyline(img_gray)
        squares = self._find_squares(img_gray)
        square = self._filterSquares(squares)
        return square[1]

    def _angle_cos(self, p0, p1, p2):
        d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
        return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

    def _find_squares(self, img):
        img = cv2.GaussianBlur(img, (5, 5), 0)
        squares = []
        for gray in cv2.split(img):
            for thrs in xrange(0, 255, 26):
                if thrs == 0:
                    bin = cv2.Canny(gray, 0, 50, apertureSize=5)
                    bin = cv2.dilate(bin, None)
                else:
                    retval, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
                contours, hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
                max_area = 0
                largest_contour = None
                for cnt in contours:
                    cnt_len = cv2.arcLength(cnt, True)
                    cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
                    if len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
                        cnt = cnt.reshape(-1, 2)
                        max_cos = np.max([self._angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in xrange(4)])
                        if max_cos < 0.3:
                            squares.append(cnt)
        return squares


    def _getPerimeter(self, square):
        return math.fabs(square[1][1] - square[0][1]) + math.fabs(square[2][1] - square[3][1]) +\
               math.fabs(square[0][0] - square[3][0]) + math.fabs(square[1][0] - square[2][0])


    def _filterSquares(self, squares):
        newSquares = []
        for square in squares:
            if square[0][0] != 1 and square[0][1] != 1:
                perimeter = self._getPerimeter(square)
                if (perimeter < 600 and perimeter > 20):
                    newSquares.append(square)
        return newSquares

