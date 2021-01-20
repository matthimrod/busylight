#!/usr/bin/env python3

import json
from flask import Flask, request
from flask.json import jsonify
from unicornhatmini import UnicornHATMini
app = Flask(__name__)

test_mode = True

if not test_mode:
    unicornhatmini = UnicornHATMini()
bright = 0.1

with open('config.json', 'r') as read_file:
    config = json.load(read_file)

status = { 
    'presence': 'init',
    'override': None
}

def set_state(text):
    if text in config['statuses']:
        set_color(config['statuses'][text])
        print(f"State {text}; {config['statuses'][text]}.")
    else: 
        set_color(config['statuses']['other'])
        print(f"Undefined state {text}; Using {config['statuses']['other']}.")

def set_color(color):
    if test_mode: 
        return
    elif color == 'off':
        unicornhatmini.clear()
    elif color in config['colors']:
        unicornhatmini.set_all(config['colors'][color][0],config['colors'][color][1],config['colors'][color][2])
        unicornhatmini.show()

def get_color():
    if status['override']:
        return config['statuses'][status['override']]
    else:
        return config['statuses'][status['presence']]

@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return '200 - OK'

@app.route('/api/config', methods=['GET'])
def get_config():
    return jsonify(config)

@app.route('/api/state', methods=['GET'])
def get_state():
    return jsonify(presence=status['presence'], override=status['override'], color=get_color())

@app.route('/api/reload', methods=['GET'])
def reload():
    with open('config.json', 'r') as read_file:
        config = json.load(read_file)
    return jsonify(config)

@app.route('/api/presence', methods=['POST'])
def set_presence():
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
def set_override():
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


if __name__ == '__main__':
    if not test_mode:
        unicornhatmini.set_brightness(bright)
        unicornhatmini.clear()
    set_state(status['presence'])
    app.run(host='0.0.0.0')
