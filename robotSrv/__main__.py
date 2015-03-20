import socket
from socket import AF_INET, SOCK_STREAM
from robotCommands import RobotCommand
import cPickle

SERVER_PORT = 8001


class RobotSocket():
    MAX_CONNECTION = 1
    HOST = '0.0.0.0'

    def __init__(self, port):
        self.server_available = True
        self.connection_available = True
        self.my_socket = socket.socket(AF_INET, SOCK_STREAM)
        self.my_socket.bind((self.HOST, port))

    def connection_stopped(self):
        self.connection_available = False

    def start_listen_loop(self):
        self.my_socket.listen(self.MAX_CONNECTION)
        while self.server_available:
            my_connection, addr = self.my_socket.accept()
            print 'Got connection from', addr
            self.listen_connection_loop(my_connection)
        my_connection.close()
        self.my_socket.close()

    def listen_connection_loop(self, my_connection):
        while self.connection_available:
            msg = my_connection.recv(1024)
            if not msg:
                self.connection_available = False
                self.server_available = False
            else:
                command = cPickle.loads(msg)
                command.perform_command(None)


if __name__ == '__main__':
    my_socket = RobotSocket(SERVER_PORT)
    my_socket.start_listen_loop()

