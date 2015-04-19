import time
import math
import cv2
from camera import Camera
from vision.cube import Cube, WhiteCubeForInBoardCamera, FormStencil
import numpy as np
from vision.visiontools import VisionTools

class VisionRobot():
    def __init__(self, a_color, camera=None):
        if camera is None:
            self.camera = Camera()
        else:
            self.camera = camera
        self.cube = self.set_cube(a_color)


    def set_cube(self, a_color):
        cube = None
        if a_color is 'white':
            cube = WhiteCubeForInBoardCamera()
        else:
            cube = Cube(a_color)
        return cube

    def find_contour_cube(self, image, cube):
        new_image = self.apply_mask_image(image, cube)
        contour = None
        if cube.color is "black" or cube.color is 'white':
            contour = self.camera.find_contour_cube_black(new_image)
        else:
            contour = self.camera.find_largest_contour_color(new_image)
        return contour

    def define_corner_number(self, square):
        size_square = len(square)
        if size_square == 6:
            if abs(square[0][0] - square[1][0]) < 50:
                corner = size_square -1
            else:
                corner = 1
        elif size_square == 4:
            corner = 1
        return corner

    def apply_mask_image(self, image, cube):
        new_image = self.apply_gripper_mask(image, cube.color)
        if cube.color is "white":
            new_image = VisionTools().get_hsv_image(new_image)
            new_image = cube.get_img(new_image)
        elif cube.color is "black":
            new_image = self.camera.apply_filter_black_cube(image, cube)
        else:
            new_image = self.camera.apply_filter_color_cubes(image, cube)
        return new_image

    def apply_gripper_mask(self,image,cube_color):
        polyform = [np.array([[0, 332], [257, 332], [257, 480], [0, 480]], np.int32),
                    np.array([[422, 350], [422, 480], [640, 480], [640, 350]], np.int32)]
        if cube_color == 'white':
            return FormStencil(polyform).apply(image, (254, 254, 254))
        else:
            return FormStencil(polyform).apply(image, (0, 0, 0))


    def get_moment(self, largest_contour):
        moment = None
        if largest_contour is not None:
            moment = cv2.moments(largest_contour)
        return moment

    def find_cube_center_delta(self, image, moment):
        height, width, depth = image.shape
        centerX = int(moment['m10']/moment['m00'])
        centerY = int(moment['m01']/moment['m00'])
        delta_centreX = width/2 - centerX
        delta_centreY = height/2 - centerY
        print (delta_centreX, delta_centreY)
        return delta_centreX, delta_centreY

    def find_cube_center(self):
        cap = self.camera.getCapt()
        if cap.isOpened():
            for x in range(0, 4):
                 _,image = cap.read()
            _,image = cap.read()
            # image = self.camera.remmaping_image(image)
            contour = self.find_contour_cube(image, self.cube)
            try:
                if contour is not None:
                    moment = self.get_moment(contour)
                    delta_centre = self.find_cube_center_delta(image, moment)
                    return delta_centre

            except:
                print 'Problem with camera'
            # k = cv2.waitKey(5) & 0xFF
            # if k == 27:
            #     break
            # cv2.imshow('BGR', image)
        return (None, None)
        # cv2.destroyAllWindows()


if __name__ == "__main__":

    camera = Camera()
    cap = camera.getCapt()
    color = 'white'
    vision = VisionRobot(color, camera)
    cv2.namedWindow('BGR', cv2.WINDOW_AUTOSIZE)
    
    while cap.isOpened():
        for x in range(0,10):
            _,image = cap.read()
        _,image = cap.read()
        # img_mask = vision.apply_mask_image(image, vision.cube)
        contour = vision.find_contour_cube(image, vision.cube)
        #img_mask = vision.apply_gripper_mask(img_mask, color)

        #img_mask = cv2.bitwise_(img_mask, img_mask)
        #contour = camera.find_contour_cube_black(img_mask)
        # image = self.camera.remmaping_image(image)
        # contour = vision.find_contour_cube(image, vision.cube)
        # try:
        #     if contour is not None:
        #         moment = vision.get_moment(contour)
        #         delta_centre = vision.find_cube_center_delta(image, moment)
        #         cv2.drawContours(image,[contour],-1,(0,255,0),6)
        #         print delta_centre
        #
        # except:
        #     print 'Problem with camera'
        cv2.drawContours(image,[contour],-1,(0,255,0),6)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
        cv2.imshow('BGR', image)
        # cv2.imshow('masque', img_mask)
        # cv2.imshow('mask', mask)

        # cv2.destroyAllWindows()

    #
    cv2.destroyAllWindows()

