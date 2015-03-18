

class RobotCommand():
    def perform_command(self, robot):
        pass


class MoveXCommand(RobotCommand):
    def __init__(self, value):
        self.value = value

    def perform_command(self, robot):
        print 'Move X: ' + str(self.value)


class MoveYCommand(RobotCommand):
    def __init__(self, value):
        self.value = value

    def perform_command(self, robot):
        print 'Move Y: ' + str(self.value)