import math
import numpy as np

class CalibrationValues:
    def __init__(self, angle, transX, transZ):
        self.angle = angle
        self.transX = transX
        self.transZ = transZ

    def get_rotation_matrix(self):
        return [[math.cos(self.angle), -math.sin(self.angle), self.transX],
                [math.sin(self.angle), math.cos(self.angle), self.transZ],
                    [0, 0, 1]]

class DistanceCalibration:
    def __init__(self):
        #self.calibration_value = CalibrationValues(-22.75/180*math.pi, 0.105, -0.535)
        #self.calibration_value = CalibrationValues(-0.3970, 0.1623, -0.4582)
        self.calibration_value = CalibrationValues(-0.3621, 0.105, -0.525)

    def apply_matrix_transformation(self, point_in_world):
        trans_rot = self.calibration_value.get_rotation_matrix()
        transformed_point = np.dot(trans_rot, point_in_world)
        return transformed_point