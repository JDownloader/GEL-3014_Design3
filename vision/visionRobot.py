import time
import math
from camera import Camera
from cube import *


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

class VisionRobot():

    def __init__(self, a_camera):
        self.camera = a_camera

    def getImage(self):
        cap = self.camera.getCapt()
        image = cap.read()
        image = self.camera.remmaping_image()
        return image

    def findAngleCube(self, square):
        if len(square) == 6:
            rightAngle = camera.get_angle_cube(square, 3)
        elif len(square) == 4:
            rightAngle = camera.get_angle_cube(square, 2)
        return rightAngle

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




    # def define_corner_ref(self, square):
    #     if square[]


if __name__ == "__main__":


    cv2.namedWindow('BGR', cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow('masque', cv2.WINDOW_AUTOSIZE)

    camera = Camera()
    cap = camera.getCapt()
    vision = VisionRobot(camera)

    while cap.isOpened():

        cap.grab()
        # cube = WhiteCube()
        # image = cv2.imread('cuboW2.png')
        cube = Cube('blue')
        image = cv2.imread('essaiCube15.png')


        height, width, depth = image.shape
        dst_ima = camera.remmaping_image(image)
        square = vision.findSquareCube(dst_ima, cube)
        if len(square)==6 or len(square)==4:
            angle = vision.findAngleCube(square)



        cv2.drawContours(dst_ima, [square], 0, (0, 0, 255), 2)
        cv2.imshow("BGR", dst_ima)




        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cap.release()
    cv2.destroyAllWindows()



print square
print angle


