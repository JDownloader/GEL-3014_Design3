import math
import constants


class Pathfinding:

    def find_path_to_cube_buffer_zone(self, robot_position, cube_center):
        unbuffered_path = self.find_path_to_point(robot_position, cube_center)
        distance_with_buffer = unbuffered_path[1] - constants.CUBE_BUFFER_RADIUS
        return (unbuffered_path[0], distance_with_buffer)

    def find_path_to_cube(self, cube_angle_compared_to_robot):
        pass

    def find_path_to_point(self, robot_position, point):
        delta_x = float(point[0] - robot_position.position[0])
        delta_y = float(point[1] - robot_position.position[1])
        print 'pathfinding to point'
        print 'delta x ' + str(delta_x)
        print 'delta_y ' + str(delta_y)
        print 'angle ' + str(robot_position.angle)
        # We assume 0 degree is when the robot is facing away from the kinect, 90 degrees from the x axis.
        # For a positive angle, the robot must rotate to its left (anti-clockwise)
        target_angle = 0
        if delta_y == 0:
            if delta_x > 0:
                target_angle = 90
            elif delta_x < 0:
                target_angle = -90
        else:
            target_angle = math.degrees(math.atan2(delta_x, delta_y))
        print 'pathfinding target angle' + str(target_angle)
        rotation = self.determine_rotation_angle(robot_position.angle, target_angle)
        distance = self.calculate_hypotenuse(delta_x, delta_y)
        return (rotation, distance)

    def calculate_hypotenuse(self, x_length, y_length):
        return math.sqrt(pow(x_length, 2) + pow(y_length, 2))

    def determine_rotation_angle(self, robot_current_angle_in_degrees, target_angle_in_degrees):
        rotation_angle = target_angle_in_degrees - robot_current_angle_in_degrees
        if rotation_angle < -180:
            rotation_angle += 360
        elif rotation_angle > 180:
            rotation_angle -= 360
        return rotation_angle

    def find_two_step_path_to_cube(self, robot_angle_and_position, cube):
        # assuming robot is at 0 degree
        movement_dict = {'first_direction': 0,
                         'first_distance': 0,
                         'second_direction': 0,
                         'second_distance': 0,
                         'angle_before_second_move': 0}
        delta_x = cube[0] - robot_angle_and_position.position[0]
        delta_y = cube[1] - robot_angle_and_position.position[1]
        if abs(delta_x) <= 400:
            if delta_y >= 0:
                movement_dict['first_direction'] = 'forward'
            else:
                movement_dict['first_direction'] = 'reverse'
            if abs(delta_y < constants.CUBE_BUFFER_RADIUS):
                y_distance = 0
            else:
                y_distance = abs(delta_y - constants.CUBE_BUFFER_RADIUS)
            movement_dict['first_distance'] = y_distance
            movement_dict['second_distance'] = abs(delta_x / 2)
            if delta_x >= 0:
                movement_dict['second_direction'] = 'left'
            else:
                movement_dict['second_direction'] = 'right'
        # elif cube[1] >= constants.TABLE_TOP_RIGHT_BUFFERED_WALL[1]:
        #     movement_dict['first_direction'] = 'forward'
        #     movement_dict['first_distance'] = abs(delta_y - constants.CUBE_BUFFER_RADIUS)
        #     movement_dict['second_distance'] = 200
        #     if delta_x >=0:
        #         movement_dict['second_direction'] = 'left'
        #     else:
        #         movement_dict['second_direction'] = 'right'
        elif delta_y < 0:
            if delta_x >= 0:
                movement_dict['first_direction'] = 'left'
            else:
                movement_dict['first_direction'] = 'right'
            movement_dict['first_distance'] = abs(delta_x)
            movement_dict['second_direction'] = 'reverse'
            movement_dict['second_distance'] = abs(delta_y)
        else:
            movement_dict['first_direction'] = 'forward'
            movement_dict['first_distance'] = abs(delta_y)
            movement_dict['second_direction'] = 'forward'
            movement_dict['second_distance'] = abs(delta_x / 2)
            if delta_x >= 0:
                movement_dict['angle_before_second_move'] = 90
            else:
                movement_dict['angle_before_second_move'] = -90
        return movement_dict

    def find_two_step_path_to_point(self, robot_angle_and_position, point):
        # assuming robot is at 0 degree
        movement_dict = {'first_direction': 0,
                         'first_distance': 0,
                         'second_direction': 0,
                         'second_distance': 0,
                         'angle_before_second_move': 0}
        delta_x = point[0] - robot_angle_and_position.position[0]
        delta_y = point[1] - robot_angle_and_position.position[1]
        if delta_x >= 0:
            movement_dict['first_direction'] = 'left'
        else:
            movement_dict['first_direction'] = 'right'
        if delta_y >= 0:
            movement_dict['second_direction'] = 'forward'
        else:
            movement_dict['second_direction'] = 'reverse'
        movement_dict['second_distance'] = abs(delta_y)
        movement_dict['first_distance'] = abs(delta_x)
        return movement_dict