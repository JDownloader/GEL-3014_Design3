import random
from tests.test_vision_kinect import FakeKinect
from time import gmtime, strftime
from vision.robotLocator import RobotPosition


class ContextProvider:
    def __init__(self, base_station):
        self.base_station = base_station
        self.set_path([])
        # self.last_known_positions = [[438, 140], [1000, 1200]]
        self.last_known_positions = list()

    def _get_current_flag(self):
        if self.base_station.flag is not None:
            return self.base_station.flag.get_matrix_for_ui()
        return ''

    def get_context(self, robot_ip):
        self.base_station.cube_finder.refresh_position()
        position = self.get_position_data()
        sample_status = { 'top': position.position[1],
                          'left': position.position[0],
                          'angle': 360 - position.get_angle_in_deg(),
                          'kinect_is_fake': self.is_fake_kinect(),
                          'path': self.path,
                          'last_known_positions': self.convert_known_positions(self.last_known_positions),
                          # 'chrono': strftime('%Mm%Ss', gmtime(tim)),
                          'chrono': '',
                          'robotIP': robot_ip,
                          'question': self.base_station.question,
                          'answer': self.base_station.answer,
                          'flag': self._get_current_flag(),
                          'cubes': self.get_cubes_data()}
        return sample_status

    def get_cubes_data(self):
        cubes_positions = []
        for cube in self.base_station.cube_finder.cubes:
            cubes_positions.append([cube.position[0], cube.position[1], cube.color])
        return cubes_positions

    def is_fake_kinect(self):
        if isinstance(self.base_station.kinect, FakeKinect):
            return True
        return False

    def get_position_data(self):
        position = RobotPosition()
        position.position = (-500, -500)
        position.angle = 0
        if self.base_station.robot_position is not None:
            if self.base_station.robot_position.position is not None \
                    and self.base_station.robot_position.angle is not None:
                real_robot_position = self.base_station.robot_position
                position = RobotPosition(real_robot_position.position[0], real_robot_position.position[1], real_robot_position.angle)
                position.position = self.convert_position(position.position)
        return position

    def convert_x_position(self, x):
        if x is None:
            return -500
        return int(float(302)-float(x)*float(0.27))

    def convert_y_position(self, y):
        if y is None:
            return -500
        return int(float(600)-float(y)*float(0.27))

    def convert_position(self, position):
        return [self.convert_x_position(position[0]), self.convert_y_position(position[1])]

    def set_path(self, path):
        new_path = []
        new_path.append(self.get_position_data().position)
        for move in path:
            new_move = self.convert_position(move)
            new_path.append(new_move)
        self.path = new_path

    def convert_known_positions(self, positions):
        new_positions = []
        for position in positions:
            new_position = self.convert_position(position)
            new_positions.append(new_position)
        return new_positions

    def add_known_position(self, position):
        self.last_known_positions.append(position)
        if self.last_known_positions.__len__() > 10:
            self.last_known_positions.pop(0)