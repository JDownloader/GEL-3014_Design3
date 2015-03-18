import os.path
from flask import Flask, redirect, url_for, jsonify
from baseStation.runLoop import RunLoop

SERVER_PORT = 8000

class MyServer(Flask):
    def __init__(self, *args, **kwargs):
        super(MyServer, self).__init__(*args, **kwargs)

app = MyServer(__name__)
app.config.from_object(__name__)
# since it will only be use by software engineer, debug on is ok
app.debug = True


def root_dir():
    return os.path.abspath(os.path.dirname(__file__))

@app.route('/move')
def robot_move():
    return 'fail'

@app.route('/status')
def robot_get_context():
    return 'ok'

if __name__ == '__main__':  # pragma: no cover
    app.run(port=SERVER_PORT)