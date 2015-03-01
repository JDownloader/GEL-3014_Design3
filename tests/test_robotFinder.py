from unittest import TestCase
from sample.robotFinder import RobotFinder


class TestRobotFinder(TestCase):
    ROBOT_MAC = RobotFinder.ROBOT_MAC
    FAKE_ROBOT_IP = "192.168.0.10"
    lines_of_arp_exit = "? (10.248.0.1) at 0:0:c:7:ac:a on en1 ifscope [ethernet]\n"+ \
                        "? (" + FAKE_ROBOT_IP + ") at " + ROBOT_MAC + " on en1 ifscope [ethernet]\n" + \
                        "? (169.254.255.255) at 0:0:c:7:ac:a on en1 [ethernet]"

    def pass_function(self):
        pass

    def setUp(self):
        self.robot_finder = RobotFinder(self.pass_function)

    def test_attempt_find(self):
        self.robot_finder._attempt_find()
        self.assertTrue(True)

    def test_attempt_parse_real(self):
        ip = self.robot_finder._parse_answer(self.lines_of_arp_exit)
        assert(ip, self.FAKE_ROBOT_IP)