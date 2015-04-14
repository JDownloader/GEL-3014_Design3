from serialCom import GripperController, PololuConnectionCreator, CameraController, LedController, RobotMovementController
import time
import numpy

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

# led_ctrl = LedController()
# mvt_contrl = RobotMovementController()
# time.sleep(2)
# led_ctrl.change_color('red', 3)
# while True:
#     mvt_contrl.move_robot('forward', 20)
#     mvt_contrl.move_robot('left', 20)
#     mvt_contrl.move_robot('reverse', 20)
#     mvt_contrl.move_robot('right', 20)
led_conrl = LedController()
time.sleep(2)

def tranpose_flag_matrix(flag_matrix):
    flag_matrix.pop()
    flag_matrix_without_none = []
    for cube in flag_matrix:
        if cube is None:
            flag_matrix_without_none.append('off')
        else:
            flag_matrix_without_none.append(cube)
    print flag_matrix_without_none
    flag_array = numpy.array(flag_matrix_without_none)
    print flag_array
    flag_array_reshaped = flag_array.reshape((3, 3))
    transposed_array = flag_array_reshaped.transpose()
    transposed_array[[0, 2],:] = transposed_array[[2, 0],:]
    reshaped_transposed_array = transposed_array.reshape((1, 9))
    transposed_flag_matrix = reshaped_transposed_array[0].tolist()
    return transposed_flag_matrix

flag = ["blue", "white", "red", "red", "white", "red", None, None, None, "white"]
transposed_flag = tranpose_flag_matrix(flag)
print transposed_flag
for index, cube in enumerate(transposed_flag):
    led_conrl.change_color(cube, index)
wait = raw_input()