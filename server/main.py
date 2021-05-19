import os
import secrets

from flask import Flask, jsonify, request
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


@app.route('/retreive', methods=['POST'])
def retreive():
    data = request.get_json()
    sender = User.query.filter_by(id=data['sender']).first()
    receiver = User.query.filter_by(id=data['receiver']).first()

    if sender and receiver:
        messages = Message.query.filter_by(sender=sender.id, receiver=receiver.id).order_by(Message.sent_at.desc()).limit(10)
        return jsonify(messages=[i.serialize for i in messages])
    elif sender:
        return jsonify({'receiver': 'not found'}), 404
    elif receiver:
        return jsonify({'sender': 'not found'}), 404
    else:
        return jsonify({'sender': 'not found', 'receiver': 'not found'}), 404


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
