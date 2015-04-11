import os.path
from flask import Flask, abort, redirect, url_for, jsonify, request
from contextProvider import ContextProvider
from robotIPFinder import RobotFinder
from vision.robotLocator import RobotLocator
import requests
import json
from vision.kinect import Kinect
import constants as cte
from questionanswering.question_processor import QuestionProcessor
from baseStation import BaseStation
import flagProcessor
from tests.test_vision_kinect import FakeKinect

SERVER_PORT = 8000


class BaseStationServer(Flask):
    robot_ip_address = RobotFinder.IP_NOT_FOUND

    def __init__(self, *args, **kwargs):
        super(BaseStationServer, self).__init__(*args, **kwargs)
        self.base_station = BaseStation()
        self.context_provider = ContextProvider(self.base_station)
        self.robot_locator = RobotLocator()
    def set_robot_ip_address(self, ip):
        print ip
        self.robot_ip_address = ip

app = BaseStationServer(__name__)
app.config.from_object(__name__)
# since it will only be use by software engineer, debug on is ok
app.debug = True
thread_robot_finder = RobotFinder(app.set_robot_ip_address)
thread_robot_finder.start()
# app.set_robot_ip_address('127.0.0.1')


def root_dir():
    return os.path.abspath(os.path.dirname(__file__))

@app.route('/')
def hello():
    return redirect(url_for('static', filename='index.html'))

@app.route('/start')
def start():
    if app.robot_ip_address == RobotFinder.IP_NOT_FOUND:
        abort(500)
    else:
        data = {'ip': app.robot_ip_address}
        response = requests.post('http://' + app.robot_ip_address + ':8001' + '/basestationip', data=data)
    return 'ok'


@app.route('/robotposition')
def fetch_robot_position():
    position = app.robot_locator.get_position(app.base_station.kinect)
    app.base_station.robot_position = position
    return jsonify(angle=position.get_angle_in_deg(),
                   position=(position.position[0], position.position[1]))
    # return jsonify(angle = '10', position = '(10,10)')

@app.route('/cubeposition', methods=['POST'])
def fetch_cube_position():
    cube_position = (-500, -500)
    if request.method == 'POST':
        color = request.form.get('color', None)
        app.base_station.cube_finder.refresh_position()
        for cube in app.base_station.cube_finder.cubes:
            if cube.color == color:
                cube_position = cube.position
                break
    return jsonify(position_x=cube_position[0] , position_y=cube_position[1])

@app.route('/path', methods=['POST'])
def receive_path():
    if request.method == 'POST':
        print 'Next path: '
        print request.form.get('path', None)

@app.route('/flag')
def fetch_flag():
    flag = ''
    for cycle in xrange(cte.NUMBER_OF_WRONG_ANSWER_ALLOWED):
        question = fetch_question()
        print question
        answer = fetch_answer(question)
        if is_right_answer(answer):
            app.base_station.change_question(question, answer)
            flag_processor = flagProcessor.FlagProcessor(answer)
            flag = flag_processor.get_flag()
            print flag
            break
    return jsonify(flag=flag)

# A javaScript fonction calls this method every 250 ms
@app.route('/context')
def get_context():
    context = app.context_provider.get_context(app.robot_ip_address)
    return jsonify(context)

@app.route('/changerobotposition', methods=['POST'])
def change():
    if request.method == 'POST':
        position_x = request.form.get('position_x', None)
        position_y = request.form.get('position_y', None)
        angle = request.form.get('angle', None)
        app.base_station.change_robot_position(position_x, position_y, angle)
    return 'ok'

def fetch_question():
    question = ''
    for url in cte.ATLAS_WEB_SERVER_URLS:
        try:
            response = requests.get(url, verify=False, timeout=0.1)
            if response.status_code == 200:
                question = response.text
                break
        except Exception:
            pass
    return json.loads(question)['question']

def fetch_answer(question):
    print "question : " + question
    processor = QuestionProcessor()
    processor.answer_question(question)
    return processor.answer

def is_right_answer(answer):
    print answer
    answer_is_good = raw_input('Is this the right answer ? (y/n) : ')
    if answer_is_good[0] is 'y':
        return True
    else:
        print 'Will retry...'
        return False

if __name__ == '__main__':  # pragma: no cover
    app.run(host='0.0.0.0', port=SERVER_PORT, use_reloader=False, threaded=False)
    thread_robot_finder.stop()