import os
import cv2
import numpy as np
import math
import time
from vision.cube import FormStencil

CAMERA_MATRIX = [[555.81341097, 0. ,323.81267756], [0., 555.07406939, 244.96419131], [0., 0.,1.]]
DIST_COEFS = [[0.26812386, -1.12309446,  0.00970802, -0.00178942,  0.97162928]]
POLYLINE = np.array([[0, 250], [640, 250], [640, 480], [0, 480]], np.int32)
ANGLE = 45


class NoCameraDetectedException(Exception):
    def __init__(self):
        pass


class Camera():

    def __init__(self):
        self.capt_obj = cv2.VideoCapture(1)
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
        img = cv2.GaussianBlur(img_rgb, (3, 3), 10)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        img_binary = cube.color_filter.apply(img)
        dilation = np.ones((3, 3), "uint8")
        img_binary = cv2.dilate(img_binary, dilation)
        #img_binary = self.apply_polyline(img_binary)
        return img_binary

    def apply_filter_black_cube(self, img_rgb):
        img = cv2.GaussianBlur(img_rgb, (3, 3), 10)
        img2gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(img2gray, 127, 255, 0)
        #mask = self.apply_polyline(mask)
        return mask

    def apply_polyline(self, image):
        stencil = FormStencil([self.polyline])
        mask = stencil.apply(image)
        return mask

    def find_contour_cube_black(self, image):
        contours, hierarchy = cv2.findContours(image,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        cnt = contours[0]
        biggest = None
        max_area = 0
        approx = None
        for i in contours:
            area = cv2.contourArea(i)
            if area > 5000 and area < 100000 :
                peri = cv2.arcLength(i,True)
                approx = cv2.approxPolyDP(i,0.02*peri,True)
                if area > max_area and len(approx)==4:
                    biggest = approx
                    max_area = area
        #corners = np.array([approx],dtype=np.int32)
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

    def find_marker_image(self, moment, largest_contour):
        marker = None
        if moment is not None:
            if moment["m00"] > 1000: # / scale_down:
                marker = cv2.minAreaRect(largest_contour)
        return marker

    def define_contour_array(self, contour):
        contour_array = np.array(np.array(contour[0][0]))
        for x  in xrange(1,len(contour[0])):
            contour_array = np.concatenate((contour_array,np.array(contour[0][x])),axis=0)
        return contour_array

    def get_angle_cube(self, contour, corner):
        oposite_side = abs(contour[0][1]-contour[corner][1])
        adjacent_side = abs(contour[0][0]-contour[corner][0])
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



