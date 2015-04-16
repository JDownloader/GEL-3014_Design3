import os.path
from flask import Flask, abort, redirect, url_for, jsonify, request
from contextProvider import ContextProvider
from robotIPFinder import RobotFinder
from vision.robotLocator import RobotLocator
import requests
import json
from sound import play_prometheus, play_acquired
import constants as cte
from questionanswering.question_processor import QuestionProcessor
from baseStation import BaseStation
import flagProcessor
from tests.test_vision_kinect import FakeKinect
from flag import Flag
SERVER_PORT = 8000


class BaseStationServer(Flask):
    robot_ip_address = RobotFinder.IP_NOT_FOUND

    def __init__(self, *args, **kwargs):
        super(BaseStationServer, self).__init__(*args, **kwargs)
        self.base_station = BaseStation()
        self.context_provider = ContextProvider(self.base_station)
        self.robot_locator = RobotLocator()
        self.refresh_since_last_kinect_update = 999

    def set_robot_ip_address(self, ip):
        print ip
        self.robot_ip_address = ip

app = BaseStationServer(__name__)
app.config.from_object(__name__)
# since it will only be use by software engineer, debug on is ok
app.debug = True
thread_robot_finder = RobotFinder(app.set_robot_ip_address)
thread_robot_finder.start()
app.set_robot_ip_address('192.168.0.36')


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
        data = {'ip': '192.168.0.32'}
        response = requests.post('http://' + app.robot_ip_address + ':8001' + '/basestationip', data=data)
        # if response.status_code == 200:
        #     response2 = requests.get('http://' + app.robot_ip_address + ':8001' + '/')
    return 'ok'


@app.route('/robotposition')
def fetch_robot_position():
    position = refresh_kinect()
    return jsonify(angle=position.get_angle_in_deg(),
                   position=(position.position[0], position.position[1]))


@app.route('/cubeposition', methods=['POST'])
def fetch_cube_position():
    cube_position = (-500, -500)
    if request.method == 'POST':
        color = request.form.get('color', None)
        cube_position = app.base_station.cube_finder.get_cube_position_with_color(color)
        if cube_position[0] is not None:
            if cube_position[0]>0:
                play_acquired()
    return jsonify(position_x=cube_position[0] , position_y=cube_position[1])


@app.route('/path', methods=['POST'])
def receive_path():
    if request.method == 'POST':
        position = refresh_kinect()
        path = eval(request.data)
        app.context_provider.set_path(path)
    return "ok"


@app.route('/flag')
def fetch_flag():
    # flag = Flag('Canada').get_matrix()
    flag = ''
    strikes = 0
    play_prometheus()
    for cycle in xrange(cte.NUMBER_OF_WRONG_ANSWER_ALLOWED):
        question = fetch_question()

        if question is None:
            break

        print question
        answer = fetch_answer(question)
        if is_right_answer(answer):
            app.base_station.set_question(question, answer)
            flag_processor = flagProcessor.FlagProcessor(answer)
            flag = flag_processor.get_flag()
            break
        else :
            strikes += 1
            if strikes >= 2:
                answer = 'Burkina Faso'
                app.base_station.set_question(question, answer)
                flag_processor = flagProcessor.FlagProcessor(answer)
                flag = flag_processor.get_flag()
                break

    # app.base_station.set_question('From where is your favorite J-D?', 'Alma')
    # flag = Flag('Alma').get_matrix()
    return jsonify(flag=flag)


# A javaScript fonction calls this method every 250 ms
@app.route('/context')
def get_context():
    app.refresh_since_last_kinect_update += 1
    if app.refresh_since_last_kinect_update >= 4:
        refresh_kinect()
    context = app.context_provider.get_context(app.robot_ip_address)
    return jsonify(context)


@app.route('/changerobotposition', methods=['POST'])
def change():
    if request.method == 'POST':
        position_x = request.form.get('position_x', None)
        position_y = request.form.get('position_y', None)
        angle = request.form.get('angle', None)
        app.base_station.set_robot_position(position_x, position_y, angle)
    return 'ok'


def fetch_question():
    json_question = ''
    question = ''
    for url in cte.ATLAS_WEB_SERVER_URLS:
        try:
            response = requests.get(url, verify=False, timeout=0.5)
            if response.status_code == 200:
                json_question = response.text
                break
        except Exception:
            pass
    try :
        question = json.loads(json_question)['question']
    except Exception:
        print 'No question from Atlas'
        fetch_question()
    return question


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


def refresh_kinect():
    position = app.robot_locator.get_position(app.base_station.kinect)
    app.base_station.robot_position = position
    app.refresh_since_last_kinect_update = 0
    app.context_provider.add_known_position(position.position)
    return position


if __name__ == '__main__':  # pragma: no cover
    app.run(host='0.0.0.0', port=SERVER_PORT, use_reloader=False, threaded=False)
    thread_robot_finder.stop()