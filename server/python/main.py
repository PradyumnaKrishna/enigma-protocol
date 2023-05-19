"""
FLASK SOCKETIO SERVER
"""

from datetime import datetime
import os
import secrets

from flask import Flask, jsonify
from flask_socketio import SocketIO, join_room
from flask_cors import CORS

from database import DataBase


app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_urlsafe(32)

CORS(app)
db = DataBase()
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route("/")
def home():
    """main homepage"""
    return "ok", 200


@app.route("/login/<public_key>")
def new(public_key):
    """
    create user and store public_key
    :param: public_key
    :return: user
    """
    identity = db.save_user(public_key)
    return jsonify({"user": identity}), 200


@app.route("/connect/<identity>")
def connect(identity):
    """
    connect to other user
    :param: identity
    :return: status, publicKey
    """
    public_key = db.get_public_key(identity)
    if public_key:
        return jsonify({"status": True, "to": identity, "publicKey": public_key}), 200
    return jsonify({"status": False}), 404


@socketio.on("send_message")
def handle_messages(data):
    """
    sends message in perticular room
    """
    socketio.emit("receive_message", data, to=data["to"])
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message_with_timestamp = {
        "timestamp": timestamp,
        "from": data["from"],
        "to": data["to"],
        "message": data["message"]
    }
    socketio.emit("receive_message", message_with_timestamp, to=data["to"])


@socketio.on("join_room")
def handle_join_room_event(data):
    """
    user join room
    """
    room = data.pop("user")

    db.update_last_activity(room)

    join_room(room)
    socketio.emit("room_announcements", "Join Room Callback", to=room)

@socketio.on("get_user_cards")
def handle_get_user_cards():
    """
    get user cards with timestamps
    """
    users = db.get_user_cards()
    user_cards_with_timestamps = []

    for user in users:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_card_with_timestamp = {
            "timestamp": timestamp,
            "user": user
        }
        user_cards_with_timestamps.append(user_card_with_timestamp)

    socketio.emit("receive_user_cards", user_cards_with_timestamps)

if __name__ == "__main__":
    PORT = os.getenv("PORT", "5000")
    socketio.run(app, host="0.0.0.0", port=PORT)
