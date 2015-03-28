import socket
from socket import AF_INET, SOCK_STREAM
from robotSrv.__main__ import SERVER_PORT
from robotSrv.robotCommands import MoveRobotCommand
import cPickle


class RobotConnection():
    def __init__(self, ip_address):
        self.my_socket = socket.socket(AF_INET, SOCK_STREAM)
        self.my_socket.connect((ip_address, SERVER_PORT))

    def send_move_command(self, direction, distance_in_mm, speed_percentage):
        self.my_socket.send(cPickle.dumps(MoveRobotCommand(direction, distance_in_mm, speed_percentage)))
        # if str(x) != '0':
        #     self.my_socket.send(cPickle.dumps(MoveXCommand(x)))
        # if str(y) != '0':
        #     self.my_socket.send(cPickle.dumps(MoveYCommand(y)))
        pass
    def stop(self):
        self.my_socket.close()