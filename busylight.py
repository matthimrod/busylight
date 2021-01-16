#!/usr/bin/python3

from flask import Flask, request
from flask.json import jsonify
# from unicornhatmini import UnicornHATMini
app = Flask(__name__)

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
    "on-the-phone": "red",
    "Free": "yellow",
    "Away": "green",
    "DoNotDisturb": "red",
    "Busy": "orange"
}

status = {}

@app.route('/heartbeat')
def heartbeat():
    return '200 - OK'

@app.route('/api/presence', methods=['POST'])
def presence():
    if(request.form['presence']):
        status['presence'] = request.form['presence']
    return f"Presence successfully updated to {status['presence']}."

@app.route('/api/state')
def state():
    return jsonify(status["presence"])

if __name__ == '__main__':
    app.run()

# def set_color(color):
