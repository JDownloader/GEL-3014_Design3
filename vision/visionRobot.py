import time
import math
from camera import Camera
from cube import *
from numpy import ndarray

class VisionRobot():

    def __init__(self, a_camera):
        self.camera = a_camera

    def get_image(self):
        cap = self.camera.getCapt()
        image = cap.read()
        image = self.camera.remmaping_image()
        return image

    def find_square_cube(self, image, cube):
        new_image = self.camera.apply_filter_black_cube(image)
        square = self.camera.find_contour_cube(new_image)
        return square

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
        if size_square >= 6:
            if abs(square[0][0] - square[1][0]) < 50:
                corner = size_square -1
            else:
                corner = 1
        elif size_square == 4:
            corner = 1
        return corner

    def mouse_click_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            print "Click at %d, %d" % (x, y)

if __name__ == "__main__":


    cv2.namedWindow('BGR', cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow('masque', cv2.WINDOW_AUTOSIZE)

    camera = Camera()
    cap = camera.getCapt()
    vision = VisionRobot(camera)
    mouse = vision.mouse_click_callback
    cv2.setMouseCallback('BGR', mouse)

    while cap.isOpened():

        # Take each frame
        # _, frame = cap.read()
        # flags_i, frame = cap.retrieve(None, cv2.CAP_OPENNI_BGR_IMAGE)
        cube = BlackCube()
        image = cv2.imread('cuboN1.png')

        image = camera.remmaping_image(image)
        corners = vision.find_square_cube(image, cube)
        mask = np.zeros(image.shape,dtype=np.uint8)
        white = (255,255,255)
        cv2.fillPoly(mask,corners,white)
        masked_image = cv2.bitwise_and(image,mask)
        #cv2.drawContours(masked_image,corners,-1,(0,255,0),6)
        new_corners = camera.define_contour_array(corners)
        angle = vision.find_angle_cube(new_corners)
        cv2.imshow('BGR',masked_image)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()

print "angle", angle