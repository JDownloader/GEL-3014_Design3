import serial
from serialCom import LedController, RobotMovementController, CameraController, PololuConnectionCreator
from robotVision.visionRobot import  VisionRobot
import time

# led_controller = LedController()
# time.sleep(2)
#
# led_controller.change_color('red', 9)
# wait = raw_input()

mvt_controller = RobotMovementController()
# time.sleep(1)
# mvt_controller.serial_communication.flushInput()
# while True:
#     mvt_controller.move_robot('forward', 50)
#     mvt_controller.move_robot('reverse', 50)
#     mvt_controller.move_robot('left', 50)
#     mvt_controller.move_robot('right', 50)
#     mvt_controller.rotate_robot(True, 20, False)
#     mvt_controller.rotate_robot(False, 20, False)
# #mvt_controller.move_robot('reverse', 10)
#mvt_controller.move_robot('right', 30)
#mvt_controller.rotate_robot(False, 80, False)
#mvt_controller.rotate_robot(True, 3, True)
#mvt_controller.rotate_robot(False, 90, True)
patatepilleeee = VisionRobot("blue")
print patatepilleeee.find_cube_center()[0]
print patatepilleeee.find_cube_center()[1]

# while True:
#     print patatepilleeee.find_cube_center()[1]
while (patatepilleeee.find_cube_center()[0] < -10):
    #delta_center = patatepilleeee.find_cube_center()
    print patatepilleeee.find_cube_center()[0]
    mvt_controller.move_robot('right', 10)
mvt_controller.stop_all_movement()
while (patatepilleeee.find_cube_center()[0] > 10):
    print patatepilleeee.find_cube_center()[0]
    mvt_controller.move_robot('left', 10)
mvt_controller.stop_all_movement()
while patatepilleeee.find_cube_center()[1] > -173:
    #delta_center = patatepilleeee.find_cube_center()
    print patatepilleeee.find_cube_center()[1]
    mvt_controller.move_robot('forward', 10)
mvt_controller.stop_all_movement()
while patatepilleeee.find_cube_center()[1] > -160:
    #delta_center = patatepilleeee.find_cube_center()
    print patatepilleeee.find_cube_center()[1]
    mvt_controller.move_robot('forward', 10)
mvt_controller.stop_all_movement()
while patatepilleeee.find_cube_center()[1] > -160:
    #delta_center = patatepilleeee.find_cube_center()
    print patatepilleeee.find_cube_center()[1]
    mvt_controller.move_robot('reverse', 10)
mvt_controller.stop_all_movement()

while (patatepilleeee.find_cube_center()[0] < -10):
    #delta_center = patatepilleeee.find_cube_center()
    print patatepilleeee.find_cube_center()[0]
    mvt_controller.move_robot('right', 10)
mvt_controller.stop_all_movement()
while (patatepilleeee.find_cube_center()[0] > 10):
    print patatepilleeee.find_cube_center()[0]
    mvt_controller.move_robot('left', 10)
mvt_controller.stop_all_movement()
while patatepilleeee.find_cube_center()[1] > -160:
    #delta_center = patatepilleeee.find_cube_center()
    print patatepilleeee.find_cube_center()[1]
    mvt_controller.move_robot('forward', 10)
mvt_controller.stop_all_movement()
while patatepilleeee.find_cube_center()[1] < -160:
    #delta_center = patatepilleeee.find_cube_center()
    print patatepilleeee.find_cube_center()[1]
    mvt_controller.move_robot('reverse', 10)
mvt_controller.stop_all_movement()

while True:
    print patatepilleeee.find_cube_center()[1]
#pololu = PololuConnectionCreator()
#time.sleep(0.5)
#cam_contrl = CameraController(pololu.pololu_serial_communication)
