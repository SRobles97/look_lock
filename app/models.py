from flask import current_app
from flask_login import UserMixin
from app import db
from datetime import datetime


def get_current_time():
    tz = current_app.config['TIME_ZONE']
    return datetime.now(tz)


class User(UserMixin, db.Model):
    __tablename__ = 'users'  # Asigna un nombre a la tabla

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    image_url = db.Column(db.String(256))

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'image_url': self.image_url
        }


class FailedLoginAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=get_current_time)
    attempted_url = db.Column(db.String(512))

    def __init__(self, attempted_url):
        self.attempted_url = attempted_url

    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'attempted_url': self.attempted_url
        }
