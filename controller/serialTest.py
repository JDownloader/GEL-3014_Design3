import serial
from serialCom import LedController, RobotMovementController
import time

# led_controller = LedController()
# time.sleep(2)
#
# led_controller.change_color('red', 9)
# wait = raw_input()

mvt_controller = RobotMovementController()
time.sleep(1)
mvt_controller.rotate_robot(False, 1, True)
#mvt_controller.move_robot('reverse', 10)
#mvt_controller.move_robot('right', 30)
#mvt_controller.rotate_robot(False, 80, False)
#mvt_controller.rotate_robot(True, 3, True)
#mvt_controller.rotate_robot(False, 90, True)


