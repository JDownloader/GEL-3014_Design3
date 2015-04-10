import time
import math
from camera import Camera
from vision.cube import *
from numpy import ndarray

class VisionRobot():

    def __init__(self, a_camera):
        self.camera = a_camera

    def get_image(self):
        cap = self.camera.getCapt()
        image = cap.read()
        image = self.camera.remmaping_image()
        return image

    def find_contour_cube(self, image, cube):
        new_image = self.apply_mask_image(image, cube)
        contour = None
        if cube.color is "black":
            contour = self.camera.find_contour_cube_black(new_image)
        else:
            contour = self.camera.find_largest_contour_color(new_image)
        return contour

    def find_angle_cube(self, square):
        corner = self.define_corner_number(square)
        if corner == 1 and len(square)>=6:
            angle = camera.get_angle_cube(square, corner)
            right_angle = 90 - angle
        elif corner != 1 and len(square) >= 6:
            right_angle = camera.get_angle_cube(square, corner)
        elif corner == 1 and len(square) == 4:
            right_angle = camera.get_angle_cube(square, corner)
        return right_angle

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

    def get_marker_cube(self, image, cube):
        mask_image = self.apply_mask_image(image, cube)
        moment, marker = camera.find_cube_marker(mask_image, cube)
        return marker

    def apply_mask_image(self, image, cube):
        if cube.color is "white":
            img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            image_hsv1 = cv2.resize(img_hsv, (0,0), fx=0.3, fy=0.3)
            new_image = cube.apply_filters(img_hsv)
        elif cube.color is "black":
            new_image = self.camera.apply_filter_black_cube(image)
        else:
            new_image = self.camera.apply_filter_color_cubes(image, cube)
        return new_image

    def get_moment(self, largest_contour):
        moment = None
        if largest_contour is not None:
            moment = cv2.moments(largest_contour)
        return moment

    def verifier_centre_image(self, image, moment):
        is_centre = False
        height, width, depth = image.shape
        centreX = int(moment['m10']/moment['m00'])
        centreY = int(moment['m01']/moment['m00'])
        if (centreX == width/2):
            is_centre = True
        else :
            is_centre = False
        return is_centre


if __name__ == "__main__":


    cv2.namedWindow('BGR', cv2.WINDOW_AUTOSIZE)

    camera = Camera()
    cap = camera.getCapt()
    vision = VisionRobot(camera)
    while cap.isOpened():

        # Take each frame
        _, image = cap.read()
        ##flags_i, image = cap.retrieve(None, cv2.CAP_OPENNI_BGR_IMAGE)


        cube = Cube("blue")
        #cube = WhiteCube()
        #image = cv2.imread("cubo_blanco.png")
        cube = WhiteCubeForInBoardCamera()
        image = camera.remmaping_image(image)
        height, width, depth = image.shape

        contour = vision.find_contour_cube(image, cube)
        try:
            if contour is not None:
                moment = vision.get_moment(contour)
                is_centre = vision.verifier_centre_image(image, moment)
                # centreX = int(moment['m10']/moment['m00'])
                # centreY = int(moment['m01']/moment['m00'])
                # if ((width/2) - 10 <= centreX <=  (width/2) +10):
                #     is_centre = True
                #
                # else :
                #     is_centre = False
                # cv2.drawContours(image,[contour],-1,(0,255,0),6)
                # cv2.circle(image, (centreX, centreY), 5, (0,0,255), -1)
                print is_centre

        except:
            pass

        cv2.imshow('BGR', image)


        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()

