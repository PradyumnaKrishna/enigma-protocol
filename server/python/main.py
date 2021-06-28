import os
import secrets

from flask import Flask, jsonify
from flask_socketio import SocketIO, join_room
from flask_cors import CORS

from database import DataBase


app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_urlsafe(32)

CORS(app)
db = DataBase()
socketio = SocketIO(app, cors_allowed_origins='*')


@app.route('/')
def home():
    """ main homepage """
    return "ok", 200


@app.route('/login/<publicKey>')
def new(publicKey):
    """
    create user and store publicKey
    :param: publicKey
    :return: user
    """
    id = db.save_user(publicKey)
    return jsonify({'user': id}), 200


@app.route('/connect/<ID>')
def connect(ID):
    """
    connect to other user
    :param: id
    :return: status, publicKey
    """
    publicKey = db.get_publicKey(ID)
    if publicKey:
        return jsonify({'status': True, 'to': ID, 'publicKey': publicKey}), 200
    return jsonify({'status': False}), 404


@socketio.on('send_message')
def handle_messages(data):
    """
    sends message in perticular room
    """
    socketio.emit('receive_message', data, to=data['to'])


@socketio.on('join_room')
def handle_join_room_event(data):
    """
    user join room
    """
    room = data.pop('user')

    db.update_last_activity(room)

    join_room(room)
    socketio.emit("room_announcements", "Join Room Callback", to=room)


if __name__ == '__main__':
    PORT = os.getenv('PORT', 5000)
    socketio.run(app, host='0.0.0.0', port=PORT)