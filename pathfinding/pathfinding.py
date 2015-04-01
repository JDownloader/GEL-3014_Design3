import math
import constants
import numpy


class Pathfinding:
    def __init__(self):
        pass

    def pathfind_to_cube_buffer_zone(self, robot_center, cube_center):
        unbuffered_path = self.pathfind_to_point(robot_center, cube_center)
        distance_with_buffer = unbuffered_path[1] - constants.CUBE_BUFFER_RADIUS
        return (unbuffered_path[0], distance_with_buffer)

    def pathfind_to_cube(self, cube_angle_compared_to_robot):
        # rotation
        pass

    def pathfind_to_point(self, robot_center, point):
        delta_x = float(robot_center.x - point.x)
        delta_y = float(point.y - robot_center.y)
        # We assume the robot is facing away from the kinect, 90 degrees from the x axis.
        # For a positive angle, the robot must rotate to its right (clockwise)
        if delta_y == 0:
            if delta_x > 0:
                angle = 90
            elif delta_x < 0:
                angle = -90
        else:
            angle = math.degrees(math.atan2(delta_x, delta_y))
        distance = self.calculate_hypotenuse(delta_x, delta_y)
        return (int(angle), int(distance))

    def calculate_hypotenuse(self, x_length, y_length):
        return math.sqrt(pow(x_length, 2) + pow(y_length, 2))