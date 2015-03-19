import os
import cv2
import numpy as np

CAMERA_MATRIX = [[555.81341097, 0. ,323.81267756], [0., 555.07406939, 244.96419131], [0., 0.,1.]]
DIST_COEFS = [[0.26812386, -1.12309446,  0.00970802, -0.00178942,  0.97162928]]

class Camera():

    def params_camera_normal_view(self):
        self.camera_matrix = np.array(CAMERA_MATRIX)
        self.distortion_matrix = np.array(DIST_COEFS)

    def remmaping_image(self, image):
        h,  w = image.shape[:2]
        newcameramtx, roi=cv2.getOptimalNewCameraMatrix(self.camera_matrix, self.distortion_matrix, (w, h), 1, (w, h))
        dst = cv2.undistort(image, self.camera_matrix, self.distortion_matrix, None, newcameramtx)
        # crop the image
        x,y,w,h = roi
        dst = dst[y:y+h, x:x+w]
        return dst

    def find_cube_marker(self, img_rgb, cube):
        img_binary = cube.color_filter.applyCamera(img_rgb)
        dilation = np.ones((3, 3), "uint8")
        img_binary = cv2.dilate(img_binary, dilation)
        contours, hierarchy = cv2.findContours(img_binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        max_area = 0
        largest_contour = None
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > max_area:
                max_area = area
                largest_contour = contour
        if not largest_contour == None:
            moment = cv2.moments(largest_contour)
            if moment["m00"] > 1000: # / scale_down:
                marker = cv2.minAreaRect(largest_contour)

        return marker

    def get_angle_cube(self, marker):
        return marker[2]
