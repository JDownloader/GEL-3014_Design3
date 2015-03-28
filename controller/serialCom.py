__author__ = 'Gabriel'


import serial
from serial.tools.list_ports import comports
import controller.constants
import maestro


class BadMovementDirection(Exception):
    def __init__(self):
        pass


class LedController:
    COLORS_FOR_CONTROLLER = {'red': 'R',
                             'blue': 'B',
                             'green': 'G',
                             'yellow': 'Y',
                             'white': 'W',
                             'black': 'K',
                             'off': 'F'}

    def __init__(self):
        communication_port = ''
        for port in comports():
            if port[2].find('USB VID:PID=2341:003b') > -1:
                communication_port = port[0]
        if len(communication_port) > 0:
            self.serial_communication = serial.Serial(communication_port, 9600)

    def change_color(self, led_color='F', led_position=9):
        self.serial_communication.write(str(led_position) + led_color)
        print(str(led_position) + self.COLORS_FOR_CONTROLLER.get(led_color))

    def serial_communication_cleanup(self):
        self.serial_communication.close()


class CameraController:
    def __init__(self):
        communication_port = ''
        for port in comports():
            if port[2].find('VID:PID=1ffb:0089') > -1:
                communication_port = port[0]

        self.position_vertical = 0
        self.position_horizontal = 0
        self.channel_vertical = controller.constants.POLOLU_CHANNELS_PWM.get('camera_vertical')
        self.channel_horizontal = controller.constants.POLOLU_CHANNELS_PWM.get('camera_horizontal')
        if len(communication_port) > 0:
            self.camera_controller = maestro.Controller(communication_port)
            self.reset_position()

    def reset_position(self):
        self.camera_controller.setTarget(self.channel_horizontal, self.position_horizontal)
        self.camera_controller.setTarget(self.channel_vertical, self.position_vertical)


class GripperController:
    def __init__(self):
        communication_port = ''
        for port in comports():
            if port[2].find('VID:PID=1ffb:0089') > -1:
                communication_port = port[0]

        self.channel_vertical = controller.constants.POLOLU_CHANNELS_PWM.get('gripper_vertical')
        self.channel_pliers = controller.constants.POLOLU_CHANNELS_PWM.get('gripper_pliers')
        self.min_vertical = 4*704.00
        self.max_vertical = 4*2096.00
        self.pos_vertical_transport_cube = 4*1785.00
        self.pos_vertical_table = 4*1264.75
        self.min_pliers = 4*454.25
        self.max_pliers = 4*2374.50
        self.pos_pliers_open_big = 4*2031.00
        self.pos_pliers_open_small = 4*1156.75
        self.pos_pliers_closed = 4*850.00
        if len(communication_port) > 0:
            self.gripper_controller = maestro.Controller(communication_port)
            self._set_parameters()

    def _set_parameters(self):
        self.gripper_controller.setRange(self.channel_vertical, self.min_vertical, self.max_vertical)
        self.gripper_controller.setTarget(self.channel_vertical, self.pos_vertical_table)
        self.gripper_controller.setRange(self.channel_pliers, self.min_pliers, self.max_pliers)
        self.gripper_controller.setTarget(self.channel_pliers, self.pos_pliers_open_big)

    def change_vertical_position(self, is_raised):
        if is_raised:
            self.gripper_controller.setTarget(self.channel_vertical, self.pos_vertical_transport_cube)
        else:
            self.gripper_controller.setTarget(self.channel_vertical, self.pos_vertical_table)

    def pliers_control(self, is_opened, opening_is_big):
        if not is_opened:
            self.gripper_controller.setTarget(self.channel_pliers, self.pos_pliers_closed)
        elif is_opened and opening_is_big:
            self.gripper_controller.setTarget(self.channel_pliers, self.pos_pliers_open_big)
        elif is_opened and not opening_is_big:
            self.gripper_controller.setTarget(self.channel_pliers, self.pos_pliers_open_small)


class RobotMovementController:
    ARDUINO_SERIAL_DIRECTION_STRING = {'forward': 1,
                                       'right': 2,
                                       'reverse': 3,
                                       'left': 4}

    def __init__(self):
        communication_port = ''
        for port in comports():
            if port[2].find('USB VID:PID=2341:003d') > -1:
                communication_port = port[0]
        if len(communication_port) > 0:
            self.serial_communication = serial.Serial(communication_port, 9600)

    def move_robot(self, direction, distance_in_mm, speed_percentage):
        try:
            self.serial_communication.write(str(chr(self.ARDUINO_SERIAL_DIRECTION_STRING.get(direction))))
        except Exception:
            raise BadMovementDirection()
        self.serial_communication.write(str(chr(speed_percentage)))
        self.serial_communication.write(str(chr(int(distance_in_mm / 10))))

    def rotate_robot(self, rotation_direction_is_left, rotation_angle_in_degrees, speed_percentage):
        rotation_angle_in_steps = int(rotation_angle_in_degrees * 109 / 90)
        if rotation_direction_is_left:
            self.serial_communication.write(str(chr(101)))
        else:
            self.serial_communication.write(str(chr(102)))
        self.serial_communication.write(str(chr(speed_percentage)))
        self.serial_communication.write(str(chr(rotation_angle_in_steps)))

    def serial_communication_cleanup(self):
        self.serial_communication.close()


class Robot:
    def __init__(self):
        self.led_controller = LedController()
        self.camera_controller = CameraController()
        self.gripper_controller = GripperController()
        self.movement_controller = RobotMovementController()