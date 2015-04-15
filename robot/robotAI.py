import time
from pathfinding.pathfinding import Pathfinding
from controller.serialCom import Robot
from robotVision.visionRobot import VisionRobot
from vision.robotLocator import RobotPosition, Position
import pathfinding.constants as tableConsts
import numpy
import math

class RobotAI:
    def __init__(self, base_station_client):
        self.pathfinder = Pathfinding()
        self.robot = Robot()
        self.robot_angle_and_position = RobotPosition()
        self.base_station = base_station_client
        self.table_number = 4

    def run_sequence(self):
        self.pre_atlas_sequence()
        flag = self.tranpose_flag_matrix(self.resolve_atlas_enigma())
        self.construct_flag(flag)

    def pre_atlas_sequence(self):
        self.update_robot_position_from_kinect()
        self.move_robot_to(tableConsts.DOCK_POINT)
        self.rotate_robot_to_target(0)
        self.move_exactly_to_docking_point()

    def resolve_atlas_enigma(self):
        two_step_path_to_atlas = self.pathfinder.find_two_step_path_to_point(self.robot_angle_and_position,
                                                                             tableConsts.ATLAS_ZONE_COORDINATES)
        self.move_two_step_to_point(two_step_path_to_atlas)
        self.robot.change_led_color('red', 9)
        time.sleep(2)
        self.robot.change_led_color('off', 9)
        return self.receive_flag_from_base_station()

    def construct_flag(self, flag_matrix):
        self.display_flag_for_five_seconds(flag_matrix)
        for cube_index, cube in enumerate(flag_matrix):
            if cube is not None:
                self.grab_cube(str(cube), cube_index)
                self.place_cube(cube_index)
                self.rotate_robot_to_target(0)
                self.move_exactly_to_docking_point()

    def grab_cube(self, cube, cube_index):
        self.robot.change_led_color(cube, cube_index)
        cube_position = self.kinect_cube_find_sequence(cube)
        path_to_cube = self.pathfinder.find_two_step_path_to_cube(self.robot_angle_and_position, cube_position)
        self.move_two_step_to_point(path_to_cube)
        self.move_robot_to_pickup_cube(cube)
        self.pickup_cube()

    def place_cube(self, cube_index):
        self.rotate_robot_to_target(0)
        path_to_dock = self.pathfinder.find_two_step_path_to_point(self.robot_angle_and_position,
                                                                   tableConsts.DOCK_POINT)
        self.move_two_step_to_point(path_to_dock)
        self.rotate_robot_to_target(0)
        self.update_robot_position_from_kinect()
        self.move_exactly_to_docking_point()
        self.rotate_robot_to_target(180)
        self.drop_cube_at_intended_point(cube_index)

    def drop_cube_at_intended_point(self, cube_index):
        cube_movement_dictionary = tableConsts.CUBE_DROP_MOVEMENTS_LIST[cube_index]
        if cube_movement_dictionary.get('direction') != 'forward':
            self.robot.move(cube_movement_dictionary.get('direction'), cube_movement_dictionary.get('width_distance'))
        self.robot.move('forward', cube_movement_dictionary.get('length_distance'))
        self.robot.move_gripper_vertically(0)
        self.robot.change_pliers_opening(1)
        self.robot.move('reverse', cube_movement_dictionary.get('length_distance'))
        if cube_movement_dictionary.get('direction') != 'forward':
            self.robot.move(self.reverse_movement_direction(cube_movement_dictionary.get('direction')),
                            cube_movement_dictionary.get('width_distance'))
        self.robot.move_gripper_vertically(2)
        self.robot.change_pliers_opening(2)

    def move_robot_to_pickup_cube(self, cube_color):
        camera = VisionRobot(cube_color)
        self.center_robot_on_cube(camera)
        self.approach_cube(camera)

    def display_flag_for_five_seconds(self, flag_matrix):
        for index, item in enumerate(flag_matrix):
            if item:
                self.robot.change_led_color(item, index)
        time.sleep(5)
        for index, item in enumerate(flag_matrix):
            if item:
                self.robot.change_led_color('off', index)

    def receive_flag_from_base_station(self):
        flag_matrix = self.base_station.fetch_flag()
        return flag_matrix

    def update_robot_position_from_kinect(self):
        time.sleep(0.25)
        angle_and_position_from_kinect = self.base_station.fetch_robot_position()
        while angle_and_position_from_kinect[0] is None:
            angle_and_position_from_kinect = self.base_station.fetch_robot_position()
            self.robot.rotate(True, 1)
            print 'kinect pos is love'
        self.robot_angle_and_position.angle = angle_and_position_from_kinect[0] + \
                                              tableConsts.TABLE_ANGLE_ADJUSTMENT[self.table_number]
        self.robot_angle_and_position.position = angle_and_position_from_kinect[1]

    def receive_cube_position_from_kinect(self, cube_color):
        cube_pos = self.base_station.fetch_cube_position(cube_color)
        return cube_pos

    def move_robot_to(self, target_position, stop_at_buffer=False, movement_direction='forward'):
        if stop_at_buffer:
            pathfinding_result = self.pathfinder.find_path_to_cube_buffer_zone(self.robot_angle_and_position,
                                                                               target_position)
        else:
            pathfinding_result = self.pathfinder.find_path_to_point(self.robot_angle_and_position, target_position)
        self.send_path_to_base_station(pathfinding_result)

        self._send_move_commands(pathfinding_result, movement_direction)

    def rotate_robot_to_target(self, target_angle_in_degrees):
        rotation_angle = self.pathfinder.determine_rotation_angle(self.robot_angle_and_position.angle,
                                                                  target_angle_in_degrees)
        self._send_move_commands((rotation_angle, 0), 'forward')

    def _send_move_commands(self, tuple_result_from_pathfinding, movement_direction):
        if tuple_result_from_pathfinding[0] != 0:
            if tuple_result_from_pathfinding[0] > 0:
                self.robot.rotate(True, tuple_result_from_pathfinding[0])
            else:
                self.robot.rotate(False, abs(tuple_result_from_pathfinding[0]))
        if tuple_result_from_pathfinding[1] != 0:
            self.robot.move(movement_direction, tuple_result_from_pathfinding[1])
        self.robot_angle_and_position.update_with_pathfinding_tuple(tuple_result_from_pathfinding)

    def tranpose_flag_matrix(self, flag_matrix):
	print flag_matrix
	if len(flag_matrix) > 9:
            flag_matrix.pop()
        flag_array = numpy.array(flag_matrix)
        print flag_array
        flag_array_reshaped = flag_array.reshape((3, 3))
        transposed_array = flag_array_reshaped.transpose()
        transposed_array[[0, 2],:] = transposed_array[[2, 0],:]
        reshaped_transposed_array = transposed_array.reshape((1, 9))
        transposed_flag_matrix = reshaped_transposed_array[0].tolist()
        return transposed_flag_matrix

    def move_exactly_to_docking_point(self, delta_angle=0, delta_x=0, delta_y=0):
        # assumning robot is at 0 degree
        angle_range = 2
        x_range = 10
        y_range = 10
        self.rotate_precisely_to_dock_angle(angle_range, delta_angle)
        self.move_precisely_to_dock_x(x_range, delta_x)
        self.move_precisely_to_dock_y(y_range, delta_y)
        self.update_robot_position_from_kinect()
        delta_angle = self.pathfinder.determine_rotation_angle(self.robot_angle_and_position.angle,
                                                               0)
        delta_x = tableConsts.DOCK_POINT[0] - self.robot_angle_and_position.position[0]
        delta_y = tableConsts.DOCK_POINT[1] - self.robot_angle_and_position.position[1]
        if abs(delta_angle) > angle_range or abs(delta_x) > x_range or abs(delta_y) > y_range:
            self.move_exactly_to_docking_point(delta_angle, delta_x, delta_y)

    def rotate_precisely_to_dock_angle(self, angle_range, delta_angle):
        temp_delta_angle = delta_angle
        if temp_delta_angle == 0:
            temp_delta_angle = self.pathfinder.determine_rotation_angle(self.robot_angle_and_position.angle,
                                                                        0)
        if abs(temp_delta_angle) > angle_range:
            if temp_delta_angle < 0:
                self.robot.rotate(False, abs(temp_delta_angle), True)
            else:
                self.robot.rotate(True, temp_delta_angle, True)

    def move_precisely_to_dock_x(self, x_range, delta_x):
        if delta_x == 0:
            delta_x = tableConsts.DOCK_POINT[0] - self.robot_angle_and_position.position[0]
        if abs(delta_x) > x_range:
            if delta_x < 0:
                self.robot.move('right', abs(delta_x))
            else:
                self.robot.move('left', delta_x)

    def move_precisely_to_dock_y(self, y_range, delta_y):
        if delta_y == 0:
            delta_y = tableConsts.DOCK_POINT[1] - self.robot_angle_and_position.position[1]
        if abs(delta_y) > y_range:
            if delta_y < 0:
                self.robot.move('reverse', abs(delta_y))
            else:
                self.robot.move('forward', delta_y)

    def reverse_movement_direction(self, direction_to_be_reversed):
        reversed_direction = 'right'
        if direction_to_be_reversed == 'forward':
            reversed_direction = 'reverse'
        elif direction_to_be_reversed == 'reverse':
            reversed_direction = 'forward'
        elif direction_to_be_reversed == 'right':
            reversed_direction = 'left'
        return reversed_direction

    def center_robot_on_cube(self, camera_instance):
        camera_delta_x = camera_instance.find_cube_center()[0]
        movement_distance = 50
        while camera_delta_x is None:
            self.move_in_direction_and_keep_angle('left', movement_distance)
            camera_delta_x = camera_instance.find_cube_center()[0]
            if camera_delta_x is None:
                self.move_in_direction_and_keep_angle('right', movement_distance + 50)
                camera_delta_x = camera_instance.find_cube_center()[0]
                movement_distance += 50
        while abs(camera_delta_x) >= 15:
            if camera_delta_x >= 0:
                self.move_in_direction_and_keep_angle('left', 10)
            else:
                self.move_in_direction_and_keep_angle('right', 10)
            camera_delta_x = camera_instance.find_cube_center()[0]
            while camera_delta_x is None:
                self.move_in_direction_and_keep_angle('reverse', 10)
                camera_delta_x = camera_instance.find_cube_center()[0]

    def approach_cube(self, camera_instance):
        self.robot.gripper_controller.change_vertical_position(0)
        self.robot.gripper_controller.pliers_control(2)
        camera_delta_y = camera_instance.find_cube_center()[1]
        while camera_delta_y > -150:
            self.center_robot_on_cube(camera_instance)
            self.move_in_direction_and_keep_angle('forward', 20)
            camera_delta_y = camera_instance.find_cube_center()[1]
            if camera_delta_y is None:
                self.move_in_direction_and_keep_angle('reverse', 30)
                self.center_robot_on_cube(camera_instance)
                camera_delta_y = 0
        self.move_in_direction_and_keep_angle('forward', 30)

    def move_in_direction_and_keep_angle(self, direction, distance):
        self.robot.move(direction, distance)
        print 'moving' + direction
        self.robot_angle_and_position.update_with_movement_direction_and_distance(direction, distance)

    def pickup_cube(self):
        self.robot.gripper_controller.pliers_control(0)
        self.robot.gripper_controller.change_vertical_position(1)
        self.move_in_direction_and_keep_angle('reverse', 50)
        self.robot.gripper_controller.change_vertical_position(0)
        self.robot.gripper_controller.pliers_control(2)
        self.move_in_direction_and_keep_angle('forward', 50)
        self.robot.gripper_controller.pliers_control(0)
        self.robot.gripper_controller.change_vertical_position(2)

    def move_two_step_to_point(self, movement_dictionary):
        self.send_path_to_base_station(movement_dictionary)
        self.move_in_direction_and_keep_angle(movement_dictionary['first_direction'],
                                              movement_dictionary['first_distance'])
        self.rotate_robot_to_target(movement_dictionary['angle_before_second_move'])
        self.move_in_direction_and_keep_angle(movement_dictionary['second_direction'],
                                              movement_dictionary['second_distance'])

    def kinect_cube_find_sequence(self, cube_color):
        path_to_safe_zone = self.pathfinder.find_two_step_path_to_point(self.robot_angle_and_position,
                                                                        tableConsts.SAFE_POINT)
        self.move_two_step_to_point(path_to_safe_zone)
        cube_pos = (-500, -500)
	print str(cube_color)
	print type(cube_color)
        while not Position(cube_pos[0], cube_pos[1]).is_valid():
            cube_pos = self.receive_cube_position_from_kinect(cube_color)
            self.move_in_direction_and_keep_angle('reverse', 20)
        path_to_pre_cube_fetch_point = self.pathfinder.find_two_step_path_to_point(self.robot_angle_and_position,
                                                                   tableConsts.PRE_CUBE_FETCH_POINT)
        self.move_two_step_to_point(path_to_pre_cube_fetch_point)
        return cube_pos

    def reverse_movement_dictionary(self, initial_movement_dictionary):
        reversed_dict = initial_movement_dictionary
        reversed_dict['first_direction'] = \
            self.reverse_movement_direction(initial_movement_dictionary['second_direction'])
        reversed_dict['second_direction'] = \
            self.reverse_movement_direction(initial_movement_dictionary['first_direction'])
        reversed_dict['first_distance'] = initial_movement_dictionary['second_distance']
        reversed_dict['second_distance'] = initial_movement_dictionary['first_distance']
        reversed_dict['angle_before_second_move'] = 0
        return reversed_dict

    def send_path_to_base_station(self, path):
        if type(path) is tuple:
            final_angle = 4
            arrival_point = (self.robot_angle_and_position.position[0] +
                             math.sin(math.radians(final_angle)) * path[1], self.robot_angle_and_position.position[1]
                             + math.cos(math.radians(final_angle)) * path[1])
            # self.base_station.send_pathfinding_itinerary(arrival_point)
            print arrival_point
        elif type(path) is dict:
            arrival_point = (0, 0)
            intermediate_point = (0, 0)
            if path['first_direction'] == 'forward':
                intermediate_point = (self.robot_angle_and_position.position[0] + path['first_distance'] *
                                      math.sin(math.radians(self.robot_angle_and_position.angle)),
                           self.robot_angle_and_position.position[1] + path['first_distance'] *
                           math.cos(math.radians(self.robot_angle_and_position.angle)))
            elif path['first_direction'] == 'reverse':
                intermediate_point = (self.robot_angle_and_position.position[0] + path['first_distance'] *
                                      math.sin(math.radians(self.robot_angle_and_position.angle + 180)),
                           self.robot_angle_and_position.position[1] + path['first_distance'] *
                           math.cos(math.radians(self.robot_angle_and_position.angle + 180)))
            elif path['first_direction'] == 'left':
                intermediate_point = (self.robot_angle_and_position.position[0] + path['first_distance'] *
                                      math.sin(math.radians(self.robot_angle_and_position.angle + 90)),
                           self.robot_angle_and_position.position[1] + path['first_distance'] *
                           math.cos(math.radians(self.robot_angle_and_position.angle + 90)))
            elif path['first_direction'] == 'right':
                intermediate_point = (self.robot_angle_and_position.position[0] + path['first_distance'] *
                                      math.sin(math.radians(self.robot_angle_and_position.angle - 90)),
                           self.robot_angle_and_position.position[1] + path['first_distance'] *
                           math.cos(math.radians(self.robot_angle_and_position.angle - 90)))

            intermediate_angle = self.robot_angle_and_position.angle + path['angle_before_second_move']
            if path['second_direction'] == 'forward':
                arrival_point = (intermediate_point[0] + path['second_distance'] *
                                      math.sin(math.radians(intermediate_angle)),
                           intermediate_point[1] + path['second_distance'] *
                           math.cos(math.radians(intermediate_angle)))
            elif path['second_direction'] == 'reverse':
                arrival_point = (intermediate_point[0] + path['second_distance'] *
                                      math.sin(math.radians(intermediate_angle + 180)),
                           intermediate_point[1] + path['second_distance'] *
                           math.cos(math.radians(intermediate_angle + 180)))
            elif path['second_direction'] == 'left':
                arrival_point = (intermediate_point[0] + path['second_distance'] *
                                      math.sin(math.radians(intermediate_angle + 90)),
                           intermediate_point[1] + path['second_distance'] *
                           math.cos(math.radians(intermediate_angle + 90)))
            elif path['second_direction'] == 'right':
                arrival_point = (intermediate_point[0] + path['second_distance'] *
                                      math.sin(math.radians(intermediate_angle - 90)),
                           intermediate_point[1] + path['second_distance'] *
                           math.cos(math.radians(intermediate_angle - 90)))

            # self.base_station.send_pathfinding_itinerary((intermediate_point, arrival_point))
            print (intermediate_point, arrival_point)
