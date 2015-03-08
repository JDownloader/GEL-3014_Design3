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

@app.route('/getPosition')
def start():
    app.runLoop.start()
    return "ok"

@app.route('/status')
def status():
    sample_status = app.runLoop.get_status(app.robot_ip_address)
    return jsonify(sample_status)

if __name__ == '__main__':  # pragma: no cover
    app.run(port=SERVER_PORT)