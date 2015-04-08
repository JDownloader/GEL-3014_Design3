import random
from tests.test_vision_kinect import FakeKinect
from time import gmtime, strftime
from vision.robotLocator import RobotPosition


class ContextProvider:
    def __init__(self, base_station):
        self.base_station = base_station

    def _get_current_flag(self):
        pass
        # return self.run_loop.flag_loop.get_flag()

    def get_context(self, robot_ip):
        self.base_station.cube_finder.refresh_position()
        pos_y = random.randrange(0, 400, 1)
        angle = random.randrange(0, 359, 45)
        # run_time = self.run_loop.get_time()
        # position = self.get_position_data()
        # sample_status = { 'robotIP': robot_ip,
        #                   'flag': self._get_current_flag(),
        #                   'cubes': self.get_cubes_data()}
        position = RobotPosition(0,0,0)
        sample_status = { 'top': 600-position.position[1]*0.27,
                          'left': 302-position.position[0]*0.27,
                          'angle': 360 - position.get_angle_in_deg(),
                          'kinect_is_fake': self.is_fake_kinect(),
                          # 'chrono': strftime('%Mm%Ss', gmtime(tim)),
                          'chrono': '',
                          'robotIP': robot_ip,
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
