import time
from robotConnection import RobotConnection
from pathfinding.pathfinding import Pathfinding


class FlagCycle:
    def __init__(self, flag_matrix, robot_connection):
        self.flag_matrix = flag_matrix
        self.robot_connection = robot_connection
        self.pathfinder = Pathfinding()

    def start(self):
        for cube_index, cube in enumerate(self.flag_matrix):
            if cube is not None:
                pass
        self.fetch_cube(str('yellow'), 4)

    def fetch_cube(self, cube_color, cube_position_in_flag):
        print 'je fais semblant que je suis arrive au cube'
        self.robot_connection.send_led_color_change_command(cube_color, cube_position_in_flag)
        self.robot_connection.send_gripper_pliers_opening_change_command(True, True)
        time.sleep(1)
        self.robot_connection.send_change_gripper_height_command(False)
        time.sleep(2)
        self.robot_connection.send_gripper_pliers_opening_change_command(True, False)
        time.sleep(1)
        self.robot_connection.send_gripper_pliers_opening_change_command(False, False)
        time.sleep(2)
        self.robot_connection.send_change_gripper_height_command(True)