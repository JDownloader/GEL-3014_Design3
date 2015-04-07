import time
from pathfinding.pathfinding import Pathfinding
from controller.serialCom import Robot
from vision.robotLocator import RobotPosition
import pathfinding.constants as tableConsts


class RobotAI:
    def __init__(self):
        self.pathfinder = Pathfinding()
        self.robot = Robot()
        self.robot_angle_and_position = RobotPosition()

    def run_sequence(self):
        flag_matrix = self.resolve_atlas_enigma()
        self.display_flag_for_five_seconds(flag_matrix)
        self.move_robot_to(tableConsts.SAFE_POINT)
        self.construct_flag(flag_matrix)

    def resolve_atlas_enigma(self):
        self.move_robot_to(tableConsts.ATLAS_ZONE_COORDINATES)
        self.robot.change_led_color('red', 9)
        time.sleep(2)
        self.robot.change_led_color('off', 9)
        return self.receive_flag_from_base_station()

    def construct_flag(self, flag_matrix):
        self.move_robot_to(tableConsts.SAFE_POINT)
        for cube_index, cube in enumerate(flag_matrix):
            if cube:
                self.grab_cube(str(cube), cube_index)
                self.place_cube(cube_index)
                self.move_robot_to(tableConsts.SAFE_POINT)

    def grab_cube(self, cube, cube_index):
        self.robot.change_led_color(cube, cube_index)
        self.move_robot_to(self.receive_cube_position_from_kinect(), True)
        self.approach_cube()

    def place_cube(self, cube_index):
        self.move_robot_to(tableConsts.DOCK_POINT)
        self.rotate_robot_to_target(180)
        self.drop_cube_at_intended_point(cube_index)

    def drop_cube_at_intended_point(self, cube_index):
        cube_movement_dictionary = tableConsts.CUBE_DROP_MOVEMENTS_LIST[cube_index]
        if cube_movement_dictionary.get('direction') != 'forward':
            self.robot.move_to(cube_movement_dictionary.get('direction'),
                               cube_movement_dictionary.get('width_distance'), 50)
        self.robot.move_to('forward', cube_movement_dictionary.get('length_distance'), 50)

    def approach_cube(self):
        pass

    def display_flag_for_five_seconds(self, flag_matrix):
        for cube_index, cube in enumerate(flag_matrix):
            self.robot.change_led_color(str(cube), cube_index)
        time.sleep(5)
        for cube_index, cube in enumerate(flag_matrix):
            self.robot.change_led_color('off', cube_index)

    def receive_flag_from_base_station(self):
        pass

    def update_robot_position_from_kinect(self):
        pass

    def receive_cube_position_from_kinect(self):
        pass

    def move_robot_to(self, target_position, stop_at_buffer=False, movement_direction='forward', movement_speed=80):
        if stop_at_buffer:
            pathfinding_result = self.pathfinder.find_path_to_cube_buffer_zone(self.robot_angle_and_position,
                                                                               target_position)
        else:
            pathfinding_result = self.pathfinder.find_path_to_point(self.robot_angle_and_position, target_position)

        self._send_move_commands(pathfinding_result, movement_direction, movement_speed)

    def rotate_robot_to_target(self, target_angle_in_degrees, rotation_speed_percentage=50):
        rotation_angle = self.pathfinder.determine_rotation_angle(self.robot_angle_and_position.angle,
                                                                  target_angle_in_degrees)
        self._send_move_commands((rotation_angle, 0), 'forward', rotation_speed_percentage)

    def _send_move_commands(self, tuple_result_from_pathfinding, movement_direction,
                            movement_speed):
        if tuple_result_from_pathfinding[0] != 0:
            if tuple_result_from_pathfinding[0] > 0:
                self.robot.rotate(True, tuple_result_from_pathfinding[0])
            else:
                self.robot.rotate(False, abs(tuple_result_from_pathfinding[0]))
            time.sleep(3)
        if tuple_result_from_pathfinding[1] != 0:
            self.robot.move_to(movement_direction, tuple_result_from_pathfinding[1], movement_speed)
            time.sleep(5)
        self.robot_angle_and_position.update_with_pathfinding_tuple(tuple_result_from_pathfinding)