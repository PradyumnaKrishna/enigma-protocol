import os
import secrets

from flask import Flask, jsonify
from flask_socketio import SocketIO, send, join_room
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_urlsafe(32)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins='*')

USERS = []


@app.route('/login')
def new():
    ID = secrets.token_hex(4)
    USERS.append(ID)
    return jsonify({'user': ID}), 200


@app.route('/connect/<ID>')
def connect(ID):
    if ID in USERS:
        return jsonify({'status': True}), 200
    return jsonify({'status': False}), 200


@socketio.on('message')
def handleMessage(msg):
    send(msg, broadcast=True)


@socketio.on('send_message')
def handle_messages(json):
    data = dict(json)
    print('Message: ' + data['message'])
    room = data.pop('to')
    socketio.emit('receive_message', data, to=room)


@socketio.on('join_room')
def handle_join_room_event(data):
    room = data.pop('user')
    join_room(room)
    socketio.emit("room_announcements", "Join Room Callback", to=room)


if __name__ == '__main__':
    port = os.getenv('PORT', 5000)
    socketio.run(app, host='0.0.0.0', port=port)
