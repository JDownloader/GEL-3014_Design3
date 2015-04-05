import time

class MovementProcessor:
    def __init__(self, robot_connection):
        self.robot_connection = robot_connection

    def move_to(self, pathfinding_tuple, robot_angle_and_position, movement_direction='forward',
                                    movement_speed=100):
        if pathfinding_tuple[0] != 0:
            if pathfinding_tuple[0] > 0:
                self.robot_connection.send_rotate_robot_command(True, pathfinding_tuple[0])
            else:
                self.robot_connection.send_rotate_robot_command(False, abs(pathfinding_tuple[0]))
        if pathfinding_tuple[1] != 0:
            time.sleep(2)
            self.robot_connection.send_move_robot_command(movement_direction, pathfinding_tuple[1], movement_speed)

        robot_angle_and_position.update_with_pathfinding_tuple(pathfinding_tuple)