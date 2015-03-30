import time
import math
from camera import Camera
from cube import *


class VisionRobot():

    def __init__(self, a_camera):
        self.camera = a_camera

    def getImage(self):
        cap = self.camera.getCapt()
        image = cap.read()
        image = self.camera.remmaping_image()
        return image

    def findSquareCube(self, image, cube):
        if cube.color == "white":
            square = self.camera.find_square_cube_white(image)
        elif cube.color == "black":
            newimage = self.camera.apply_filter_black_cube(image)
            square = self.camera.find_contour_cube(newimage)
        else:
            newimage = self.camera.apply_filter_color_cubes(image, cube)
            square = self.camera.find_contour_cube(newimage)

        return square

    def findAnglesCube(self, square):
        if len(square) == 6:
            rightAngle = camera.get_angle_cube(square, 3)
            leftAngle = camera.get_angle_cube(square, 2)
        elif len(square) == 4 or len(square)==5:
            rightAngle = camera.get_angle_cube(square, 1)
            leftAngle = camera.get_angle_cube(square, 0)
        return leftAngle, rightAngle


if __name__ == "__main__":


    cv2.namedWindow('BGR', cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow('masque', cv2.WINDOW_AUTOSIZE)

    camera = Camera()
    cap = camera.getCapt()
    vision = VisionRobot(camera)

    while cap.isOpened():

        cap.grab()

        #flags, image = cap.read()
        cube = Cube('blue')
        image = cv2.imread('essaiCube15.png')
        height, width, depth = image.shape
        dst_ima = camera.remmaping_image(image)
        square = vision.findSquareCube(dst_ima, cube)
        angles = vision.findAnglesCube(square)


        cv2.drawContours(dst_ima, [square], 0, (0, 0, 255), 2)
        cv2.imshow("BGR", dst_ima)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cap.release()
    cv2.destroyAllWindows()

print angles

