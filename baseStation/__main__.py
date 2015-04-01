import os.path
from flask import Flask, abort, redirect, url_for, jsonify
from robotFinder import RobotFinder
from runLoop import RunLoop
from robotConnection import RobotConnection

SERVER_PORT = 8000


class MyServer(Flask):
    robot_ip_address = RobotFinder.IP_NOT_FOUND

    def __init__(self, *args, **kwargs):
        super(MyServer, self).__init__(*args, **kwargs)
        self.run_loop = RunLoop()
        self.robot_connection = None

    def set_robot_ip_address(self, ip):
        self.robot_ip_address = ip
        self.robot_connection = RobotConnection(self.robot_ip_address)

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
    if app.robot_connection is not None:
        app.run_loop.start(app.robot_connection)
    else:
        abort(500)

    return "ok"

# A javaScript fonction calls this method every 250 ms
@app.route('/context')
def get_context():
    sample_context = app.run_loop.get_context(app.robot_ip_address)
    return jsonify(sample_context)

@app.route('/demomoverobot/<x>/<y>')
def demo_move_robot(x, y):
    if app.robot_connection is not None:
        app.robot_connection.send_move_command(x, y)
    else:
        abort(500)
    return "ok"


if __name__ == '__main__':  # pragma: no cover
    app.run(port=SERVER_PORT, use_reloader=False)
    thread_robot_finder.stop()