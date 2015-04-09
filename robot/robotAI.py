import time
from pathfinding.pathfinding import Pathfinding
from controller.serialCom import Robot
from vision.robotLocator import RobotPosition
import pathfinding.constants as tableConsts
import numpy


class RobotAI:
    def __init__(self, base_station_client):
        self.pathfinder = Pathfinding()
        self.robot = Robot()
        self.robot_angle_and_position = RobotPosition()
        self.base_station = base_station_client

    def run_sequence(self):
        self.update_robot_position_from_kinect()
        self.move_robot_to(tableConsts.DOCK_POINT)
        self.update_robot_position_from_kinect()
        self.move_to_exactly_to_docking_point()
        # flag_matrix = self.resolve_atlas_enigma()
        # self.display_flag_for_five_seconds(flag_matrix)
        # self.move_robot_to(tableConsts.SAFE_POINT)
        # self.update_robot_position_from_kinect()
        # self.construct_flag(flag_matrix)
        # self.construct_flag(['red'])

    def resolve_atlas_enigma(self):
        self.move_robot_to(tableConsts.ATLAS_ZONE_COORDINATES)
        self.robot.change_led_color('red', 9)
        time.sleep(2)
        self.robot.change_led_color('off', 9)
        return self.receive_flag_from_base_station()

    def construct_flag(self, flag_matrix):
        for cube_index, cube in enumerate(flag_matrix):
            if cube:
                # self.grab_cube(str(cube), cube_index)
                self.place_cube(cube_index)
                # self.move_robot_to(tableConsts.SAFE_POINT)
                # self.update_robot_position_from_kinect()

    def grab_cube(self, cube, cube_index):
        self.robot.change_led_color(cube, cube_index)
        self.move_robot_to(self.receive_cube_position_from_kinect(), True)
        self.approach_cube()

    def place_cube(self, cube_index):
        self.move_robot_to(tableConsts.DOCK_POINT)
        self.update_robot_position_from_kinect()
        self.move_to_exactly_to_docking_point()
        # self.drop_cube_at_intended_point(cube_index)

    def drop_cube_at_intended_point(self, cube_index):
        cube_movement_dictionary = tableConsts.CUBE_DROP_MOVEMENTS_LIST[cube_index]
        if cube_movement_dictionary.get('direction') != 'forward':
            self.robot.move(cube_movement_dictionary.get('direction'),
        self.robot.move('forward', cube_movement_dictionary.get('length_distance')))
        # self.robot.move_gripper_vertically(False)
        # self.robot.change_pliers_opening(True, False)
        self.robot.move('reverse', cube_movement_dictionary.get('length_distance'))
        # self.robot.move_gripper_vertically(True)
        # self.robot.change_pliers_opening(True, True)

    def approach_cube(self):
        pass

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
        position_updated = False
        while not position_updated:
            time.sleep(2)
            angle_and_position_from_kinect = self.base_station.fetch_robot_position()
            print 'unupdated pos: '+ str(self.robot_angle_and_position.angle) + ' ' + str(self.robot_angle_and_position.position)
            position_updated = self.robot_angle_and_position.update_with_kinect(angle_and_position_from_kinect[1],
                                                             angle_and_position_from_kinect[0])
            print 'updated pos: '+ str(self.robot_angle_and_position.angle) + ' ' + str(self.robot_angle_and_position.position)

    def receive_cube_position_from_kinect(self):
        pass

    def move_robot_to(self, target_position, stop_at_buffer=False, movement_direction='forward'):
        if stop_at_buffer:
            pathfinding_result = self.pathfinder.find_path_to_cube_buffer_zone(self.robot_angle_and_position,
                                                                               target_position)
        else:
            pathfinding_result = self.pathfinder.find_path_to_point(self.robot_angle_and_position, target_position)

        self._send_move_commands(pathfinding_result, movement_direction)

    def rotate_robot_to_target(self, target_angle_in_degrees):
        rotation_angle = self.pathfinder.determine_rotation_angle(self.robot_angle_and_position.angle,
                                                                  target_angle_in_degrees)
        self._send_move_commands((rotation_angle, 0), 'forward')

    def _send_move_commands(self, tuple_result_from_pathfinding, movement_direction):
        print '_sendmoveocmmand'
        if tuple_result_from_pathfinding[0] != 0:
            if tuple_result_from_pathfinding[0] > 0:
                self.robot.rotate(True, tuple_result_from_pathfinding[0])
            else:
                self.robot.rotate(False, abs(tuple_result_from_pathfinding[0]))
        if tuple_result_from_pathfinding[1] != 0:
            print 'moving'
            self.robot.move(movement_direction, tuple_result_from_pathfinding[1])
        self.robot_angle_and_position.update_with_pathfinding_tuple(tuple_result_from_pathfinding)

    def tranpose_flag_matrix(self, flag_matrix):
        flag_array = numpy.array(flag_matrix)
        flag_array_reshaped = flag_array.reshape((3, 3))
        transposed_array = flag_array_reshaped.transpose()
        reshaped_transposed_array = transposed_array.reshape((1, 9))
        transposed_flag_matrix = reshaped_transposed_array[0].tolist()
        return transposed_flag_matrix

    def move_to_exactly_to_docking_point(self, delta_angle=0, delta_x=0, delta_y=0):
        print 'adjusting position'
        angle_range = 1
        x_range = 10
        y_range = 10
        print 'adjusting position, delta angle : '
        self.rotate_precisely_to_dock_angle(angle_range, delta_angle)
        print 'angle adjusted'
        self.move_precisely_to_dock_x(x_range, delta_x)
        print 'x adjusted'
        self.move_precisely_to_dock_y(y_range, delta_y)
        print 'y adjusted'
        self.update_robot_position_from_kinect()
        delta_angle = self.pathfinder.determine_rotation_angle(self.robot_angle_and_position.angle,
                                                               tableConsts.DOCK_ANGLE)
        delta_x = tableConsts.DOCK_POINT[0] - self.robot_angle_and_position.position[0]
        delta_y = tableConsts.DOCK_POINT[1] - self.robot_angle_and_position.position[1]
        if abs(delta_angle) > angle_range or abs(delta_x) > x_range or abs(delta_y) > y_range:
            self.move_to_exactly_to_docking_point(delta_angle, delta_x, delta_y)

    def rotate_precisely_to_dock_angle(self, angle_range, delta_angle):
        temp_delta_angle = delta_angle
        print 'trying rotation'
        print delta_angle
        print 'allo5'
        if temp_delta_angle == 0:
            print 'allo4'
            print str(tableConsts.DOCK_ANGLE)
            print 'allo5'
            print str(self.robot_angle_and_position.angle)
            temp_delta_angle = self.pathfinder.determine_rotation_angle(self.robot_angle_and_position.angle,
                                                                        tableConsts.DOCK_ANGLE)
            print 'temp delta angle: ' + str(temp_delta_angle)
        if abs(temp_delta_angle) > angle_range:
            print 'allo3'
            if temp_delta_angle < 0:
                print 'allo 2'
                self.robot.rotate(False, abs(temp_delta_angle), True)
                print 'rotating right'
            else:
                print 'allo'
                self.robot.rotate(True, temp_delta_angle, True)
                print 'rotating left'

    def move_precisely_to_dock_x(self, x_range, delta_x):
        if delta_x == 0:
            delta_x = tableConsts.DOCK_POINT[0] - self.robot_angle_and_position.position[0]
        if abs(delta_x) > x_range:
            if delta_x < 0:
                self.robot.move('left', abs(delta_x))
            else:
                self.robot.move('right', delta_x)

    def move_precisely_to_dock_y(self, y_range, delta_y):
        if delta_y == 0:
            delta_y = tableConsts.DOCK_POINT[1] - self.robot_angle_and_position.position[1]
        if abs(delta_y) > y_range:
            if delta_y < 0:
                self.robot.move('forward', abs(delta_y))
            else:
                self.robot.move('reverse', delta_y)