import os
from flask import Flask, abort, redirect, url_for, jsonify, request, after_this_request
import requests
import constants as cte
import json
from robot.baseStationClient import BaseStationClient
from robot.robotAI import RobotAI

SERVER_PORT = 8001


here = os.path.abspath(os.path.dirname(__file__))


class RobotServer(Flask):
    base_station_ip_address = ''

    def __init__(self, *args, **kwargs):
        super(RobotServer, self).__init__(*args, **kwargs)

    def set_robot_ip_address(self, ip):
        self.base_station_ip_address = ip

app = RobotServer(__name__)
app.config.from_object(__name__)
# since it will only be use by software engineer, debug on is ok
app.debug = True

@app.route('/')
def start():
    @after_this_request
    def rune_sequence_callback(response):
        robot = RobotAI(BaseStationClient(app))
        robot.run_sequence()
        return response
    # get_robot_position_from_base_station()
    return 'ok'

@app.route('/basestationip', methods=['POST'])
def recieve_base_stationIP():
    if request.method == 'POST':
        app.base_station_ip_address = request.form.get('ip', None)
    return 'ok'


if __name__ == '__main__':  # pragma: no cover
    app.run(host='0.0.0.0', port=SERVER_PORT, use_reloader=False)