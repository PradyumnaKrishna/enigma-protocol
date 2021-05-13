from flask import Flask, jsonify
from flask_socketio import SocketIO, send
from flask_cors import CORS
import secrets

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


@app.route('/login/<ID>')
def login(ID):
    if ID in USERS:
        return jsonify({'status': True}), 200
    return jsonify({'status': False}), 200


@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    send(msg, broadcast=True)


if __name__ == '__main__':
    socketio.run(app)
