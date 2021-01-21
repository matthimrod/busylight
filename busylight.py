#!/usr/bin/env python3

import json
import sys
from flask import Flask, request
from flask.json import jsonify
from unicornhatmini import UnicornHATMini
app = Flask(__name__)

test_mode = '--test' in sys.argv

if not test_mode:
    unicornhatmini = UnicornHATMini()

with open('config.json', 'r') as read_file:
    config = json.load(read_file)

status = { 
    'presence': None,
    'override': None
}

@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return '200 - OK'

def set_state(text):
    if text in config['statuses']:
        set_color(config['statuses'][text])
        print(f"State {text}; {config['statuses'][text]}.")
    elif text in config['colors']:
        set_color(config[text])
        print(f"Color {text}.")
    else: 
        print(f"Undefined state {text}.")

def set_color(color):
    if test_mode: 
        return
    elif color == 'off':
        status['color']='off'
        unicornhatmini.clear()
        unicornhatmini.show()
    elif color in config['colors']:
        status['color']=color
        unicornhatmini.set_all(config['colors'][color][0],config['colors'][color][1],config['colors'][color][2])
        unicornhatmini.show()

def get_color():
    if color in status:
        return status['color']
    else:
        return 'off'

@app.route('/api/config', methods=['GET'])
def get_config():
    return jsonify(config)

@app.route('/api/state', methods=['GET'])
def get_state():
    return jsonify(status)

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
        if 'brightness' in config:
            unicornhatmini.set_brightness(config['brightness'])
        unicornhatmini.clear()
    set_state(config['default_state'])
    app.run(host='0.0.0.0')
