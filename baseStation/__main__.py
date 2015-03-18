import os.path
from flask import Flask, redirect, url_for, jsonify
from robotFinder import RobotFinder
from runLoop import RunLoop

SERVER_PORT = 8000

class MyServer(Flask):
    robot_ip_address = RobotFinder.IP_NOT_FOUND
    def __init__(self, *args, **kwargs):
        super(MyServer, self).__init__(*args, **kwargs)
        self.runLoop = RunLoop()

    def set_robot_ip_address(self, ip):
        self.robot_ip_address = ip

app = MyServer(__name__)
app.config.from_object(__name__)
# since it will only be use by software engineer, debug on is ok
app.debug = True
thread_robot_finder = RobotFinder(app.set_robot_ip_address)
thread_robot_finder.start()


def root_dir():
    return os.path.abspath(os.path.dirname(__file__))

@app.route('/')
def hello():
    return redirect(url_for('static', filename='index.html'))

@app.route('/start')
def start():
    app.runLoop.start()
    return "ok"

@app.route('/context')
def get_context():
    sample_context = app.runLoop.get_status(app.robot_ip_address)
    return jsonify(sample_context)

if __name__ == '__main__':  # pragma: no cover
    app.run(port=SERVER_PORT)
    thread_robot_finder.stop()