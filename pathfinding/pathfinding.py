import math
import constants
import numpy


class Pathfinding:
    def __init__(self):
        pass

    def pathfind_to_cube_buffer_zone(self, robot_position, cube_center):
        unbuffered_path = self.pathfind_to_point(robot_position, cube_center)
        distance_with_buffer = unbuffered_path[1] - constants.CUBE_BUFFER_RADIUS
        return (int(unbuffered_path[0]), int(distance_with_buffer))

    def pathfind_to_cube(self, cube_angle_compared_to_robot):
        # rotation
        pass

    def pathfind_to_point(self, robot_position, point):
        delta_x = float(point[0] - robot_position.position[0])
        delta_y = float(point[1] - robot_position.position[1])
        # We assume the robot is facing away from the kinect, 90 degrees from the x axis.
        # For a positive angle, the robot must rotate to its left (anti-clockwise)
        target_angle = 0
        if delta_y == 0:
            if delta_x > 0:
                target_angle = 90
            elif delta_x < 0:
                target_angle = -90
        else:
            target_angle = math.degrees(math.atan2(delta_x, delta_y))
        rotation = self.determine_rotation_angle(math.degrees(robot_position.angle), target_angle)
        distance = self.calculate_hypotenuse(delta_x, delta_y)
        return (int(rotation), int(distance))

    def calculate_hypotenuse(self, x_length, y_length):
        return math.sqrt(pow(x_length, 2) + pow(y_length, 2))

    def determine_rotation_angle(self, robot_current_angle_in_degrees, target_angle_in_degrees):
        rotation_angle = target_angle_in_degrees - robot_current_angle_in_degrees
        if rotation_angle < -180:
            rotation_angle = rotation_angle + 360
        elif rotation_angle > 180:
            rotation_angle = rotation_angle - 360
        return int(rotation_angle)