import time
from robotConnection import RobotConnection
from pathfinding.pathfinding import Pathfinding
from movementProcessor import MovementProcessor
import pathfinding.constants
from cubeFinder import CubeFinder
from vision.cube import Cube


class FlagCycle:
    def __init__(self, flag_matrix, robot_status, kinect):
        self.flag_matrix = flag_matrix
        self.robot_status = robot_status
        self.robot_connection = robot_status.robot_connection
        self.pathfinder = Pathfinding()
        self.cube_finder = CubeFinder(kinect)

    def start(self):
        for cube_index, cube in enumerate(self.flag_matrix):
            if cube is not None:
                self.fetch_cube(str(cube), cube_index)

    def fetch_cube(self, cube_color, cube_position_in_flag):
        movement_processor = MovementProcessor(self.robot_connection)
        self.robot_connection.send_led_color_change_command(cube_color, cube_position_in_flag)
        pathfind_to_wait_position_tuple = self.pathfinder.pathfind_to_point(self.robot_status.position,
                                                                      pathfinding.constants.WAIT_ZONE)
        print pathfind_to_wait_position_tuple
        movement_processor.physical_movement_processor(pathfind_to_wait_position_tuple, self.robot_status.position,
                                                       movement_speed=75)

        target_cube = Cube(cube_color)
        self.cube_finder.add_cube(target_cube)
        self.cube_finder.refresh_position()
        self.cube_finder.refresh_position()
        self.cube_finder.refresh_position()
        print target_cube.position
        pathfind_tuple_to_cube = self.pathfinder.pathfind_to_cube_buffer_zone(self.robot_status.position,
                                                                   target_cube.position)
        movement_processor.physical_movement_processor(pathfind_tuple_to_cube, self.robot_status.position, movement_speed=75)
        self.robot_connection.send_change_gripper_height_command(False)
        wait = raw_input()
        self.robot_connection.send_change_gripper_height_command(True)
        time.sleep(1)
        pathfind_tuple_pre_drop_point = self.pathfinder.pathfind_to_point(self.robot_status.position,
                                                                          pathfinding.constants.PRE_DROP_POINT)
        movement_processor.physical_movement_processor(pathfind_tuple_pre_drop_point, self.robot_status.position,
                                                       movement_speed=75)
        print self.robot_status.position.angle
        pathfind_tuple_to_drop_angle = (self.pathfinder.determine_rotation_angle(self.robot_status.position.angle, 180),
                                        0)
        print pathfind_tuple_to_drop_angle[0]
        movement_processor.physical_movement_processor(pathfind_tuple_to_drop_angle, self.robot_status.position)
        movement_processor.physical_movement_processor((0, 200), self.robot_status.position, movement_speed=75)
        self.robot_connection.send_change_gripper_height_command(False)