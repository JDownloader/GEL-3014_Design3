import serial
from serial.tools.list_ports import comports
import controller.constants
from maestro import Controller
import time


class BadMovementDirection(Exception):
    def __init__(self):
        pass


class PololuSerialConnectionFailed(Exception):
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
        self.serial_communication.write(str(led_position) + self.COLORS_FOR_CONTROLLER.get(led_color))


class PololuConnectionCreator:
    def __init__(self):
        self.pololu_serial_communication = ''
        pololu_communication_port = ''
        for port in comports():
            if port[2].find('VID:PID=1ffb:0089') > -1:
                pololu_communication_port = port[0]
        try:
            self.pololu_serial_communication = Controller(pololu_communication_port)
        except Exception:
            raise PololuSerialConnectionFailed()


class CameraController:
    def __init__(self, pololu_serial_communication):
        self.position_vertical = int(4 * 1047.5)
        self.position_horizontal = int(4 * 1550)
        self.channel_vertical = controller.constants.POLOLU_CHANNELS_PWM.get('camera_vertical')
        self.channel_horizontal = controller.constants.POLOLU_CHANNELS_PWM.get('camera_horizontal')
        self.reset_position(pololu_serial_communication)

    def reset_position(self, pololu_serial_communication):
        pololu_serial_communication.setTarget(self.channel_horizontal, self.position_horizontal)
        pololu_serial_communication.setTarget(self.channel_vertical, self.position_vertical)


class GripperController:
    def __init__(self, pololu_serial_communication):
        self.gripper_serial_communication = pololu_serial_communication
        self.channel_vertical = controller.constants.POLOLU_CHANNELS_PWM.get('gripper_vertical')
        self.channel_pliers = controller.constants.POLOLU_CHANNELS_PWM.get('gripper_pliers')
        self.min_vertical = int(4*704.00)
        self.max_vertical = int(4*2096.00)
        self.pos_vertical_transport_cube = int(4*1785.00)
        self.pos_vertical_table = int(4*1264.75)
        self.vertical_speed = 20
        self.min_pliers = int(4*454.25)
        self.max_pliers = int(4*2374.50)
        self.pos_pliers_open_big = int(4*2031.00)
        self.pos_pliers_open_small = int(4*1156.75)
        self.pos_pliers_closed = int(4*850.00)
        self.pliers_speed = 30
        self._set_parameters()

    def _set_parameters(self):
        if self.gripper_serial_communication:
            self.gripper_serial_communication.setRange(self.channel_vertical, self.min_vertical, self.max_vertical)
            self.gripper_serial_communication.setSpeed(self.channel_vertical, self.vertical_speed)
            self.gripper_serial_communication.setTarget(self.channel_vertical, self.pos_vertical_transport_cube)
            self.gripper_serial_communication.setRange(self.channel_pliers, self.min_pliers, self.max_pliers)
            self.gripper_serial_communication.setSpeed(self.channel_pliers, self.pliers_speed)
            self.gripper_serial_communication.setTarget(self.channel_pliers, self.pos_pliers_closed)

    def change_vertical_position(self, is_raised):
        if is_raised:
            self.gripper_serial_communication.setTarget(self.channel_vertical, self.pos_vertical_transport_cube)
        else:
            self.gripper_serial_communication.setTarget(self.channel_vertical, self.pos_vertical_table)
        while self.gripper_serial_communication.isMoving(self.channel_vertical):
            pass

    def pliers_control(self, is_opened, opening_is_big):
        if not is_opened:
            self.gripper_serial_communication.setTarget(self.channel_pliers, self.pos_pliers_closed)
        elif is_opened and opening_is_big:
            self.gripper_serial_communication.setTarget(self.channel_pliers, self.pos_pliers_open_big)
        elif is_opened and not opening_is_big:
            self.gripper_serial_communication.setTarget(self.channel_pliers, self.pos_pliers_open_small)
        while self.gripper_serial_communication.isMoving(self.channel_pliers):
            pass



class RobotMovementController:
    ARDUINO_SERIAL_DIRECTION_STRING = {'forward': 1,
                                       'right': 2,
                                       'reverse': 3,
                                       'left': 4}

    def __init__(self):
        communication_port = ''
        for port in comports():
            if port[2].find('USB VID:PID=2341:003d') > -1 or port[2].find('USB VID:PID=2a03:003d') > -1:
                communication_port = port[0]
        if len(communication_port) > 0:
            self.serial_communication = serial.Serial(communication_port, baudrate=9600, timeout=7)

    def move_robot(self, direction, distance_in_mm):
        distance_in_cm = int(round(distance_in_mm / 10))
        if distance_in_cm >= 40:
            speed_percentage = 75
        elif 25 < distance_in_cm <= 40:
            speed_percentage = 50
        elif 15 < distance_in_cm <= 25:
            speed_percentage = 30
        else:
            speed_percentage = 10
        try:
            self.serial_communication.write(str(chr(self.ARDUINO_SERIAL_DIRECTION_STRING.get(direction))))
        except Exception:
            raise BadMovementDirection()
        self.serial_communication.write(str(chr(speed_percentage)))
        self.serial_communication.write(str(chr(int(distance_in_cm))))
        self.serial_communication.flushInput()
        read = self.serial_communication.read(size=1)
        self.serial_communication.flushInput()

    def rotate_robot(self, rotation_direction_is_left, rotation_angle_in_degrees, rotation_speed_is_slow):
        if rotation_speed_is_slow:
            speed_percentage = 10
        else:
            speed_percentage = 25
        if rotation_direction_is_left:
            self.serial_communication.write(str(chr(101)))
        else:
            self.serial_communication.write(str(chr(102)))
        self.serial_communication.write(str(chr(speed_percentage)))
        self.serial_communication.write(str(chr(rotation_angle_in_degrees)))
        self.serial_communication.flushInput()
        read = self.serial_communication.read(size=1)
        self.serial_communication.flushInput()



    def stop_all_movement(self):
        self.serial_communication.write(str(chr(99)))
        self.serial_communication.write(str(chr(0)))
        self.serial_communication.write(str(chr(0)))


class Robot:
    def __init__(self):
        self._initialize_connections()
        try:
            self.pololu_serial_connection = PololuConnectionCreator()
        except PololuSerialConnectionFailed:
            print 'Polulu connection failed'
        else:
            self._initialize_pololu_connections(self.pololu_serial_connection)
        time.sleep(controller.constants.LED_COMMUNICATION_INITIALIZATION_WAIT_TIME)

    def _initialize_connections(self):
        self.movement_controller = RobotMovementController()
        self.led_controller = LedController()

    def _initialize_pololu_connections(self, pololu_connection):
        self.camera_controller = CameraController(pololu_connection.pololu_serial_communication)
        self.gripper_controller = GripperController(pololu_connection.pololu_serial_communication)

    def move(self, direction, distance_in_mm):
        self.movement_controller.move_robot(direction, distance_in_mm)

    def rotate(self, rotation_direction_is_left, rotation_angle_in_degrees, movement_speed_is_slow=False):
        self.movement_controller.rotate_robot(rotation_direction_is_left, int(round(rotation_angle_in_degrees)),
                                              movement_speed_is_slow)

    def move_gripper_vertically(self, wanted_position_is_raised):
        self.gripper_controller.change_vertical_position(wanted_position_is_raised)

    def change_pliers_opening(self, wanted_position_is_opened, opening_is_big=False):
        self.gripper_controller.pliers_control(wanted_position_is_opened, opening_is_big)

    def change_led_color(self, led_color, led_position):
        self.led_controller.change_color(str(led_color), int(led_position))

    def stop_movement(self):
        self.movement_controller.stop_all_movement()