import math
import numpy as np


class CalibrationValues:
    def __init__(self, angle, trans_x, trans_y, dilatate_x = 1, dilatate_y = 1):
        self.angle = angle
        self.trans_x = trans_x
        self.trans_y = trans_y
        self.dilatate_x = dilatate_x
        self.dilatate_y = dilatate_y

    def set_values(self,angle, trans_x, trans_y, dilatate_x, dilatate_y):
        self.angle = angle
        self.trans_x = trans_x
        self.trans_y = trans_y
        self.dilatate_x = dilatate_x
        self.dilatate_y = dilatate_y

    def get_rotation_matrix(self):
        return [[math.cos(self.angle), -math.sin(self.angle), self.trans_x],
                [math.sin(self.angle), math.cos(self.angle), self.trans_y],
                    [0, 0, 1]]

TABLE_CALIBRATION_DISTANCES = {'1': CalibrationValues(-0.4021, 0.05, -0.570, 1.13, 1),  # Not set yet
                               '2': CalibrationValues(-0.3971, 0.05, -0.570, 1.09, 1.03),
                               '3': CalibrationValues(-0.4021, 0.05, -0.570, 1.13, 1),
                               '4': CalibrationValues(-0.4021, 0.05, -0.570, 1.13, 1),  # Not set yet
                               '5': CalibrationValues(-0.4021, 0.05, -0.570, 1.13, 1),  # Not set yet
                               '6': CalibrationValues(-0.4021, 0.05, -0.570, 1.13, 1)}   # Not set yet


class DistanceCalibration:
    def __init__(self, table):
        self.calibration_value = TABLE_CALIBRATION_DISTANCES.get(table)

    def apply_matrix_transformation(self, point_in_world):
        trans_rot = self.calibration_value.get_rotation_matrix()
        transformed_point = np.dot(trans_rot, point_in_world)
        transformed_point[0] *= self.calibration_value.dilatate_x
        transformed_point[1] *= self.calibration_value.dilatate_y
        return transformed_point