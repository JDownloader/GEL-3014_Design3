

class RobotCommand():
    def __init__(self):
        pass

    def perform_command(self, robot):
        pass


class LedColorCommand(RobotCommand):
    def __init__(self, led_color, led_pos):
        self.led_color = led_color
        self.led_pos = led_pos

    def perform_command(self, robot):
        robot.led_controller.change_color(self.led_color, self.led_pos)


class LedSerialCommunicationCleanupCommand(RobotCommand):
    def __init__(self):
        pass

    def perform_command(self, robot):
        robot.led_controller.serial_communication_cleanup()


class CameraResetPositionCommand(RobotCommand):
    def __init__(self):
        pass

    def perform_command(self, robot):
        robot.camera_controller.reset_position()


class GripperChangeVerticalPositionCommand(RobotCommand):
    def __init__(self, is_raised):
        self.is_raised = is_raised

    def perform_command(self, robot):
        robot.gripper_controller.change_vertical_position(self.is_raised)


class GripperPliersOpeningCommand(RobotCommand):
    def __init__(self, is_opened, opening_is_big):
        self.is_opened = is_opened
        self.opening_is_big = opening_is_big

    def perform_command(self, robot):
        robot.gripper_controller.pliers_control(self.is_opened, self.opening_is_big)


class MoveRobotCommand(RobotCommand):
    def __init__(self, direction, distance_in_mm, speed_percentage):
        self.direction = direction
        self.distance_in_mm = distance_in_mm
        self.speed_percentage = speed_percentage

    def perform_command(self, robot):
        robot.movement_controller.move_robot(self.direction, self.distance_in_mm, self.speed_percentage)


class RotateRobotCommand(RobotCommand):
    def __init__(self, rotation_direction_is_left, rotation_angle_in_degrees, speed_percentage):
        self.rotation_direction_is_left = rotation_direction_is_left
        self.rotation_angle_in_degrees = rotation_angle_in_degrees
        self.speed_percentage = speed_percentage

    def perform_command(self, robot):
        robot.movement_controller.rotate_robot(self.rotation_direction_is_left, self.rotation_angle_in_degrees,
                                               self.speed_percentage)

class RobotMovementSerialCommunicationCleanupCommand(RobotCommand):
    def __init__(self):
        pass

    def perform_command(self, robot):
        robot.movement_controller.serial_communication_cleanup()