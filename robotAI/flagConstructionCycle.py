import time
from pathfinding.pathfinding import Pathfinding
import pathfinding.constants
import math


class FlagConstructionCycle:

    def flag_construction_sequence(self, flag_matrix, robot):
        for cube_index, cube in enumerate(self.flag_matrix):
            if cube is not None:
                self.fetch_cube(str(cube), cube_index)

    def fetch_cube(self, cube_color, cube_position_in_flag):
        movement_processor = MovementProcessor(self.robot_connection)
        self.robot_connection.send_led_color_change_command(cube_color, cube_position_in_flag)
        pathfind_to_wait_position_tuple = self.pathfinder.find_path_to_point(self.robot_status.position,
                                                                      pathfinding.constants.SAFE_POINT)
        movement_processor.move(pathfind_to_wait_position_tuple, self.robot_status.position,
                                                       movement_speed=75)

        target_cube = Cube(cube_color)
        self.cube_finder.add_cube(target_cube)
        self.cube_finder.refresh_position()
        self.cube_finder.refresh_position()
        self.cube_finder.refresh_position()
        pathfind_tuple_to_cube = self.pathfinder.find_path_to_point(self.robot_status.position,
                                                                   target_cube.position)
        movement_processor.move(pathfind_tuple_to_cube, self.robot_status.position, movement_speed=75)
        self.robot_connection.send_change_gripper_height_command(False)
        time.sleep(2)
        self.robot_connection.send_change_gripper_height_command(True)
        time.sleep(1)
        pathfind_tuple_pre_drop_point = self.pathfinder.find_path_to_point(self.robot_status.position,
                                                                          pathfinding.constants.DOCK_POINT)
        movement_processor.move(pathfind_tuple_pre_drop_point, self.robot_status.position,
                                                       movement_speed=75)
        pathfind_tuple_to_drop_angle = (self.pathfinder.determine_rotation_angle(math.degrees(self.robot_status.position.angle), 180),
                                        0)
        movement_processor.move(pathfind_tuple_to_drop_angle, self.robot_status.position)
        movement_processor.move((0, 200), self.robot_status.position, movement_speed=75)
        self.robot_connection.send_change_gripper_height_command(False)