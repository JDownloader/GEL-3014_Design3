import socket
from socket import AF_INET, SOCK_STREAM
from robotSrv.__main__ import SERVER_PORT
from robotSrv.robotCommands import MoveXCommand, MoveYCommand
import cPickle


class RobotConnection():
    def __init__(self, ip_address):
        self.my_socket = socket.socket(AF_INET, SOCK_STREAM)
        self.my_socket.connect((ip_address, SERVER_PORT))

    def send_move_command(self, x, y):
        if str(x) != '0':
            self.my_socket.send(cPickle.dumps(MoveXCommand(x)))
        if str(y) != '0':
            self.my_socket.send(cPickle.dumps(MoveYCommand(y)))

    def stop(self):
        self.my_socket.close()