import os
from flask import Flask, abort, redirect, url_for, jsonify

SERVER_PORT = 8001


class RobotServer(Flask):
    base_station_ip_address = ''

    def __init__(self, *args, **kwargs):
        super(RobotServer, self).__init__(*args, **kwargs)
        self.base_station_connection = None

    def set_robot_ip_address(self, ip):
        self.base_station_ip_address = ip

app = RobotServer(__name__)
app.config.from_object(__name__)

def root_dir():
    return os.path.abspath(os.path.dirname(__file__))

@app.route('/')
def start():
    return 'ok'


if __name__ == '__main__':  # pragma: no cover
    app.run(port=SERVER_PORT, use_reloader=False)