from serialCom import GripperController, PololuConnectionCreator, CameraController, LedController, RobotMovementController
import time

# pololu_com = PololuConnectionCreator()
# time.sleep(0.5)
# gripper = GripperController(pololu_com.pololu_serial_communication)
# while True:
#     print 'gripper lvl'
#     lvl = int(raw_input())
#     gripper.change_vertical_position(lvl)
#     print 'pince lvl'
#     lvl = int(raw_input())
#     gripper.pliers_control(lvl)


# camera = CameraController(pololu_com.pololu_serial_communication)

# led_ctrl = LedController()
# time.sleep(2)
# while True:
#     print 'pos'
#     pos = int(raw_input())
#     print 'color'
#     color = raw_input()
#     led_ctrl.change_color(color, pos)
led_ctrl = LedController()
mvt_contrl = RobotMovementController()
time.sleep(2)
led_ctrl.change_color('red', 3)
while True:
    mvt_contrl.move_robot('forward', 20)
    mvt_contrl.move_robot('left', 20)
    mvt_contrl.move_robot('reverse', 20)
    mvt_contrl.move_robot('right', 20)