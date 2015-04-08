import random
from tests.test_vision_kinect import FakeKinect
from time import gmtime, strftime
from vision.robotLocator import RobotPosition


class ContextProvider:
    def __init__(self, base_station):
        self.base_station = base_station

    def _get_current_flag(self):
        return self.base_station.flag.get_matrix_for_ui()

    def get_context(self, robot_ip):
        self.base_station.cube_finder.refresh_position()
        pos_y = random.randrange(0, 400, 10)
        angle = random.randrange(0, 359, 45)
        position = RobotPosition(0, pos_y, angle)
        sample_status = { 'top': 600-position.position[1]*0.27,
                          'left': 302-position.position[0]*0.27,
                          'angle': 360 - position.get_angle_in_deg(),
                          'kinect_is_fake': self.is_fake_kinect(),
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
        pass
        # position = RobotPosition()
        # position.position = (-500, -500)
        # position.angle = 0
        # if self.run_loop.robot_status is not None \
        #         and self.run_loop.robot_status.position.angle is not None:
        #     position = self.run_loop.robot_status.position
        # return position
