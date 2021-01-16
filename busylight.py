#!/usr/bin/python3

from flask import Flask, request
from flask.json import jsonify
from unicornhatmini import UnicornHATMini
app = Flask(__name__)

unicornhatmini = UnicornHATMini()
bright = 0.1

colors = {
    "red":    [255,   0,   0],
    "orange": [255, 165,   0],
    "yellow": [255, 255,   0],
    "green":  [  0, 128,   0],
    "blue":   [  0,   0, 255],
    "purple": [128,   0, 128],
    "white":  [255, 255, 255]
}

statuses = {
    "away": "green",
    "berightback": "yellow",
    "busy": "orange",
    "donotdisturb": "red",
    "free": "yellow",
    "on-the-phone": "red"
}

status = {}

@app.route('/heartbeat')
def heartbeat():
    return '200 - OK'

@app.route('/api/presence', methods=['POST'])
def presence():
    if request.form['presence'] and not status['override']:
        status['presence'] = request.form['state'].lower()
        set_state(status['presence'])
        return f"Presence successfully updated to {status['presence']}."
    elif status['override']:
        status['presence'] = request.form['state'].lower()
        return f"Override in place. Keeping override {status['override']}, but setting fallback to {status['presence']}."
    else:
        return f"Unable to process request.", 400

@app.route('/api/override', methods=['POST'])
def override():
    if request.form['override']:
        status['override'] = request.form['state'].lower()
        set_state(status['override'])
        return f"Override successfully updated to {status['override']}."
    elif request.form['clear'].lower() == 'true':
        status['override'] = None
        set_state(status['presence'])
        return f"Presence reverted to {status['presence']}."
    else:
        return f"Unable to process request.", 400


@app.route('/api/state')
def state():
    return jsonify(presence=status['presence'], override=status['override'])

if __name__ == '__main__':
    status['presence'] = None
    status['override'] = None
    unicornhatmini.set_brightness(bright)
    unicornhatmini.clear()
    app.run(host='0.0.0.0')

def set_state(text):
    if statuses.has_key(text):
        set_color(statuses[text])

def set_color(color):
    if color == 'off':
        unicornhatmini.clear()
    elif colors.has_key(color):
        unicornhatmini.set_all(colors[color][0],colors[color][1],colors[color][2])
        unicornhatmini.show()
