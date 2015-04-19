from robot.robotAI import RobotAI
import time

robot = RobotAI(None)
robot.robot_angle_and_position.angle=0
robot.robot_angle_and_position.position = (1000, 1000)
robot.move_robot_to_pickup_cube('white')
robot.pickup_cube()
time.sleep(4)