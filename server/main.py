import os
import secrets

from flask import Flask, jsonify
from flask_socketio import SocketIO, join_room
from flask_migrate import Migrate
from flask_cors import CORS

from models import db, User, Message

DB_URL = os.getenv('DB_URL')
PORT = os.getenv('PORT', 5000)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SECRET_KEY'] = secrets.token_urlsafe(32)

CORS(app)
db.init_app(app)
socketio = SocketIO(app, cors_allowed_origins='*')

migrate = Migrate(app, db)


@app.route('/login/<publicKey>')
def new(publicKey):
    user = User(publicKey=publicKey)
    db.session.add(user)
    db.session.commit()
    return jsonify({'user': user.id}), 200


@app.route('/connect/<ID>')
def connect(ID):
    user = User.query.filter_by(id=ID).first()
    if user:
        return jsonify({'status': True, 'to': user.id, 'publicKey': user.publicKey}), 200
    return jsonify({'status': False}), 200


# TODO: API to retrieve encrypted messages
@socketio.on('send_message')
def handle_messages(data):
    message = Message(message=data['message'], sender=data['user'], receiver=data['to'])
    db.session.add(message)
    db.session.commit()
    socketio.emit('receive_message', data, to=data['to'])


@socketio.on('join_room')
def handle_join_room_event(data):
    room = data.pop('user')
    join_room(room)
    socketio.emit("room_announcements", "Join Room Callback", to=room)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=PORT)
