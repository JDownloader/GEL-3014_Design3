import os.path
from flask import Flask, abort, redirect, url_for, jsonify
from robotIPFinder import RobotFinder
from runLoop import RunLoop
from vision.robotLocator import RobotLocator
import requests
import json
from tests.test_vision_kinect import FakeKinect

SERVER_PORT = 8000


class BaseStationServer(Flask):
    robot_ip_address = 'http://127.0.0.1:8001/'
    # robot_ip_address = 'http://10.248.177.53:8001/'
    # robot_ip_address = RobotFinder.IP_NOT_FOUND

    def __init__(self, *args, **kwargs):
        super(BaseStationServer, self).__init__(*args, **kwargs)
        self.run_loop = RunLoop()
        self.robot_connection = None

    def set_robot_ip_address(self, ip):
        self.robot_ip_address = ip
        # self.robot_connection = RobotConnection(self.robot_ip_address)

app = BaseStationServer(__name__)
app.config.from_object(__name__)
# since it will only be use by software engineer, debug on is ok
app.debug = True
# thread_robot_finder = RobotFinder(app.set_robot_ip_address)
# thread_robot_finder.start()


def root_dir():
    return os.path.abspath(os.path.dirname(__file__))

@app.route('/')
def hello():
    return redirect(url_for('static', filename='index.html'))

@app.route('/start')
def start():
    data = {'ip':'10.248.177.53'}
    response = requests.post(app.robot_ip_address + 'basestationip', data=data)
    return 'ok'



@app.route('/robotposition')
def fetchRobotPosition():
    robotLocator = RobotLocator()
    # return str(robotLocator.get_position(FakeKinect()))
    return jsonify(angle = '10', position = '(10,10)')

@app.route('/flag')
def fetchFlag():
    return jsonify(angle = '10', position = '(10,10)')


# A javaScript fonction calls this method every 250 ms
@app.route('/context')
def get_context():
    sample_context = app.run_loop.get_context(app.robot_ip_address)
    return jsonify(sample_context)


if __name__ == '__main__':  # pragma: no cover
    app.run(host='0.0.0.0',port=SERVER_PORT, use_reloader=False)
    # thread_robot_finder.stop()