import secrets
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.String(), primary_key=True)
    publicKey = db.Column(db.String(), nullable=False)

    def __init__(self, publicKey):
        self.id = secrets.token_hex(5)
        self.publicKey = publicKey

    def __repr__(self):
        return id


class Message(db.Model):
    id = db.Column(db.String(), primary_key=True)
    message = db.Column(db.LargeBinary(), nullable=False)
    sender = db.Column(db.String(), db.ForeignKey('user.id'), nullable=False)
    receiver = db.Column(db.String(), db.ForeignKey('user.id'), nullable=False)
    sent_at = db.Column(db.DateTime(), default=datetime.utcnow())

    def __init__(self, message, sender, receiver):
        self.id = secrets.token_hex(16)
        self.message = message.encode()
        self.sender = sender
        self.receiver = receiver

    def __repr__(self):
        return id
