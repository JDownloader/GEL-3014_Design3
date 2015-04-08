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
        # flag_matrix = self.resolve_atlas_enigma()
        # self.display_flag_for_five_seconds(flag_matrix)
        # self.move_robot_to(tableConsts.SAFE_POINT)
        # self.update_robot_position_from_kinect()
        # self.construct_flag(flag_matrix)
        self.construct_flag(['red'])

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
        print 'dockzone1'
        self.move_robot_to(tableConsts.DOCK_POINT)
        print 'upate pos1'
        self.update_robot_position_from_kinect()
        print 'rotate'
        self.rotate_robot_to_target(180)
        print 'dropcube'
        self.drop_cube_at_intended_point(cube_index)

    def drop_cube_at_intended_point(self, cube_index):
        cube_movement_dictionary = tableConsts.CUBE_DROP_MOVEMENTS_LIST[cube_index]
        if cube_movement_dictionary.get('direction') != 'forward':
            print 'moving sideways'
            self.robot.move(cube_movement_dictionary.get('direction'),
                               cube_movement_dictionary.get('width_distance'))
        print 'moving forward'
        self.robot.move('forward', cube_movement_dictionary.get('length_distance'))
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
        angle_and_position_from_kinect = self.base_station.fetch_robot_position()
        self.robot_angle_and_position.angle = angle_and_position_from_kinect[0]
        self.robot_angle_and_position.position = angle_and_position_from_kinect[1]

    def receive_cube_position_from_kinect(self):
        pass

    def move_robot_to(self, target_position, stop_at_buffer=False, movement_direction='forward'):
        print 'movecommand'
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


