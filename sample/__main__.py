
import os.path, random
from flask import Flask, redirect, url_for, jsonify


app = Flask(__name__)
app.config.from_object(__name__)
# since it will only be use by software engineer, debug on is ok
app.debug = True

def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))

@app.route('/')
def hello():
    return redirect(url_for('static', filename='index.html'))

@app.route('/status')
def status():
    poxY = random.randrange(0, 400, 1)
    time = 0
    # if self.runLoop is not None:
    #     time = self.runLoop.getTime()
    #     print "hello"
    me = {  "top": 30,
            "left": poxY,
            "chrono":"chrono: 00m00s" + str(time),
            "robotIP":"0.0.0.0",}
    return jsonify(me)

if __name__ == '__main__':  # pragma: no cover
    app.run(port=8000)