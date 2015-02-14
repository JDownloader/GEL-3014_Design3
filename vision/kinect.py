import sys
import numpy as np
import math



class Kinect():

    def __init__(self, a_cap):
        self.angle = -22.75*math.pi/180
        self.transX = 0.135
        self.transZ = -0.545
        self.cap = a_cap


    def get_matriz_transformation(self, point_reference):
        trans_rot = [[math.cos(self.angle), -math.sin(self.angle), self.transX],
                    [math.sin(self.angle), math.cos(self.angle), self.transZ],
                    [0, 0 , 1]]

        matrix_transformation = np.dot(trans_rot, point_reference)

        return matrix_transformation


    def get_position_object(self, matrix):

        position_object = [matrix[0], matrix[1]]
        return position_object







