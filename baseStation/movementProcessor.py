import time


class MovementProcessor:
    def __init__(self, robot_connection):
        self.robot_connection = robot_connection

    def physical_movement_processor(self, pathfinding_tuple, movement_direction='forward', movement_speed=100):
        if pathfinding_tuple[0] != 0:
            if pathfinding_tuple[0] > 0:
                self.robot_connection.send_rotate_robot_command(False, pathfinding_tuple[0])
            else:
                self.robot_connection.send_rotate_robot_command(True, abs(pathfinding_tuple[0]))
            time.sleep(5)
        if pathfinding_tuple[1] != 0:
            time.sleep(2)
            self.robot_connection.send_move_robot_command(movement_direction, pathfinding_tuple[1], movement_speed)
            time.sleep(5)