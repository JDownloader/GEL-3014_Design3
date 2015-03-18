import socket
from robotSrv.__main__ import SERVER_PORT
from robotSrv.robotCommands import MoveXCommand
import cPickle


class RobotConnection():
    def __init__(self, ip_address):
        self.my_socket = socket.socket()
        self.my_socket.connect((ip_address, SERVER_PORT))

    def send_move_command(self):
        self.my_socket.send(cPickle.dumps(MoveXCommand(2)))

    def stop(self):
        self.my_socket.close()