#!/usr/bin/env python3

import json
import sys
from flask import Flask, request, redirect
from flask.json import jsonify
from unicornhatmini import UnicornHATMini
app = Flask(__name__)

test_mode = '--test' in sys.argv

if not test_mode:
    unicornhatmini = UnicornHATMini()

status = { 
    'presence': None,
    'override': None
}

def set_state(text):
    if text in config['statuses']:
        set_color(config['statuses'][text])
        print(f"State {text}; {config['statuses'][text]}.")
    elif text == 'off':
        set_color('off')
        print(f"State off.")
    elif text in config['colors']:
        set_color(text)
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

@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return '200 - OK'

@app.route('/')
def root():
    if status['color'] == 'off':
        current = '#000000'
    else:
        current = '#%02x%02x%02x' % (config['colors'][status['color']][0],config['colors'][status['color']][1],config['colors'][status['color']][2])
    return """
<html>
    <head>
        <meta http-equiv="refresh" content="30">
        <style>
            p {{
                display: block;
                width: 100%;
                max-width: 400px;
                padding: 16px;
                margin: 0 auto 16px auto;
                box-sizing: border-box;
                border-style: none;
                border-radius: 6px;
               
            }}
            
            .btn {{
                display: block;
                width: 100%;
                max-width: 400px;
                padding: 16px;
                margin: 0 auto 16px auto;
                box-sizing: border-box;
                border-style: none;
                border-radius: 6px;
                font-size: 1.5em;
            }}
        </style>
    </head>
    <body>
        <p align='center'>
            <svg width="300" height="120">
                <rect width="300" height="120" style="fill:{};stroke-width:3;stroke:black" />
            </svg>
        </p>
        <p>
            <form action="http://busylight.lan:5000/api/presence" method="post">
                <input class='btn' type="submit" name="state" value="purple" />
                <input class='btn' type="submit" name="state" value="blue" />
                <input class='btn' type="submit" name="state" value="green" />
                <input class='btn' type="submit" name="state" value="yellow" />
                <input class='btn' type="submit" name="state" value="orange" />
                <input class='btn' type="submit" name="state" value="red" />
                <input class='btn' type="submit" name="state" value="off" />
                <input type='hidden' name='redirect' value='true' />
            </form>
        </p>
    </body>
</html>
""".format(current)

@app.route('/api/config', methods=['GET'])
def get_config():
    return jsonify(config)

@app.route('/api/state', methods=['GET'])
def get_state():
    return jsonify(status)

@app.route('/api/reload', methods=['GET'])
def load_config():
    global config
    with open('config.json', 'r') as read_file:
        config = json.load(read_file)
    if 'brightness' in config and not test_mode:
        unicornhatmini.set_brightness(config['brightness'])
    return '200 - OK'

@app.route('/api/presence', methods=['POST'])
def set_presence():
    if request.form.get('state'):
        status['presence'] = request.form.get('state').lower()
        if not status['override']:
            set_state(status['presence'])
            if request.form.get('redirect') == 'true':
                return redirect('/')
            else:
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
    load_config()
    if not test_mode:
        unicornhatmini.clear()
    if 'default_state' in config:
        set_state(config['default_state'])
    app.run(host='0.0.0.0')
