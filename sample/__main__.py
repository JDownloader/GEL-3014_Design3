import os.path, random
from flask import Flask, redirect, url_for, jsonify
from time import gmtime, strftime
from robotFinder import RobotFinder

from runLoop import RunLoop

class MyServer(Flask):
    robotIpAddress = RobotFinder.IP_NOT_FOUND
    def __init__(self, *args, **kwargs):
        super(MyServer, self).__init__(*args, **kwargs)
        self.runLoop = RunLoop()
        threadRobotFinder = RobotFinder(self.setBaseIpAdress)
        threadRobotFinder.start()

    def setBaseIpAdress(self, ip):
        self.robotIpAddress = ip

app = MyServer(__name__)
app.config.from_object(__name__)
# since it will only be use by software engineer, debug on is ok
app.debug = True

def root_dir():
    return os.path.abspath(os.path.dirname(__file__))

@app.route('/')
def hello():
    return redirect(url_for('static', filename='index.html'))

@app.route('/start')
def start():
    app.runLoop.start()
    return "ok"

@app.route('/status')
def status():
    poxY = random.randrange(0, 400, 1)
    runTime = app.runLoop.getTime()
    me = {  "top": 30,
            "left": poxY,
            "chrono": strftime("%Mm%Ss",gmtime(runTime)),
            "robotIP":app.robotIpAddress,}
    return jsonify(me)

if __name__ == '__main__':  # pragma: no cover
    app.run(port=8000)