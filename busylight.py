#!/usr/bin/env python3

import json
import requests
import sys
import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from flask import Flask, request, redirect
from flask.json import jsonify
from ics import Calendar
app = Flask(__name__)

test_mode = '--test' in sys.argv

if not test_mode:
    from unicornhatmini import UnicornHATMini
    unicornhatmini = UnicornHATMini()
    display_width, display_height = unicornhatmini.get_shape()

status = { 
    'presence': None,
    'override': None
}

def set_state(state):
    if state in config['statuses']:
        set_color(config['statuses'][state])
        print(f"State {state}; {config['statuses'][state]}.")
    elif state == 'off':
        set_color('off')
        print(f"State off.")
    elif state in config['colors']:
        set_color(state)
        print(f"Color {state}.")
    else: 
        print(f"Undefined state {state}.")

def set_color(color):
    if color == 'off':
        status['color']='off'
        if not test_mode: 
            unicornhatmini.clear()
            unicornhatmini.show()
    elif color in config['colors']:
        status['color']=color
        if not test_mode: 
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

@app.route('/api/config', methods=['GET'])
def get_config():
    return jsonify(config)

@app.route('/api/state', methods=['GET'])
def get_state():
    return jsonify(status)

def load_calendar():
    global calendar
    global config
    if config['calendar_enabled']:
        print(f"{datetime.now()} Loading calendar from {config['calendar_url']}")
        calendar = Calendar(requests.get(config['calendar_url']).text)
        print(f"{datetime.now()} Finished loading calendar")

@app.route('/api/calendar', methods=['GET'])
def set_calendar():
    global calendar
    if config['calendar_enabled']:
        print("Setting based on calendar")
        if calendar:
            busy = False
            events = list(calendar.timeline.now())
            for event in events: 
                if not event.all_day:
                    busy = True
            if busy:
                set_calendar_state("busy")
            else:
                set_calendar_state("off")
    if request:
        return get_return()

def set_calendar_state(state):
    status['presence'] = state
    if not status['override']:
        set_state(status['presence'])

@app.route('/api/reload', methods=['GET'])
def load_config():
    global config
    with open('config.json', 'r') as read_file:
        config = json.load(read_file)
    if 'brightness' in config and not test_mode:
        unicornhatmini.set_brightness(config['brightness'])
    load_calendar()
    if request:
        return get_config()

@app.route('/api/presence', methods=['POST'])
def set_presence():
    if request.form.get('state'):
        status['presence'] = request.form.get('state').lower()
        if not status['override']:
            set_state(status['presence'])
        return get_return()
    else:
        return f"Unable to process request.", 400

@app.route('/api/override', methods=['POST'])
def set_override():
    if request.form.get('state'):
        status['override'] = request.form.get('state').lower()
        set_state(status['override'])
        return get_return()
    elif request.form.get('clear').lower() == 'true':
        status['override'] = None
        set_state(status['presence'])
        return get_return()
    else:
        return f"Unable to process request.", 400

def get_return():
    if request:
        if request.form.get('redirect') == 'true':
            return redirect('/')
        else:
            return jsonify(status)
    else:
        return

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
        <h1 align='center'>Presence</h1>
        <p>
            <form action="/api/presence" method="post">
                <button class='btn' type="submit" name="state" value="purple">purple</button>
                <button class='btn' type="submit" name="state" value="blue">blue</button>
                <button class='btn' type="submit" name="state" value="green">green</button>
                <button class='btn' type="submit" name="state" value="yellow">yellow</button>
                <button class='btn' type="submit" name="state" value="orange">orange</button>
                <button class='btn' type="submit" name="state" value="red">red</button>
                <button class='btn' type="submit" name="state" value="off">off</button>
                <input type='hidden' name='redirect' value='true' />
            </form>
        </p>
        <h1 align='center'>Override</h1>
        <p>
            <form action="/api/override" method="post">
                <button class='btn' type="submit" name="state" value="purple">purple</button>
                <button class='btn' type="submit" name="state" value="blue">blue</button>
                <button class='btn' type="submit" name="state" value="green">green</button>
                <button class='btn' type="submit" name="state" value="yellow">yellow</button>
                <button class='btn' type="submit" name="state" value="orange">orange</button>
                <button class='btn' type="submit" name="state" value="red">red</button>
                <button class='btn' type="submit" name="state" value="off">off</button>
                <button class='btn' type="submit" name="clear" value="true">clear</button>
                <input type='hidden' name='redirect' value='true' />
            </form>
        </p>
        <h1 align='center'>Utilities</h1>
        <p>
            <form action="/api/config" method="get">
                <button class='btn' type="submit">Display Configuration</button>
                <input type='hidden' name='redirect' value='true' />
            </form>
            <form action="/api/reload" method="get">
                <button class='btn' type="submit">Reload Config/Calendar</button>
                <input type='hidden' name='redirect' value='true' />
            </form>
        </p>
    </body>
</html>
""".format(current)

scheduler = BackgroundScheduler()
scheduler.add_job(func=load_calendar, trigger="interval", seconds=900)
scheduler.add_job(func=set_calendar, trigger="interval", seconds=60)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    load_config()
    if not test_mode:
        unicornhatmini.clear()
    if 'default_state' in config:
        set_state(config['default_state'])
    set_calendar()
    app.run(host='0.0.0.0')
