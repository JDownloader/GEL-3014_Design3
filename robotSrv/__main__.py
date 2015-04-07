import os
from flask import Flask, abort, redirect, url_for, jsonify, request
import requests
import constants as cte
import json

SERVER_PORT = 8001


class RobotServer(Flask):
    base_station_ip_address = ''

    def __init__(self, *args, **kwargs):
        super(RobotServer, self).__init__(*args, **kwargs)

    def set_robot_ip_address(self, ip):
        self.base_station_ip_address = ip

app = RobotServer(__name__)
app.config.from_object(__name__)

def root_dir():
    return os.path.abspath(os.path.dirname(__file__))

def get_robot_position_from_base_station():
    response = requests.get(app.base_station_ip_address + cte.GET_ROBOT_POSITION_URL)
    return json.loads(response.text)['position']

@app.route('/')
def start():
    get_robot_position_from_base_station()
    return 'ok'

@app.route('/basestationip', methods=['POST'])
def recieve_base_stationIP():
    if request.method == 'POST':
        # app.base_station_ip_address = request.form.get('ip', None)
        app.base_station_ip_address = 'http://127.0.0.1:8000/'
    return 'ok'


if __name__ == '__main__':  # pragma: no cover
    app.run(host='0.0.0.0', port=SERVER_PORT, use_reloader=False)