import random
from tests.test_vision import FakeKinect
from time import gmtime, strftime


class ContextHelper:
    def __init__(self, run_loop):
        self.run_loop = run_loop

    def _get_current_flag(self):
        return self.run_loop.flag_loop.get_flag()

    def get_context(self, robot_ip):
        pos_y = random.randrange(0, 400, 1)
        run_time = self.run_loop.get_time()
        sample_status = { 'top': 30,
                          'left': pos_y,
                          'kinect_is_fake': self.is_fake_kinect(),
                          'chrono': strftime('%Mm%Ss', gmtime(run_time)),
                          'robotIP': robot_ip,
                          'flag': self._get_current_flag(),
                          'cubes': self.get_cubes_data()}
        return sample_status

    def get_cubes_data(self):
        cubes_positions = []
        for cube in self.run_loop.cube_finder.cubes:
            cubes_positions.append([cube.position[0], cube.position[1], cube.color])
        return cubes_positions

    def is_fake_kinect(self):
        if isinstance(self.run_loop.kinect, FakeKinect):
            return True
        return False