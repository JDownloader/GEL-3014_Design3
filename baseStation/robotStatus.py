from vision.robotLocator import RobotLocator, RobotPosition


class RobotStatus:
    def __init__(self, robot_connection):
        self.robot_connection = robot_connection
        self.robot_locator = RobotLocator()
        self.position = RobotPosition()

    def update_position_with_kinect(self, kinect):
        self.position = self.robot_locator.get_position(kinect)