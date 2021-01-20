#!/usr/bin/env python3

from flask import Flask, request
from flask.json import jsonify
from unicornhatmini import UnicornHATMini
app = Flask(__name__)

test_mode = True

if not test_mode:
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
    "in-a-meeting": "red",
    "in-presentation": "red", 
    "on-the-phone": "red",
    "other": "blue"
}

status = { 
    'presence': "other",
    'override': None
}

def set_state(text):
    if text in statuses:
        set_color(statuses[text])
        print(f"State {text}; {statuses[text]}.")
    else: 
        set_color(statuses["other"])
        print(f"Undefined state {text}; Using {statuses['other']}.")

def set_color(color):
    if test_mode: 
        return
    elif color == 'off':
        unicornhatmini.clear()
    elif color in colors:
        unicornhatmini.set_all(colors[color][0],colors[color][1],colors[color][2])
        unicornhatmini.show()

def get_color():
    if status['override']:
        return statuses[status['override']]
    else:
        return statuses[status['presence']]

@app.route('/heartbeat')
def heartbeat():
    return '200 - OK'

@app.route('/api/presence', methods=['POST'])
def presence():
    if request.form.get('state'):
        status['presence'] = request.form.get('state').lower()
        if not status['override']:
            set_state(status['presence'])
            return f"Presence {status['presence']} received."
        else:
            return f"Presence {status['presence']} received. Override {status['override']} active."
    else:
        return f"Unable to process request.", 400

@app.route('/api/override', methods=['POST'])
def override():
    if request.form.get('state'):
        status['override'] = request.form.get('state').lower()
        set_state(status['override'])
        return f"Override {status['override']} received."
    elif request.form.get('clear').lower() == 'true':
        status['override'] = None
        set_state(status['presence'])
        return f"Override cleared. Presence {status['presence']} set."
    else:
        return f"Unable to process request.", 400


@app.route('/api/state')
def state():
    return jsonify(presence=status['presence'], override=status['override'], color=get_color())

if __name__ == '__main__':
    if not test_mode:
        unicornhatmini.set_brightness(bright)
        unicornhatmini.clear()
    set_state(status['presence'])
    app.run(host='0.0.0.0')
