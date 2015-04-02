import socket
from socket import AF_INET, SOCK_STREAM
from robotSrv.__main__ import SERVER_PORT
from robotSrv.robotCommands import *
import cPickle


class RobotConnection():
    def __init__(self, ip_address):
        self.robot_socket = socket.socket(AF_INET, SOCK_STREAM)
        self.robot_socket.connect((ip_address, SERVER_PORT))

    def send_command(self, command):
        print command
        print cPickle.loads(cPickle.dumps(command))
        self.robot_socket.send(cPickle.dumps(command))

    def send_move_command(self, x, y):
        if str(x) != '0':
            self.send_command(MoveXCommand(x))
        if str(y) != '0':
            self.send_command(MoveXCommand(y))

    def send_led_color_change_command(self, led_color, led_position):

        self.send_command(LedColorCommand(led_color, led_position))

    def send_led_serial_communication_cleanup_command(self):
        self.send_command(LedSerialCommunicationCleanupCommand())

    def send_camera_reset_position_command(self):
        self.send_command(CameraResetPositionCommand())

    def send_change_gripper_height_command(self, is_raised):
        self.send_command(GripperChangeVerticalPositionCommand(is_raised))

    def send_gripper_pliers_opening_change_command(self, is_opened, opening_is_big):
        self.send_command(GripperPliersOpeningCommand(is_opened, opening_is_big))

    def send_move_robot_command(self, direction, distance_in_mm, speed_percentage):
        self.send_command(MoveRobotCommand(direction, distance_in_mm, speed_percentage))

    def send_rotate_robot_command(self, rotation_direction_is_left, rotation_angle_in_degrees, speed_percentage=50):
        self.send_command(RotateRobotCommand(rotation_direction_is_left, rotation_angle_in_degrees, speed_percentage))

    def send_robot_movement_serial_communication_cleanup_command(self):
        self.send_command(RobotMovementSerialCommunicationCleanupCommand())

    def stop(self):
        self.robot_socket.close()