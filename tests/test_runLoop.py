from unittest import TestCase
from baseStation.runLoop import RunLoop


class TestRunLoop(TestCase):
    def setUp(self):
        self.empty_run_loop = RunLoop()
        self.stated_run_loop = RunLoop()
        self.stated_run_loop.start_timer()

    def test_new_should_not_return_time(self):
        self.assertEqual(0, self.empty_run_loop.get_time())

    def test_time_is_not_zero_when_started(self):
        time = self.stated_run_loop.get_time()
        if time < 0:
            self.fail()